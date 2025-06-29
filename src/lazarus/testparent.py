import subprocess
import sys
import logging

from socem25.decoractors import log_function_call

csv_file = "test_data.csv"
x_col = "time"
y_col = "force"
def hide():
    # ATTEMP 2
    subprocess.run([
        sys.executable,
        "-m", "src.lazarus.data_assessor",
        "src/lazarus/test_data.csv",
        "--xcol", "time",
        "--ycol", "force"
    ])

    """
    # ATTEMP 3
    import src
    print(dir(src))
    from src.lazarus.data_assessor import launch_assessment


    launch_assessment(csv_file, x_col, y_col)
    """
@log_function_call(level=logging.INFO)
def run_data_assessor():
    csv_file = "src/lazarus/test_data.csv"
    subprocess.run([
        sys.executable,
        "-m", "src.lazarus.data_assessor",
        csv_file,
        "--xcol", "time",
        "--ycol", "force"
    ])

if __name__ == "__main__":
    print("hi")
    run_data_assessor()