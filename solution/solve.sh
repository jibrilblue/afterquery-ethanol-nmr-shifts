#!/bin/bash

cat << 'PYEOF' > /app/solve.py
import json
import os
import numpy as np
from pyscf import gto, scf
import pyqmc.api as pyq
import logging

logging.disable(logging.WARNING)
np.random.seed(42)

mol = gto.Mole()
mol.atom = [
    ["O", (0.0, 0.0, 0.0)],
    ["H", (0.0, -0.757, 0.587)],
    ["H", (0.0, 0.757, 0.587)]
]
mol.basis = "cc-pVDZ"
mol.charge = 0
mol.spin = 0
mol.build()

chk_path = "/app/data/h2o_rhf.chk" if os.path.exists("/app") else "h2o_rhf.chk"
out_path = "/app/output/vmc.json" if os.path.exists("/app") else "vmc.json"

mf = scf.RHF(mol)
mf.chkfile = chk_path
mf.kernel()
hf_energy = float(mf.e_tot)

wf_slater = pyq.Slater(mol, mf)
wf_jastrow, _ = pyq.generate_jastrow(mol)
wf = pyq.MultiplyWF(wf_slater, wf_jastrow)

configs = pyq.initial_guess(mol, nconfig=1000)
grad_acc = pyq.gradient_generator(mol, wf)
wf, _ = pyq.line_minimization(wf, configs, grad_acc, max_iterations=15, verbose=False)

# VMC (Agent gets to choose convergence)
vmc_data, configs = pyq.vmc(
    wf, configs, nblocks=400,
    accumulators={'energy': pyq.EnergyAccumulator(mol)}
)
vmc_energy = float(np.mean(vmc_data['energytotal']))

if vmc_energy >= hf_energy:
    print("Warning: VMC energy is not lower than HF.")

correlation_energy = vmc_energy - hf_energy

out = {
    "hf_energy_hartree": hf_energy,
    "vmc_energy_hartree": vmc_energy,
    "correlation_energy_hartree": correlation_energy
}

with open(out_path, "w") as f:
    json.dump(out, f, indent=2)

print("\n--- SIMULATION COMPLETE ---")
print(json.dumps(out, indent=2))
PYEOF

python3 /app/solve.py
