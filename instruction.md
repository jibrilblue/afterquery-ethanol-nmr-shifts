Calculate the 1H and 13C NMR chemical shifts for ethanol at the GIAO-B3LYP/cc-pVTZ level of theory using PySCF.

You must:
1. Optimize the geometry of ethanol.
2. Optimize the geometry of the reference standard, tetramethylsilane (TMS).
3. Compute the isotropic magnetic shielding tensors for all unique atoms in both molecules.
4. Calculate the chemical shifts in ppm relative to TMS: `delta = sigma_TMS - sigma_sample`.

Write your results to `/app/output/nmr.json`. The JSON must contain exactly these keys:
- `h_shifts`: A list of the 1H chemical shifts (floats).
- `c_shifts`: A list of the 13C chemical shifts (floats).

You have 14400 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
