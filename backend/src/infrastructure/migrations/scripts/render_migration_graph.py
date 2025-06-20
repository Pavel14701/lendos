import ast
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List, Dict

VERSIONS: Path = Path(__file__).parents[1] / "versions"
OUTPUT: Path = Path("backend/docs")
OUTPUT.mkdir(exist_ok=True)

DOT: Path = OUTPUT / "migration_graph.dot"
SVG: Path = OUTPUT / "migration_graph.svg"


def extract(path: Path) -> Tuple[Optional[str], List[str], str]:
    """Extracts revision, down_revision and message from an Alembic migration."""
    rev: Optional[str] = None
    down: List[str] = []
    msg: str = "No message"
    with path.open(encoding="utf-8") as f:
        lines: List[str] = f.readlines()
        for line in lines:
            if line.strip() and not line.strip().startswith('"""'):
                msg = line.strip()
                break
        tree: ast.Module = ast.parse("".join(lines))
        for stmt in tree.body:
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Name):
                        if target.id == "revision":
                            rev = ast.literal_eval(stmt.value)
                        elif target.id == "down_revision":
                            val = stmt.value
                            if isinstance(val, (ast.List, ast.Tuple)):
                                down = [ast.literal_eval(v) for v in val.elts]
                            else:
                                down = [ast.literal_eval(val)]
    return rev, down, msg


def build() -> None:
    """Creates .dot and .svg migration diagram."""
    nodes: Dict[str, str] = {}
    edges: List[Tuple[str, str]] = []
    for file in VERSIONS.glob("*.py"):
        rev, down_list, msg = extract(file)
        if not rev:
            continue
        nodes[rev] = f"{rev}\\n{msg}"
        for parent in down_list:
            edges.append((parent, rev))
    lines: List[str] = [
        "digraph migrations {",
        "  rankdir=TB;",
        '  node [shape=box, style=filled, fillcolor="#F3F4F6"];',
    ]
    lines += [f'  "{rev}" [label="{label}"];' for rev, label in nodes.items()]
    lines += [f'  "{parent}" -> "{child}";' for parent, child in edges]
    lines.append("}")
    DOT.write_text("\n".join(lines), encoding="utf-8")
    subprocess.run(["dot", "-Tsvg", str(DOT), "-o", str(SVG)], check=True)
    with (OUTPUT / "ER_README.md").open("a", encoding="utf-8") as f:
        f.write("\n## 📈 Migration Graph\n")
        f.write("![Migration Graph](migration_graph.svg)\n")


if __name__ == "__main__":
    build()
