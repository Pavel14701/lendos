from backend.src.infrastructure.migrations.scripts._types import (
    ColumnSchema,
    TableSchema,
)
from backend.src.infrastructure.models import Base


def get_model_definitions() -> list[TableSchema]:
    tables: list[TableSchema] = []
    for table in Base.metadata.sorted_tables:
        columns: list[ColumnSchema] = []
        for col in table.columns:
            columns.append({
                "name": col.name,
                "type": str(col.type),
                "nullable": bool(col.nullable),
                "primary_key": bool(col.primary_key),
                "comment": col.comment
            })
        tables.append({
            "name": table.name,
            "columns": columns,
            "comment": table.comment
        })
    return tables
