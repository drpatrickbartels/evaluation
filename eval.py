import argparse
from pathlib import Path

import pandas as pd


class DataFrameAusgabe:
	def __init__(self, dataframe: pd.DataFrame) -> None:
		self.dataframe = dataframe

	def ausgeben(self) -> None:
		print(self.dataframe)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"csv_datei",
		type=Path,
		nargs="?",
		default=Path(__file__).with_name("testdaten.csv"),
	)
	argumente = parser.parse_args()
	dataframe = pd.read_csv(argumente.csv_datei)
	DataFrameAusgabe(dataframe).ausgeben()
