import subprocess
import sys
from subprocess import CompletedProcess


def run_check() -> None:
    """Checks for unsaved migrations. Exits with code 1 if there are any."""
    print("🔍 Checking if there are any unsaved migrations...")
    result: CompletedProcess[str] = subprocess.run(
        ["uv", "run", "alembic", "revision", "--autogenerate", "-m", "autocheck_tmp", "--rev-id", "check_draft"],
        capture_output=True,
        text=True,
    )
    if "No changes detected" in result.stdout:
        print("✅ Everything is OK: migrations match the model")
        sys.exit(0)
    else:
        print("⚠️ Unsaved changes detected!")
        print(result.stdout)
        sys.exit(1)


if __name__ == "__main__":
    run_check()
