from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).with_name('verify_artifacts_v11.py')),run_name='__main__')
