from backend.src.infrastructure.migrations.scripts._types import TableSchema


def render_upgrade_downgrade(models: list[TableSchema]) -> tuple[str, str]:
    upgrade: list[str] = []
    downgrade: list[str] = []
    for model in models:
        table_name = model["name"]
        upgrade.append(f'op.create_table("{table_name}",')
        for col in model["columns"]:
            col_name = col["name"]
            col_type = col["type"]
            nullable = col["nullable"]
            primary_key = col["primary_key"]
            upgrade.append(
                f'    sa.Column("{col_name}", sa.{col_type}, '
                f'nullable={nullable}, primary_key={primary_key}),'
            )
        upgrade.append(")\n")
        downgrade.append(f'op.drop_table("{table_name}")')
    return "\n".join(upgrade), "\n".join(downgrade)
