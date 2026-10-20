import subprocess
import sys
import tempfile
import time
from pathlib import Path
from shutil import copyfile
from urllib.error import URLError
from urllib.request import Request, urlopen


SOURCE_URL = "https://api.github.com/repos/drpatrickbartels/evaluation/contents/eval.py?ref=main"


def main() -> int:
    try:
        request = Request(
            f"{SOURCE_URL}&cache_bust={time.time_ns()}",
            headers={
                "Accept": "application/vnd.github.raw",
                "Cache-Control": "no-cache, no-store",
                "Pragma": "no-cache",
                "User-Agent": "evaluation-fetcher",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        with urlopen(request, timeout=15) as response:
            source = response.read()

        workspace = Path(__file__).parent
        local_program = workspace / "eval.py"
        csv_file = workspace / "testdaten.csv"

        with tempfile.TemporaryDirectory() as temp_dir:
            if local_program.exists() and local_program.read_bytes() == source:
                program_to_run = local_program
            else:
                program_to_run = Path(temp_dir) / "eval.py"
                program_to_run.write_bytes(source)
                copyfile(csv_file, Path(temp_dir) / "testdaten.csv")

            subprocess.run(
                [sys.executable, str(program_to_run), str(csv_file)],
                check=True,
            )
    except (OSError, URLError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Fehler: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())