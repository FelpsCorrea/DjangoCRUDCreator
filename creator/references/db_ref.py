from pydantic import BaseModel, validator, ValidationError
from typing import List, Optional

class DBColumn(BaseModel):
    name: str
    type: str
    max_length: int = None # Length opcional para CHAR ou VARCHAR
    pk: bool = False
    fk: bool = False
    not_null: bool = False
    unique: bool = False
    auto_increment: bool = False
    default: str = None # Valor default definido
    decimal_places: str = None # Caso seja DECIMAL
    fk_table_name: str = None # Nome da classe para referenciar a FK
    fk_class_name: Optional[str] = None # Valor Inicial


    # Caso o tipo seja VARCHAR ou CHAR, o length deve ser informado
    @validator('max_length')
    def validate_length(cls, v, values, **kwargs):
        if 'type' in values and (values['type'] == 'varchar' or values['type'] == 'char' or values['type'] == 'int' or values['type'] == 'char') and v is None:
            raise ValidationError('The max_length cannot be None for type "varchar" or "char".')
        return v

    # Caso seja uma coluna virtual, a expressão deve ser informada
    @validator('default')
    def validate_default(cls, v, values, **kwargs):
        if 'generated_column' in values and values['generated_column'] == True and v is None:
            raise ValidationError('Default expression must be provided when generated_column is True.')
        return v
    
    # Caso seja uma coluna virtual, a expressão deve ser informada
    @validator('fk_table_name')
    def validate_fk_table_name(cls, v, values, **kwargs):
        if 'fk' in values and values['fk'] == True and v is None:
            raise ValidationError('FK table name must be provided when fk is True.')
        return v
    
    # Gera o nome da tabela da FK a partir do nome da tabela
    @validator('fk_class_name', always=True)
    def generate_class_name(cls, v, values):
        if "fk_table_name" in values and values['fk_table_name'] is not None:
            return "".join(word.capitalize() for word in values['fk_table_name'].split('_')) # Transforma em CamelCase
        return v
    
    # Ajusta o nome da coluna caso seja FK
    @validator('name', always=True)
    def adjust_name(cls, v, values):
        if "fk" in values and values['fk']:
            return v.replace("_id", "").replace("id_", "")
        return v

class DBTable(BaseModel):
    table_name: str
    class_name: Optional[str] = None # Valor Inicial

    @validator('class_name', always=True)
    def generate_class_name(cls, v, values):
        if 'table_name' in values:  # Verifica se table_name está disponível
            return "".join(word.capitalize() for word in values['table_name'].split('_')) # Transforma em CamelCase
        return v  # Caso contrário, retornar o valor atual
