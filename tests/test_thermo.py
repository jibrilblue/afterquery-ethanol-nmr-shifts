"""Verifier. Cheap structural checks run first; the Hessian recompute is the expensive one.

Atom ordering in ts_geometry is NOT assumed: fragments, forming bonds and endo/exo are
all derived from the submitted geometry alone.
"""
import json, os
from itertools import combinations
import numpy as np
import pytest
from pyscf import gto, dft
from pyscf.hessian import thermo
from pyscf.data import nist

OUT = "/app/output/thermo.json"
TRUTH = "/app/tests/ground_truth.json"
KEYS = {"delta_G_activation_kcal_mol", "delta_G_reaction_kcal_mol", "imaginary_frequency_cm-1",
        "forming_CC_distances_angstrom", "ts_geometry"}
XC = "HYB_MGGA_X_M06_2X,MGGA_C_M06_2X"
COV = {"H": 0.31, "C": 0.76, "O": 0.66}
FD_STEP = 0.005

TOL_DG, TOL_FREQ, TOL_CC, TOL_FREQ_SELF = 0.5, 75.0, 0.08, 10.0
ENDO_MIN_PROJ = 0.5     # Angstrom; calibrate against your own endo/exo TS geometries
GRAD_MAX = 1e-4         # Eh/bohr


# ---------------- helpers ----------------
@pytest.fixture(scope="module")
def data():
    return json.load(open(OUT))


@pytest.fixture(scope="module")
def truth():
    return json.load(open(TRUTH))


def _bonded(sym, X):
    n = len(sym); adj = {i: set() for i in range(n)}
    for i, j in combinations(range(n), 2):
        if np.linalg.norm(X[i] - X[j]) < 1.15 * (COV[sym[i]] + COV[sym[j]]):
            adj[i].add(j); adj[j].add(i)
    return adj


def _fragments(adj):
    seen, frags = set(), []
    for s in adj:
        if s in seen: continue
        stack, comp = [s], set()
        while stack:
            u = stack.pop()
            if u in comp: continue
            comp.add(u); stack.extend(adj[u] - comp)
        seen |= comp; frags.append(sorted(comp))
    return frags


def _formula(sym, idx):
    return {e: sum(sym[i] == e for i in idx) for e in "CHO" if any(sym[i] == e for i in idx)}


@pytest.fixture(scope="module")
def topo(data):
    sym = [a[0] for a in data["ts_geometry"]]
    X = np.array([a[1:4] for a in data["ts_geometry"]], float)
    assert len(sym) == 22, "TS must have 22 atoms (C9H10O3)"
    adj = _bonded(sym, X); frags = _fragments(adj)
    assert len(frags) == 2, f"expected 2 weakly-bound fragments, found {len(frags)}"
    diene = next(f for f in frags if _formula(sym, f) == {"C": 5, "H": 8})
    dpile = next(f for f in frags if _formula(sym, f) == {"C": 4, "H": 2, "O": 3})
    cc = sorted((float(np.linalg.norm(X[i] - X[j])), i, j) for i in diene for j in dpile
                if sym[i] == "C" and sym[j] == "C")
    p1 = cc[0]; p2 = next(c for c in cc if c[1] != p1[1] and c[2] != p1[2])
    pairs = [(p1[1], p1[2]), (p2[1], p2[2])]
    assert max(p1[0], p2[0]) < 2.7, f"two shortest disjoint inter-fragment C-C contacts too long: {p1[0]:.2f}, {p2[0]:.2f} A"
    n_h = lambda i: sum(sym[k] == "H" for k in adj[i])
    assert all(n_h(p[0]) == 2 for p in pairs), "forming bonds must involve the two CH2 termini of the diene"
    assert all(n_h(p[1]) == 1 for p in pairs), "forming bonds must involve the two CH carbons of the dienophile"
    term = [p[0] for p in pairs]
    methyl = [i for i in diene if sym[i] == "C" and sum(sym[k] == "H" for k in adj[i]) == 3]
    internal = [i for i in diene if sym[i] == "C" and i not in term and i not in methyl]
    alkene = [p[1] for p in pairs]
    carbonyl = [i for i in dpile if sym[i] == "C" and i not in alkene]
    assert len(methyl) == 1 and len(internal) == 2 and len(carbonyl) == 2
    return dict(sym=sym, X=X, pairs=pairs, term=term, internal=internal, alkene=alkene, carbonyl=carbonyl)


def _make_mol(sym, X):
    mol = gto.M(atom=[(s, tuple(x)) for s, x in zip(sym, X)], basis="def2-svp", unit="Angstrom",
                symmetry=False, charge=0, spin=0, max_memory=6000, verbose=0)
    return mol


def _make_mf(mol):
    mf = dft.RKS(mol); mf.xc = XC
    mf.grids.atom_grid = (99, 590); mf.grids.prune = None
    mf.conv_tol = 1e-10; mf.max_cycle = 200
    return mf


