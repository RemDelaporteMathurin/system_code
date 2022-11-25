import runpy
import sys
import system_code
from pathlib import Path


def main():

    path_to_app = str(Path(system_code.__path__[0])/'gui_app.py')

    sys.argv = ["streamlit", "run", path_to_app]; 
    runpy.run_module("streamlit", run_name="__main__")


if __name__ == "__main__":
    main()
