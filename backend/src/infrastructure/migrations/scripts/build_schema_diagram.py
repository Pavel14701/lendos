import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Final

OUTPUT: Final[Path] = Path("backend/docs")
OUTPUT.mkdir(exist_ok=True, parents=True)

DATABASE_URL: Final[str] = 'postgresql+psycopg://{user}:{password}@{host}:{port}/{db}'.format(
    user=os.getenv('POSTGRES_USER', 'user'),
    password=os.getenv('POSTGRES_PASSWORD', 'pass'),
    host=os.getenv('POSTGRES_HOST', 'localhost'),
    port=os.getenv('POSTGRES_PORT', '5432'),
    db=os.getenv('POSTGRES_DB', 'mydb'),
)

DOT: Final[Path] = OUTPUT / "schema.dot"
SVG: Final[Path] = OUTPUT / "schema.svg"


def build() -> None:
    """Generates ER diagram via eralchemy and saves it as .svg"""
    subprocess.run(["eralchemy", "-i", DATABASE_URL, "-o", str(DOT)], check=True)
    subprocess.run(["dot", "-Tsvg", str(DOT), "-o", str(SVG)], check=True)
    with open(OUTPUT / "ER_README.md", "w", encoding="utf-8") as f:
        f.write(
            "# 📊 ER Diagram\n\n![schema](schema.svg)\n\n_Last updated: " +
            f"{datetime.now().isoformat()}_"
        )


if __name__ == "__main__":
    build()
