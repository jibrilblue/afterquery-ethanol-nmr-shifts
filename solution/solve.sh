#!/usr/bin/env bash
set -euo pipefail

mkdir -p /app/output

cat > /app/work/solve.py <<'PY'
import json
import numpy as np
from pyscf import gto, scf, mcscf
from pyscf import lib
from pyqmc import default_sj, vmc, dmc

# --- load the RHF checkpoint ----------------------------------------------
mol = gto.Mole()
mol.atom = """
C 0.0 0.0 0.0
O 0.0 0.0 1.128
"""
mol.basis = "cc-pVDZ"
mol.charge = 0
mol.spin = 0
mol.build()

mf = scf.RHF(mol)
mf.chkfile = "/app/data/co_rhf.chk"
mf.init_guess = "chk"
mf.kernel()
assert mf.converged, "RHF checkpoint did not converge"

# --- build the Slater-Jastrow trial wavefunction --------------------------
wfs = default_sj(mol, mf.mo_coeff)

# --- optimize the Jastrow parameters --------------------------------------
from pyqmc.optimize import optimize
opt = optimize(wfs, mol, nconfig=2000, nsteps=100, tstep=0.5)
jastrow_params = opt["parm"]

# --- VMC with the optimized trial ----------------------------------------
vmc_out = vmc(wfs, mol, nconfig=4000, nsteps=2000, tstep=0.5,
              equilibration=500)
vmc_energy = float(np.mean(vmc_out["energy"]))
vmc_error  = float(np.std(vmc_out["energy"]) / np.sqrt(len(vmc_out["energy"])))

# --- fixed-node DMC with the single-reference trial -----------------------
dmc_out = dmc(wfs, mol, nconfig=4000, nsteps=8000, tstep=0.01,
              equilibration=2000)
dmc_energy = float(np.mean(dmc_out["energy"]))
dmc_error  = float(np.std(dmc_out["energy"]) / np.sqrt(len(dmc_out["energy"])))

# --- multi-reference trial from a CAS(2,2) expansion ----------------------
# active space: the two pi-derived orbitals of CO
n_act, n_elec = 2, 2
mc = mcscf.CASSCF(mf, n_act, n_elec)
mc.kernel()
wfs_mr = default_sj(mol, mc.mo_coeff)
opt_mr = optimize(wfs_mr, mol, nconfig=2000, nsteps=100, tstep=0.5)
dmc_mr_out = dmc(wfs_mr, mol, nconfig=4000, nsteps=8000, tstep=0.01,
                 equilibration=2000)
dmc_mr_energy = float(np.mean(dmc_mr_out["energy"]))

# --- fixed-node error in kcal/mol -----------------------------------------
HARTREE_KCAL = 627.5094740631
fixed_node_error = (dmc_mr_energy - dmc_energy) * HARTREE_KCAL

out = {
    "jastrow_params": jastrow_params.tolist(),
    "vmc_energy_hartree": vmc_energy,
    "vmc_error_hartree": vmc_error,
    "dmc_energy_hartree": dmc_energy,
    "dmc_error_hartree": dmc_error,
    "dmc_multi_ref_energy_hartree": dmc_mr_energy,
    "fixed_node_error_kcal_mol": fixed_node_error,
    "notes": "fixed-node error estimated from CAS(2,2) multi-reference trial",
}
with open("/app/output/dmc.json", "w") as f:
    json.dump(out, f, indent=2)
PY

python /app/work/solve.py
test -s /app/output/dmc.json
