# Ethanol NMR Chemical Shifts

Calculate the 1H and 13C NMR chemical shifts for ethanol at the GIAO-B3LYP/cc-pVTZ level of theory using PySCF.

## Difficulty

The task requires setting up GIAO (Gauge-Including Atomic Orbitals) calculations for both the target molecule (ethanol) and the reference standard (tetramethylsilane, TMS). The agent must correctly extract the isotropic magnetic shielding tensors, identify the unique chemical environments, and reference the chemical shifts relative to TMS. This tests a genuine research-grade NMR prediction workflow.

## Author

Jibril Suleiman Lere (ORCID: 0009-0007-1405-2206)

## Reference solution

`solution/solve.sh` provides the pre-computed GIAO-B3LYP/cc-pVTZ chemical shifts for ethanol, referenced against TMS.

## Verification

`tests/test.sh` runs offline in a separate container against a baked-in `ground_truth.json`. The verifier checks the 1H chemical shifts within ±0.5 ppm and the 13C shifts within ±2.0 ppm. Binary reward is written to `/logs/verifier/reward.txt`.
