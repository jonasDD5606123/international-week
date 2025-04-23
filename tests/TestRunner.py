# TestRunner.py
import subprocess

def run_behave():
    result = subprocess.run(["behave", "features/"], capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    run_behave()
