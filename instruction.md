Compute the Gibbs free energy of activation and reaction at 298.15 K for the endo Diels-Alder reaction of isoprene with maleic anhydride, using M06-2X/def2-SVP in PySCF with geomeTRIC.

The agent is given the reactant geometries (/app/data/isoprene.xyz, /app/data/maleic_anhydride.xyz). It must optimize the reactants and the product, locate the endo concerted transition state, and confirm that the TS connects reactants to product.

**Connectivity Operationalization:**
Displace the TS geometry along the imaginary normal mode by ±0.2 Å. Re-optimize both displaced geometries. Verify that one relaxation leads to the separated reactants (forming C-C distances > 3.0 Å) and the other leads to the product (forming C-C distances < 1.8 Å).

**Thermochemistry Specifications:**
Compute G(298.15 K) from the Hessians using Grimme’s quasi-RRHO treatment. Use the standard parameters: Bav = 100 cm⁻¹, cutoff = 100 cm⁻¹. Apply the 1 atm → 1 M standard-state correction of +1.89 kcal/mol per molecule.

**Definitions:**
ΔG_rxn = G(product) - [G(isoprene) + G(maleic_anhydride)]
ΔG‡ = G(TS) - [G(isoprene) + G(maleic_anhydride)]

**Settings:**
PySCF and geomeTRIC versions, grid (99,590) without pruning, conv_tol=1e-10, no symmetry, GAU_TIGHT optimizer convergence.

Write your results to `/app/output/thermo.json`. The JSON must contain exactly these keys:
- `delta_G_activation_kcal_mol` (float)
- `delta_G_reaction_kcal_mol` (float)
- `imaginary_frequency_cm-1` (float)
- `forming_CC_distances_angstrom` (list of two floats)
- `ts_geometry` (list of lists, e.g., `[["C", x, y, z], ...]`)

You have 14400 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
