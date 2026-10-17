import json
import os
import numpy as np
from pyscf import gto, dft
from pyscf.hessian import thermo

def test_output_exists():
    assert os.path.exists('/app/output/kepler.json'), "Output file missing"

def test_energies_and_tolerances():
    with open('/app/output/kepler.json') as f:
        data = json.load(f)
    with open('/app/tests/ground_truth.json') as f:
        truth = json.load(f)

    # 1. Check energies within tolerance
    assert abs(data['delta_G_activation_kcal_mol'] - truth['delta_G_activation_kcal_mol']) <= 0.5, "DG‡ out of tolerance"
    assert abs(data['delta_G_reaction_kcal_mol'] - truth['delta_G_reaction_kcal_mol']) <= 0.5, "DG_rxn out of tolerance"
    
    # 2. Check imaginary frequency
    assert abs(data['imaginary_frequency_cm-1'] - truth['imaginary_frequency_cm-1']) <= 75.0, "Imaginary frequency out of tolerance"

    # 3. Check forming CC distances
    dists = data['forming_CC_distances_angstrom']
    truth_dists = truth['forming_CC_distances_angstrom']
    assert len(dists) == 2, "Must provide exactly two forming distances"
    for d, td in zip(dists, truth_dists):
        assert abs(d - td) <= 0.05, "Forming distances out of tolerance"

def test_ts_hessian_and_connectivity():
    """Independently recomputes Hessian to verify exactly 1 imaginary freq."""
    with open('/app/output/kepler.json') as f:
        data = json.load(f)
    
    # Rebuild molecule from submitted TS geometry
    mol = gto.Mole()
    mol.atom = data['ts_geometry']
    mol.basis = 'def2-svp'
    mol.charge = 0
    mol.spin = 0
    mol.max_memory = 2000
    mol.build()

    # Recompute Hessian
    mf = dft.RKS(mol)
    mf.xc = 'M06-2X'
    mf.grids.level = 4 # roughly (99,590)
    mf.conv_tol = 1e-10
    mf.kernel()
    
    hess = mf.Hessian().kernel()
    
    # Get eigenvalues (mass-weighted to get frequencies)
    freq = thermo.harmonic_analysis(mol, hess)['freq_wavenumber']
    
    # Count imaginary frequencies (negative values)
    imag_freqs = [f for f in freq if f < 0]
    assert len(imag_freqs) == 1, f"Expected exactly 1 imaginary frequency, found {len(imag_freqs)}"
