import json
import os

def test_output_exists():
    assert os.path.exists('/app/output/nmr.json'), "Output file missing"

def test_nmr_shifts():
    with open('/app/output/nmr.json') as f:
        data = json.load(f)
    with open('/app/tests/ground_truth.json') as f:
        truth = json.load(f)

    # Check Hydrogen shifts within 0.5 ppm
    assert len(data['h_shifts']) == len(truth['h_shifts']), "Incorrect number of H shifts"
    for h, t_h in zip(sorted(data['h_shifts']), sorted(truth['h_shifts'])):
        assert abs(h - t_h) <= 0.5, f"H shift {h} out of tolerance vs {t_h}"

    # Check Carbon shifts within 2.0 ppm
    assert len(data['c_shifts']) == len(truth['c_shifts']), "Incorrect number of C shifts"
    for c, t_c in zip(sorted(data['c_shifts']), sorted(truth['c_shifts'])):
        assert abs(c - t_c) <= 2.0, f"C shift {c} out of tolerance vs {t_c}"
