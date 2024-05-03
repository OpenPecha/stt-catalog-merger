import pandas as pd

from stt_catalog_merger.google_sheet_parser import parse_google_sheet
from stt_catalog_merger.merge_meta import convert_to_csv, merge_csv_with_google_sheet
from stt_catalog_merger.update_csv_gender import update_gender

sheet_id = "1ROGuWa4acCZO19p3KHYJPuT1g52r_kUhh5v-Duud4kw"
sheet_name = "stt_data_catalog"


def test_parse_google_sheet():
    # Act
    df = parse_google_sheet(sheet_id, sheet_name)
    # Assert
    assert df.shape == (4, 3)


def test_merge_csv_with_google_sheet():
    # Arrange
    csv_file_path = "./tests/test_data/catalog.csv"
    columns_to_add = ["Speakers", "Duration"]
    id_length = 6
    # Act
    merged_df = merge_csv_with_google_sheet(
        csv_file_path, sheet_id, sheet_name, columns_to_add, id_length
    )
    merged_csv_path = "./tests/test_data/merged_STT.csv"
    convert_to_csv(merged_df, merged_csv_path)
    expected_catalog_path = "./tests/test_data/expected_catalog.csv"
    expected_df = pd.read_csv(expected_catalog_path)
    # Assert
    assert merged_df.shape == (4, 4)
    assert merged_df.equals(expected_df)


def test_update_gender():
    # Arrange
    csv_file_path = "./tests/test_data/merged_STT.csv"
    csv_updated_file_path = "./tests/test_data/updated_merged_STT.csv"
    # Act
    df = pd.read_csv(csv_file_path)
    df["Gender"] = df.apply(update_gender, axis=1)
    df.to_csv(csv_updated_file_path, index=False)

    # Assert
    updated_df = pd.read_csv(csv_updated_file_path)
    expected_df = pd.read_csv("./tests/test_data/expected_catalog_updated.csv")
    assert updated_df.equals(expected_df)
