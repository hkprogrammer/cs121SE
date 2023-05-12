from src import extractText, processJsonFiles
from pathlib import Path
import os

if __name__ == "__main__":
    p = os.path.abspath("developer/DEV")
    extractText.extract_text_from_json_files(p)
    processJsonFiles.record_json_freq_invert(p)