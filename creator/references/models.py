from pydantic import BaseModel, validator, ValidationError

class ModelColumn(BaseModel):
    name: str
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

    # Caso o tipo seja VARCHAR ou CHAR, o length deve ser informado
    @validator('length')
    def validate_length(cls, v, values, **kwargs):
        if 'type' in values and (values['type'] == 'varchar' or values['type'] == 'char' or values['type'] == 'int' or values['type'] == 'char') and v is None:
            raise ValidationError('The length cannot be None for type "varchar" or "char".')
        return v

    # Caso seja uma coluna virtual, a expressão deve ser informada
    @validator('default_expression')
    def validate_default_expression(cls, v, values, **kwargs):
        if 'generated_column' in values and values['generated_column'] == True and v is None:
            raise ValidationError('Default expression must be provided when generated_column is True.')
        return v