def _fd_hessian(mol, mf0):
    n = mol.natm; X0 = mol.atom_coords(); dm0 = mf0.make_rdm1(); H = np.zeros((3 * n, 3 * n))
    for i in range(n):
        for k in range(3):
            g = []
            for s in (+1, -1):
                X = X0.copy(); X[i, k] += s * FD_STEP
                m = mol.set_geom_(X, unit="Bohr", inplace=False); m.verbose = 0
                mf = _make_mf(m); mf.kernel(dm0=dm0); assert mf.converged
                g.append(mf.nuc_grad_method().kernel().ravel())
            H[3 * i + k] = (g[0] - g[1]) / (2 * FD_STEP)
    H = 0.5 * (H + H.T)
    return H.reshape(n, 3, n, 3).transpose(0, 2, 1, 3)


@pytest.fixture(scope="module")
def electronic(topo):
    """SCF + gradient on the submitted geometry (one gradient: cheap)."""
    mol = _make_mol(topo["sym"], topo["X"]); mf = _make_mf(mol); mf.kernel()
    assert mf.converged, "SCF did not converge on submitted TS geometry"
    g = mf.nuc_grad_method().kernel()
    return mol, mf, g


@pytest.fixture(scope="module")
def vib(electronic):
    """Expensive: full Hessian. Analytic if PySCF supports it for meta-GGA, else finite difference."""
    mol, mf, _ = electronic
    try:
        hess = mf.Hessian().kernel()
    except NotImplementedError:
        hess = _fd_hessian(mol, mf)
    res = thermo.harmonic_analysis(mol, hess)
    f = np.asarray(res["freq_wavenumber"])
    f = np.where(np.iscomplex(f), -np.abs(f.imag), f.real)
    o = np.argsort(f)
    return f[o], np.asarray(res["norm_mode"])[o]


# ---------------- tests ----------------
def test_output_schema(data):
    assert set(data) == KEYS, f"keys must be exactly {sorted(KEYS)}"
    assert isinstance(data["delta_G_activation_kcal_mol"], float)
    assert isinstance(data["delta_G_reaction_kcal_mol"], float)
    assert isinstance(data["imaginary_frequency_cm-1"], float) and data["imaginary_frequency_cm-1"] < 0
    assert len(data["forming_CC_distances_angstrom"]) == 2


def test_reported_distances_match_geometry(data, topo, truth):
    calc = sorted(float(np.linalg.norm(topo["X"][i] - topo["X"][j])) for i, j in topo["pairs"])
    rep = sorted(data["forming_CC_distances_angstrom"])
    for c, r, t in zip(calc, rep, sorted(truth["forming_CC_distances_angstrom"])):
        assert abs(c - r) <= 0.005, "reported forming distance disagrees with submitted geometry"
        assert abs(c - t) <= TOL_CC, f"forming distance {c:.3f} vs reference {t:.3f}"


def test_endo_not_exo(topo):
    X = topo["X"]; mid = lambda idx: X[idx].mean(axis=0)
    T, I, D, K = mid(topo["term"]), mid(topo["internal"]), mid(topo["alkene"]), mid(topo["carbonyl"])
    u = (I - T) / np.linalg.norm(I - T)
    proj = float((K - D) @ u)
    assert proj > ENDO_MIN_PROJ, f"anhydride ring not tucked under the diene (projection {proj:.2f} A): exo-like"


def test_stationary_point(electronic):
    _, _, g = electronic
    assert np.abs(g).max() < GRAD_MAX, f"max |gradient| {np.abs(g).max():.2e} Eh/bohr: not a stationary point"


def test_one_imaginary_frequency(vib, data, truth):
    f, _ = vib
    assert int(np.sum(f < 0)) == 1, f"expected exactly 1 imaginary frequency, found {np.sum(f < 0)}: {f[:3]}"
    assert abs(f[0] - data["imaginary_frequency_cm-1"]) <= TOL_FREQ_SELF, "reported frequency != recomputed"
    assert abs(f[0] - truth["imaginary_frequency_cm-1"]) <= TOL_FREQ, "imaginary frequency out of tolerance"


def test_imaginary_mode_is_the_cycloaddition(vib, topo):
    """Cheap proxy for connectivity: +/- displacement must make BOTH forming bonds shorten on one side
    and lengthen on the other (concerted C-C formation), not a methyl rotation or ring flip."""
    _, modes = vib; X = topo["X"]
    q = modes[0] / np.linalg.norm(modes[0], axis=1).max() * 0.2
    d0 = np.array([np.linalg.norm(X[i] - X[j]) for i, j in topo["pairs"]])
    dp = np.array([np.linalg.norm((X + q)[i] - (X + q)[j]) for i, j in topo["pairs"]]) - d0
    dm = np.array([np.linalg.norm((X - q)[i] - (X - q)[j]) for i, j in topo["pairs"]]) - d0
    assert np.all(np.abs(dp) > 0.02) and np.all(dp * dm < 0), f"imaginary mode not C-C forming: {dp}, {dm}"
    assert np.sign(dp[0]) == np.sign(dp[1]), "forming bonds do not move together (not concerted)"


def test_free_energies_against_reference(data, truth):
    # Cannot be recomputed cheaply (needs reactant + product thermochemistry); compared to ground truth.
    assert abs(data["delta_G_activation_kcal_mol"] - truth["delta_G_activation_kcal_mol"]) <= TOL_DG
    assert abs(data["delta_G_reaction_kcal_mol"] - truth["delta_G_reaction_kcal_mol"]) <= TOL_DG
