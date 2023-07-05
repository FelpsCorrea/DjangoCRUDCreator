from pydantic import BaseModel, validator

class ModelColumns(BaseModel):
    type: str
    length: int = None # Length opcional para CHAR ou VARCHAR
    pk: bool = False
    fk: bool = False
    not_null: bool = False
    unique: bool = False
    auto_increment: bool = False
    zero_fill: bool = False # Campos numéricos são preenchidos com zeros à esquerda até atingir a largura definida da coluna
    generated_column: bool = False # Campos gerados a partir de dados de outras colunas, ex: total DECIMAL(5,2) AS (quantidade * preco_por_item)
    default_expression: str = None # Valor default definido ou expressão referente a "generated_column", para colunas virtuais
