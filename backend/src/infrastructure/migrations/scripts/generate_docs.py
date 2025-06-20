from datetime import datetime
from pathlib import Path
from typing import List

from backend.src.infrastructure.migrations.scripts._types import TableSchema


def generate_markdown_doc(
    filename: str, 
    message: str, 
    models: List[TableSchema]
) -> None:
    docs: Path = Path("backend/docs")
    docs.mkdir(exist_ok=True, parents=True)
    content: List[str] = [
        f"# Migration: {filename}",
        f"**Created**: {datetime.now().isoformat()}",
        f"**Message**: {message}",
        ""
    ]
    for model in models:
        content.append(f"## Table `{model['name']}`")
        for col in model["columns"]:
            line = f"- `{col['name']}` ({col['type']})"
            if col["primary_key"]:
                line += " [PK]"
            if col["comment"]:
                line += f" — {col['comment']}"
            content.append(line)
        content.append("")
    with open(docs / f"{filename}.md", "w", encoding="utf-8") as f:
        f.write("\n".join(content))
