from pydantic import BaseModel, validator, ValidationError
from typing import List

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
    fk_class_name: str = None # Nome da classe para referenciar a FK


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
    @validator('fk_class_name')
    def validate_fk_class_name(cls, v, values, **kwargs):
        if 'fk' in values and values['fk'] == True and v is None:
            raise ValidationError('FK class name must be provided when fk is True.')
        return v
    
    # Inicializador
    def __post_init__(self):
        if self.fk:
            self.name.replace("_id", "").replace("id_", "")