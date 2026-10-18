import json
import os

def test_output_exists():
    assert os.path.exists('/app/output/thermo.json'), "Output file missing"

def test_energies_and_tolerances():
    with open('/app/output/thermo.json') as f:
        data = json.load(f)
    with open('/app/tests/ground_truth.json') as f:
        truth = json.load(f)

    # 1. Check energies within tolerance
    assert abs(data['delta_G_activation_kcal_mol'] - truth['delta_G_activation_kcal_mol']) <= 0.5, "DG‡ out of tolerance"
    assert abs(data['delta_G_reaction_kcal_mol'] - truth['delta_G_reaction_kcal_mol']) <= 0.5, "DG_rxn out of tolerance"
    
    # 2. Check imaginary frequency
    assert abs(data['imaginary_frequency_cm-1'] - truth['imaginary_frequency_cm-1']) <= 75.0, "Imaginary frequency out of tolerance"

    # 3. Check forming CC distances
    dists = data['forming_CC_distances_angstrom']
    truth_dists = truth['forming_CC_distances_angstrom']
    assert len(dists) == 2, "Must provide exactly two forming distances"
    for d, td in zip(dists, truth_dists):
        assert abs(d - td) <= 0.05, "Forming distances out of tolerance"
