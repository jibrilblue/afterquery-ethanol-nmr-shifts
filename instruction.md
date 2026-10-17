Compute the Gibbs free energy of activation and reaction at 298.15 K for the Diels-Alder reaction of s-cis-1,3-butadiene with ethylene, using M06-2X/def2-SVP in PySCF with geomeTRIC.

The agent is given only the reactant geometries (/app/data/butadiene.xyz, /app/data/ethylene.xyz). It must optimize the reactants and the cyclohexene product, locate the concerted transition state on its own, and confirm that the TS has exactly one imaginary frequency and connects reactants to product.

**Definitions & Operationalization:**
1. **ΔG_rxn:** Defined as G(cyclohexene) - [G(butadiene) + G(ethylene)].
2. **ΔG‡:** Defined as G(TS) - [G(butadiene) + G(ethylene)].
3. **TS Connectivity Check:** The agent must displace the TS geometry along the imaginary normal mode by ±0.2 Å, re-optimize both displaced geometries, and verify that one relaxation leads to the separated reactants (forming C-C distances > 3.0 Å) and the other leads to the product (forming C-C distances < 1.8 Å).
4. **Thermochemistry:** Compute G(298.15 K) from the Hessians using Grimme’s quasi-RRHO treatment (cutoff 100 cm⁻¹) with the 1 atm → 1 M standard-state correction (+1.89 kcal/mol per molecule).

All numerical settings are pinned: PySCF and geomeTRIC versions, grid (99,590) without pruning, conv_tol=1e-10, no symmetry, GAU_TIGHT optimizer convergence.

**Output format:**
Write your results to `/app/output/kepler.json`. The JSON file must contain exactly these keys:
- `delta_G_activation_kcal_mol` (float)
- `delta_G_reaction_kcal_mol` (float)
- `imaginary_frequency_cm-1` (float)
- `forming_CC_distances_angstrom` (list of two floats, representing the two new bonds in the TS)
- `ts_geometry` (list of lists, e.g. `[["C", x, y, z], ...]`)

You have 14400 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
