from sqlalchemy.schema import CreateTable
from database.models import Base, Component, SensorRecord, ClimateData
from database.oracle import db
import os


def generate_ddl(output_dir="generated"):
    """
    Gera os comandos SQL (DDL) para criar as tabelas baseadas nos models.
    Salva o resultado em um arquivo DDL.
    """
    os.makedirs(output_dir, exist_ok=True)
    ddl_path = os.path.join(output_dir, "schema.ddl")

    with open(ddl_path, "w", encoding="utf-8") as file:
        for table in Base.metadata.sorted_tables:
            ddl_statement = str(CreateTable(table).compile(db.engine))
            file.write(f"{ddl_statement};\n\n")

    print(f"Arquivo DDL gerado em: {ddl_path}")


def print_mer():
    """
    Exibe um MER simplificado no terminal baseado nos models e relacionamentos declarados.
    """
    print("\nModelo de Entidade-Relacionamento:\n")

    for table in Base.metadata.tables.values():
        print(f"Tabela: {table.name}")
        for column in table.columns:
            col_info = f"  - {column.name} ({column.type})"
            if column.primary_key:
                col_info += " [PK]"
            if column.foreign_keys:
                foreign_table = list(column.foreign_keys)[0].column.table.name
                col_info += f" [FK -> {foreign_table}]"
            print(col_info)
        print()


if __name__ == "__main__":
    generate_ddl()
    print_mer()