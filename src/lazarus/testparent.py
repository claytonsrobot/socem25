import subprocess
import sys
import logging
logger = logging.getLogger(__name__)

from socem25.decoractors import log_function_call

# Configuration Variables
## Extramodular file-based configuration variables
None # Documentation could be inaccurate, check. (CLEP 02, it would be better if unpacking JSON and TOML dictionaries was done with a custom function that called automated documentation as well, likely to markdown.)
## Intermodule constants
XCOL = "time"
YCOL = "force"

def proto():
    subprocess.run([
        sys.executable,
        "-m", "src.lazarus.data_assessor",
        "src/lazarus/test_data.csv",
        "--xcol", "time",
        "--ycol", "force"
    ])

@log_function_call(level=logging.INFO)
def run_data_assessor_script(csv_files = None):
    import src
    print(dir(src))
    from src.lazarus.data_assessor import launch_assessment
    if not csv_files:
        csv_files = ["src/lazarus/test_data.csv","src/lazarus/test_data2.csv"]
    for csv_file in csv_files:
        launch_assessment(csv_file, XCOL, YCOL)

@log_function_call(level=logging.INFO)
def run_data_assessor_process(csv_files = None):
    if not csv_files:
        csv_files = ["src/lazarus/test_data.csv"]
    for csv_file in csv_files:
        subprocess.run([
            sys.executable,
            "-m", "src.lazarus.data_assessor",
            csv_file,
            "--xcol", str(XCOL),
            "--ycol", str(YCOL)
        ])

if __name__ == "__main__":
    logger.info("newberry shall rise")
    run_data_assessor_process()