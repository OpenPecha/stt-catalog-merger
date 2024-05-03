import pandas as pd

from stt_catalog_merger.google_sheet_parser import parse_google_sheet


def convert_to_csv(df, csv_file_path):
    df.to_csv(csv_file_path, index=False)
    print(f"CSV file saved successfully at {csv_file_path}")


def merge_csv_with_google_sheet(
    csv_file_path, google_sheet_id, sheet_name, columns_to_add, id_length
):
    # Read the Google Sheet into a DataFrame
    sheet_df = parse_google_sheet(google_sheet_id, sheet_name)

    # Read the CSV file into a DataFrame
    csv_df = pd.read_csv(csv_file_path)

    # Extract the identifier from the file names in both DataFrames
    sheet_df["file_id"] = sheet_df["ID"].str.extract(rf"STT_(\w{{{id_length}}})")
    csv_df["file_id"] = csv_df["file_name"].str.extract(rf"STT_(\w{{{id_length}}})")

    # Merge based on the first four digits of the file names
    merged_df = pd.merge(
        csv_df, sheet_df[["file_id"] + columns_to_add], on="file_id", how="left"
    )

    # Drop the 'file_id' column as it was only used for merging
    merged_df.drop(columns=["file_id"], inplace=True)

    return merged_df
