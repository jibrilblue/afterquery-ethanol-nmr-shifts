**VMC Correlation Energy for Water**

You are provided with a water (H2O) molecule. Your goal is to calculate the correlation energy recovered by a Slater-Jastrow trial wavefunction using Variational Monte Carlo (VMC). 

**The system**

The molecule is H2O at the experimental geometry: O at (0,0,0), H at (0, -0.757, 0.587), and H at (0, 0.757, 0.587) Angstroms. The basis set is cc-pVDZ. Set `np.random.seed(42)` at the start of your script to ensure reproducibility.

**The calculation**

1. Run a Restricted Hartree-Fock (RHF) calculation to obtain the baseline HF energy.
2. Build a Slater-Jastrow trial wavefunction using PyQMC's default two-body Jastrow.
3. Optimize the Jastrow parameters using VMC.
4. Run a converged VMC simulation to obtain the final VMC energy. You must choose sufficient walkers and blocks to ensure your statistical error is small.
5. Calculate the correlation energy: `E_corr = E_vmc - E_hf`. The VMC energy must be strictly lower than the HF energy.

**Output format**

Write your results to `/app/output/vmc.json`. The JSON file must contain exactly these three keys:
- `hf_energy_hartree`: The baseline RHF energy.
- `vmc_energy_hartree`: The optimized VMC energy.
- `correlation_energy_hartree`: The difference between VMC and HF.

You have 14400 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
