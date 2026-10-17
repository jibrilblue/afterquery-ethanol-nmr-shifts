# Diels-Alder TS Thermochemistry

Compute the Gibbs free energy of activation and reaction for the Diels-Alder reaction of s-cis-1,3-butadiene with ethylene using M06-2X/def2-SVP and PySCF.

## Difficulty

The difficulty comes from a chain of expert decisions where each mistake silently shifts the answer by several kcal/mol: landing on a higher-order saddle or a non-concerted path, skipping quasi-RRHO corrections, omitting the standard-state correction, referencing a complex instead of the separated reactants, or using the wrong butadiene conformer.

## Author

Jibril Suleiman Lere (ORCID: 0009-0007-1405-2206)

## Reference solution

`solution/solve.sh` optimizes the reactants and the cyclohexene product, locates the concerted transition state, confirms it has exactly one imaginary frequency, computes G(298.15 K) using Grimme’s quasi-RRHO treatment, and calculates ΔG‡ and ΔG_rxn.

## Verification

`tests/test.sh` runs offline in a separate container against a baked-in `ground_truth.json`. The verifier checks ΔG‡ and ΔG_rxn within ±0.5 kcal/mol, the imaginary frequency within ±75 cm⁻¹, and the forming C-C distances within ±0.05 Å. Binary reward is written to `/logs/verifier/reward.txt`.
