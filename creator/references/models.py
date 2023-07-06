from pydantic import BaseModel, validator, ValidationError
from typing import List

class ModelColumn(BaseModel):
    name: str
    type: str
    max_length: int = None # Length opcional para CHAR ou VARCHAR
    pk: bool = False
    fk: bool = False
    not_null: bool = False
    unique: bool = False
    auto_increment: bool = False
    zero_fill: bool = False # Campos numéricos são preenchidos com zeros à esquerda até atingir a largura definida da coluna
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
    
    def get_column_type_definition(self):

        if self.auto_increment:
            return "models.AutoField(primary_key=True"
        
        elif self.fk:
            return f"models.ForeignKey({self.fk_class_name}, on_delete=models.CASCADE"

        
        elif self.type == "int" or self.type == "mediumint":
            if self.max_length is not None:
                return f"models.IntegerField(max_value={self.max_length}"
            else:
                return "models.IntegerField("
        
        elif self.type == "varchar" or self.type == "char":
            if self.max_length is not None:
                return f"models.CharField(max_length={self.max_length}"
            else:
                return "models.CharField("
            
        elif self.type == "smallint":
            if self.max_length is not None:
                return f"models.SmallIntegerField(max_value={self.max_length}"
            else:
                return "models.SmallIntegerField("
            
        elif self.type == "bigint":
            if self.max_length is not None:
                return f"models.BigIntegerField(max_value={self.max_length}"
            else:
                return "models.BigIntegerField("
            
        elif self.type == "decimal":
            if self.max_length is not None and self.decimal_places is not None:
                return f"models.DecimalField(max_digits={self.max_length}, decimal_places={self.decimal_places}"
            else:
                return "models.DecimalField("
            
        elif self.type == "float" or self.type == "double":
            return "models.FloatField("
        
        elif self.type == "text" or self.type == "long_text":
            return "models.TextField("
        
        elif self.type == "date":
            return "models.DateField("
        
        elif self.type == "time":
            return "models.TimeField("
        
        elif self.type == "datetime" or self.type == "timestamp":
            return "models.DateTimeField("
        
        elif self.type == "tinyint":
            return "models.BooleanField("
        
        elif self.type == "blob":
            return "models.BinaryField("
        
    def get_default_value(self):

        if self.type in ["datetime", "date", "time"]:

            if self.default == "CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()":
                return "auto_now=True"
            
            elif self.default == "CURRENT_TIMESTAMP()":
                return "auto_now_add=True"
            
        if self.default == "''":
            return "blank=True"
            
        return f"default={self.default}"
    
    def add_param(self, old_value:str, value:str):

        if old_value[-1] != "(":
            return old_value + f",{value}"
    
    def get_django_model_row(self):
        
        # Tab e nome da coluna
        row_column = f"\t{self.name} = "

        # Definição da tipagem
        row_column += self.get_column_type_definition()

        # Caso seja PK
        if self.pk:
            row_column = self.add_param(row_column, "primary_key=True")

        # Caso tenha default value
        if self.default != None:
            row_column = self.add_param(row_column, self.get_default_value())

        # Caso seja não obrigatório
        if not self.not_null:
            row_column = self.add_param(row_column, "null=True")

        return row_column

class ModelDjango(BaseModel):
    class_name: str
    columns: List[ModelColumn]
