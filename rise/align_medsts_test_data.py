from rise.common import get_data_root

if __name__ == "__main__":
    medsts_root = get_data_root() / "data/projects/az-deviations/ClinicalSTS"
    test_sentences = medsts_root / "clinicalSTS.test.txt"
    test_scores = medsts_root / "clinicalSTS.test.gs.sim.txt"
    combined = medsts_root / "rise-clinicalSTS-test.csv"

    with test_sentences.open(mode="r") as fh_sent:
        with test_scores.open(mode="r") as fg_score:
            with combined.open(mode="w") as out:
                sent_lines = fh_sent.readlines()
                score_lines = fg_score.readlines()
                for line1, line2 in zip(sent_lines, score_lines):
                    out.write(f"{line1.rstrip()}\t{line2}")
