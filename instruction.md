Carbon monoxide is a classic test case for the fixed-node approximation in
diffusion Monte Carlo: the nodes of a single-determinant trial wavefunction are
imperfect, and the resulting DMC energy is biased relative to the exact
non-relativistic limit. Your task is to quantify that bias by running
fixed-node DMC with two different trial wavefunctions.

**The system**

The molecule is CO at the experimental bond length of 1.128 Angstrom, with the
carbon at the origin and the oxygen on the positive z axis. The RHF orbitals are
provided in a PySCF checkpoint file at `/app/data/co_rhf.chk`. The basis set is
cc-pVDZ.

**The calculation**

All calculations use PyQMC, the real-space QMC module in PySCF.

1. **Optimize a Slater-Jastrow trial wavefunction.** Start from the RHF
determinant in the checkpoint file. Add a two-body Jastrow factor and
optimize the Jastrow parameters by VMC energy minimization.
Report the final Jastrow parameters.

2. **Run VMC with the optimized trial wavefunction.** Equilibrate the walkers,
then accumulate the VMC energy. Report the VMC energy and its statistical
error.

3. **Run fixed-node DMC with the same trial wavefunction.** Use a time step of
0.01 atomic units and run long enough that the DMC energy has clearly
plateaued. Report the DMC energy and its statistical error.

4. **Estimate the fixed-node error.** Run a second fixed-node DMC calculation
using a multi-reference trial wavefunction built from a small
complete-active-space (CAS) expansion. The CAS is the two pi-derived
orbitals of CO (CAS(2,2)). Report the DMC energy from this multi-reference
trial and the difference between the two DMC energies. That difference is
your estimate of the fixed-node error.

**What to produce**

Write `/app/output/dmc.json`:

{
"jastrow_params": [],
"vmc_energy_hartree": 0.0,
"vmc_error_hartree": 0.0,
"dmc_energy_hartree": 0.0,
"dmc_error_hartree": 0.0,
"dmc_multi_ref_energy_hartree": 0.0,
"fixed_node_error_kcal_mol": 0.0,
"notes": "anything you want the reviewer to know"
}

Field meaning:

- `jastrow_params`: the optimized Jastrow parameters, in the order returned by
PyQMC.
- `vmc_energy_hartree`: the VMC energy in Hartree.
- `vmc_error_hartree`: the statistical error on the VMC energy in Hartree.
- `dmc_energy_hartree`: the fixed-node DMC energy with the single-reference
Slater-Jastrow trial, in Hartree.
- `dmc_error_hartree`: the statistical error on that DMC energy in Hartree.
- `dmc_multi_ref_energy_hartree`: the fixed-node DMC energy with the
multi-reference CAS(2,2) trial, in Hartree.
- `fixed_node_error_kcal_mol`: the difference between the two DMC energies,
converted to kcal/mol.
- `notes` is free text and is not graded.

**How your answer is judged**

An automated check compares your numbers against a reference computed
independently on the same checkpoint file with the same PyQMC version. Absolute
energies are compared with a tolerance that absorbs a constant offset from
different Jastrow parameterizations. The fixed-node error is compared directly.
Statistical errors must be smaller than the reported energy differences.

Only `/app/output/dmc.json` is collected. Anything else you write is discarded.

You have 14400 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
