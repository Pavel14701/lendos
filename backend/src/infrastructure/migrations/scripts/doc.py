from scripts.build_schema_diagram import build as diagram
from scripts.render_migration_graph import build as graph
from scripts.verify_migrations import run_check as verify


def run_all() -> None:
    """Runs the generation of the ER 
    diagram, migration graph and model 
    verification."""
    diagram()
    graph()
    verify()
