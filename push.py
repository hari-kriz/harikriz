import subprocess
import sys

GIT = r"C:\Program Files\Git\bin\git.exe"

def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    return result.returncode

msg = input("Commit message: ").strip()
if not msg:
    print("No commit message provided. Aborting.")
    sys.exit(1)

print("\n— Staging all changes...")
run([GIT, "add", "-A"])

print("\n— Committing...")
if run([GIT, "commit", "-m", msg]) != 0:
    print("Nothing to commit.")
    sys.exit(0)

print("\n— Pushing...")
run([GIT, "push"])

print("\nDone.")
