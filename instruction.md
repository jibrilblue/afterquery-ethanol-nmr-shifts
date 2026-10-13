Dinitrogen is a classic test case for the fixed-node approximation in diffusion Monte Carlo: the nodes of a single-determinant trial wavefunction are imperfect, and the resulting DMC energy is biased relative to the exact non-relativistic limit. Your task is to quantify that bias by running fixed-node DMC with two different trial wavefunctions.

**The system**

The molecule is N2 at the experimental bond length of 1.098 Angstrom, with both nitrogen atoms on the z axis. The RHF orbitals are provided in a PySCF checkpoint file at `/app/data/n2_rhf.chk`. The basis set is cc-pVDZ.

**The calculation**

Load the RHF checkpoint with PySCF. Build a Slater-Jastrow trial wavefunction using PyQMC's default two-body Jastrow. Optimize the Jastrow parameters by VMC energy minimization with a sufficiently large sample. Run VMC with the optimized trial, equilibrate for a few thousand steps, and accumulate the energy. Run fixed-node DMC with a time step of 0.01 a.u., discarding the first 20 percent of steps for equilibration and accumulating the energy over the remainder. Build a multi-reference trial from a CAS(2,2) expansion, optimize its Jastrow, and run a second fixed-node DMC.

**Output format**

Write your results to `/app/output/dmc.json`. The file should include all calculated energies, the optimized Jastrow parameters, the statistical errors, and the difference between the two DMC energies as the fixed-node error in kcal/mol.

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
