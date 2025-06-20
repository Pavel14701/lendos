import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Final

from backend.src.infrastructure.migrations.scripts._types import TableSchema
from scripts.inspect_models import get_model_definitions
from scripts.format_migration import render_upgrade_downgrade
from scripts.generate_docs import generate_markdown_doc

MIGRATIONS_DIR: Final[Path] = Path(__file__).parents[1] / "versions"

def create_revision(message: str) -> Path:
    rev_id: str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename: str = f"{rev_id}_{message.lower().replace(' ', '_')}.py"
    path: Path = MIGRATIONS_DIR / filename
    subprocess.run([
        "uv", "run", "alembic", "revision",
        "-m", message,
        "--rev-id", rev_id
    ], check=True)
    return path

def main() -> None:
    if len(sys.argv) < 2:
        print("❗ Usage: python scripts/create_migration.py \"Message for revision\"")
        return
    message: str = " ".join(sys.argv[1:])
    path: Path = create_revision(message)
    models: list[TableSchema]  = get_model_definitions()
    upgrade: str
    downgrade: str
    upgrade, downgrade = render_upgrade_downgrade(models)
    generate_markdown_doc(path.name, message, models)
    with open(path, "r+", encoding="utf-8") as f:
        contents: str = f.read()
        contents = contents.replace("pass", upgrade, 1).replace("pass", downgrade, 1)
        f.seek(0)
        f.write(contents)
        f.truncate()
    print(f"✅ Migration created and filled: {path.relative_to(Path.cwd())}")

if __name__ == "__main__":
    main()
