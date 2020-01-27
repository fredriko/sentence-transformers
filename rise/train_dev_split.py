import pandas as pd
"""
MedSTS structure: sentence1 \t sentence2 \t score
"""
from rise.common import get_data_root

if __name__ == "__main__":
    medsts_root = get_data_root() / "data/projects/az-deviations/ClinicalSTS"
    train_file = medsts_root / "clinicalSTS.train.txt"
    train_csv = medsts_root / "rise-clinicalSTS-train.csv"
    dev_csv = medsts_root / "rise-clinicalSTS-dev.csv"
    sentence_one_field = "sentence1"
    sentence_two_field = "sentence2"
    score_field = "score"

    train_df = pd.read_csv(train_file, sep="\t")
    #train_df.columns = [sentence_one_field, sentence_two_field, score_field]
    train_df.reset_index()

    print(f"Train: {train_df.shape[0]}")
    print(train_df.head())
    dev_df = train_df.sample(n=75, random_state=42, replace=False)
    train_df = train_df.drop(dev_df.index)
    print(f"Train: {train_df.shape[0]}")
    print(f"Dev: {dev_df.shape[0]}")

    dev_df.to_csv(dev_csv, index=False, sep="\t")
    train_df.to_csv(train_csv, index=False, sep="\t")

    # TODO save dev_df and train_df to csv files
