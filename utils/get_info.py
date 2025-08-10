from utils.midilogger import stamp
from pathlib import Path

def get_info(section):
    info_file = Path(__file__).parent / "info.md"
    if not info_file.exists():
        stamp(2, "info.md missing")
    else:
        stamp(5, f"scanning info.md for {section}")
        starttag = f"!-->{section}"
        endtag = "!-->"
        lines = info_file.read_text().splitlines()
        printing = False
        printed = False
        for line in lines:
            if endtag in line:
                printing = False
            if printing:
                print(line)
            if starttag in line:
                printing = True
                printed = True
        if not printed:
            print(f"{section} section of info.md not found.")