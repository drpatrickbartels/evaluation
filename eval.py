import argparse
import os
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI


MODEL = "GLM-5.3-Flash-NVFP4"
BASE_URL = "https://llm.lab.f4-w.de/v1"


class DataFrameAusgabe:
	def __init__(self, dataframe: pd.DataFrame, client: OpenAI) -> None:
		self.dataframe = dataframe
		self.client = client

	def bewerten(self) -> None:
		benoetigte_spalten = {"frage", "sollantwort"}
		fehlende_spalten = benoetigte_spalten.difference(self.dataframe.columns)
		if fehlende_spalten:
			raise ValueError(
				f"Im DataFrame fehlen erforderliche Spalten: {', '.join(sorted(fehlende_spalten))}"
			)

		istantworten = []
		pruefungen = []
		token_verbraeuche = []
		laufzeiten_ms = []
		for _, zeile in self.dataframe.iterrows():
			startzeit = time.perf_counter_ns()
			antwort = self.client.chat.completions.create(
				model=MODEL,
				messages=[{"role": "user", "content": str(zeile["frage"])}],
			)
			laufzeit_ms = (time.perf_counter_ns() - startzeit) / 1_000_000
			istantwort = (antwort.choices[0].message.content or "").strip()
			sollantwort = str(zeile["sollantwort"]).strip()
			istantworten.append(istantwort)
			pruefungen.append(istantwort.casefold() == sollantwort.casefold())
			token_verbraeuche.append(
				antwort.usage.total_tokens if antwort.usage is not None else None
			)
			laufzeiten_ms.append(round(laufzeit_ms, 2))

		self.dataframe["istantwort"] = istantworten
		self.dataframe["prüfung"] = pruefungen
		self.dataframe["token_verbrauch"] = token_verbraeuche
		self.dataframe["laufzeit_ms"] = laufzeiten_ms

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
	csv_datei = argumente.csv_datei.resolve()
	load_dotenv(dotenv_path=csv_datei.parent / ".env")
	dataframe = pd.read_csv(csv_datei)
	api_schluessel = os.environ.get("OPENAI_API_KEY")
	if not api_schluessel:
		parser.error("Bitte den API-Schlüssel in der Umgebungsvariable OPENAI_API_KEY setzen.")

	client = OpenAI(base_url=BASE_URL, api_key=api_schluessel)
	ausgabe = DataFrameAusgabe(dataframe, client)
	ausgabe.bewerten()
	ausgabe.ausgeben()
