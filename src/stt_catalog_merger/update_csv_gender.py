import pandas as pd


def update_gender(row):
    speakers = str(row["Speakers"])  # Convert to string to handle NaN values
    if pd.isna(speakers):
        return "null"

    if "1 Female" == speakers or "2 Females" == speakers:
        return "Female"
    elif "1 Male" == speakers or "2 Males" == speakers:
        return "Male"
    return "null"


if __name__ == "__main__":
    df = pd.read_csv("./data/merged_csv/STT_NS_1.csv")
    df["Gender"] = df.apply(update_gender, axis=1)
    df.to_csv(
        "/home/gangagyatso/Desktop/work/stt_catalog_merger/data/merged_csv/STT_NS_1.csv",
        index=False,
    )

    print("New CSV file with updated 'Gender' column has been created.")
