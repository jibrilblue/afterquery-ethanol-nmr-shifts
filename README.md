# H2O VMC Correlation Energy

Calculate the correlation energy recovered by a two-body Slater-Jastrow Variational Monte Carlo (VMC) simulation for the H2O molecule.

## Difficulty

The task requires the agent to set up a full QMC pipeline from scratch: run RHF, construct a Slater-Jastrow wavefunction, optimize the Jastrow parameters to recover correlation energy, and run a converged VMC simulation. The challenge lies in properly equilibrating the walkers, choosing sufficient sampling blocks, and ensuring the variational energy is strictly below the HF baseline without falling into statistical noise.

## Author

Jibril Suleiman Lere (ORCID: 0009-0007-1405-2206)

## Reference solution

`solution/solve.sh` loads the RHF checkpoint, builds a Slater-Jastrow trial wavefunction with PyQMC, optimizes the Jastrow parameters by VMC energy minimization, runs a converged VMC simulation, and calculates the correlation energy (E_vmc - E_hf).

## Verification

`tests/test.sh` runs offline in a separate container against a baked-in `ground_truth.json` produced by the author's own PyQMC calculation. It checks the correlation energy within a tight tolerance derived from the statistical error of the reference run. It also enforces the variational bound, ensuring the agent's VMC energy is strictly lower than the HF energy, preventing trivial cheating. Binary reward is written to `/logs/verifier/reward.txt`.
