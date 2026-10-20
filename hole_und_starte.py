import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


SOURCE_URL = "https://raw.githubusercontent.com/drpatrickbartels/evaluation/main/hallo_welt.py"
EXPECTED_SOURCE = b'print("Hallo Welt")\n'


def main() -> int:
    try:
        with urlopen(SOURCE_URL, timeout=15) as response:
            source = response.read(len(EXPECTED_SOURCE) + 1)

        if source != EXPECTED_SOURCE:
            raise ValueError("Der Inhalt im Repository entspricht nicht dem erwarteten Programm.")

        with tempfile.TemporaryDirectory() as temp_dir:
            local_program = Path(temp_dir) / "hallo_welt.py"
            local_program.write_bytes(source)
            subprocess.run([sys.executable, str(local_program)], check=True)
    except (OSError, URLError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Fehler: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())