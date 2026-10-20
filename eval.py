from pathlib import Path

import pandas as pd


class DataFrameAusgabe:
	def __init__(self, dataframe: pd.DataFrame) -> None:
		self.dataframe = dataframe

	def ausgeben(self) -> None:
		print(self.dataframe)


if __name__ == "__main__":
	datei = Path(__file__).with_name("testdaten.csv")
	dataframe = pd.read_csv(datei)
	DataFrameAusgabe(dataframe).ausgeben()
