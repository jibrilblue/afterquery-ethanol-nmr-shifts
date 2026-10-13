# fixed-mode-dmc-nodal-quality
task: Fixed-node DMC nodal quality benchmark for N2 — VMC + DMC with single- and multi-reference Slater-Jastrow trials. 
## Difficulty
Author-generated RHF checkpoint for N2 at 1.098 A in cc-pVDZ. Difficulty comes from four dependent stages that each fail silently: Jastrow optimization (a poor optimization biases both VMC and DMC), VMC equilibration (insufficient equilibration leaves walkers out of equilibrium), DMC branching (a time step that is too large introduces bias, one that is too small requires prohibitive run times), and the fixed-node error estimate (which requires a separate multi-reference calculation).

## Author
Jibril Suleiman Lere (ORCID: 0009-0007-1405-2206)

## Reference solution
`solution/solve.sh` loads the RHF checkpoint, builds a Slater-Jastrow trial
wavefunction with PyQMC, optimizes the Jastrow parameters by VMC energy
minimization, runs VMC and fixed-node DMC with the optimized trial, then builds
a multi-reference CAS(2,2) trial, optimizes its Jastrow, and runs a second
fixed-node DMC. The fixed-node error is the difference between the two DMC
energies.

## Verification
`tests/test.sh` runs offline in a separate container against a baked-in
`ground_truth.json` produced by the author's own high-precision PyQMC
calculation. It checks the VMC and DMC energies, the multi-reference DMC
energy, the fixed-node error, and the statistical errors. A guard fails any
submission whose multi-reference DMC energy equals its single-reference DMC
energy, catching a skipped CAS step. Binary reward, written to
`/logs/verifier/reward.txt` on every code path.
