import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


SOURCE_URL = "https://api.github.com/repos/drpatrickbartels/evaluation/contents/hallo_welt.py?ref=main"


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

        local_program = Path(__file__).with_name("hallo_welt.py")
        if not local_program.exists() or local_program.read_bytes() != source:
            local_program.write_bytes(source)

        subprocess.run([sys.executable, str(local_program)], check=True)
    except (OSError, URLError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Fehler: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())