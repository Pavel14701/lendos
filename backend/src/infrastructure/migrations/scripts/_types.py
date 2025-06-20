from typing import TypedDict

class ColumnSchema(TypedDict):
    name: str
    type: str
    nullable: bool
    primary_key: bool
    comment: str | None


class TableSchema(TypedDict):
    name: str
    columns: list[ColumnSchema]
    comment: str | None
