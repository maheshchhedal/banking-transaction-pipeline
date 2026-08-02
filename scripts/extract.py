import shutil
from pathlib import Path

import pandas as pd

INCOMING_DIR = Path('data/incoming')
ARCHIVE_DIR = Path('data/archive')


def get_new_files(incoming_dir):
    incoming_dir.mkdir(parents=True, exist_ok=True)
    files = list(incoming_dir.glob('*.csv'))
    print(f"\n found {len(files)} new file(s) in {incoming_dir}")
    return files


def read_files(files):
    dataframes = []
    for file in files:
        print(f"reading {file.name}")
        df = pd.read_csv(file)
        dataframes.append(df)

    if not dataframes:
        return pd.DataFrame()

    combined = pd.concat(dataframes, ignore_index=True)
    print(f"combined shape: {combined.shape}")
    return combined


def archive_files(files, archive_dir):
    archive_dir.mkdir(parents=True, exist_ok=True)
    for file in files:
        destination = archive_dir / file.name
        shutil.move(str(file), str(destination))
        print(f"archived {file.name}")


def main():
    files = get_new_files(INCOMING_DIR)
    df = read_files(files)

    if df.empty:
        print("no new data to process")
        return df

    archive_files(files, ARCHIVE_DIR)
    return df


if __name__ == '__main__':
    result = main()
    print(result.head())