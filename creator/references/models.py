from pydantic import BaseModel
from typing import List

from references.db_column import DBColumn

class ModelColumn(BaseModel):

    column: DBColumn

    def get_column_type_definition(self):

        if self.column.auto_increment:
            return "models.AutoField(primary_key=True"
        
        elif self.column.fk:
            return f"models.ForeignKey({self.column.fk_class_name}, on_delete=models.CASCADE"

        
        elif self.column.type == "int" or self.column.type == "mediumint":
            if self.column.max_length is not None:
                return f"models.IntegerField(max_value={self.column.max_length}"
            else:
                return "models.IntegerField("
        
        elif self.column.type == "varchar" or self.column.type == "char":
            if self.column.max_length is not None:
                return f"models.CharField(max_length={self.column.max_length}"
            else:
                return "models.CharField("
            
        elif self.column.type == "smallint":
            if self.column.max_length is not None:
                return f"models.SmallIntegerField(max_value={self.column.max_length}"
            else:
                return "models.SmallIntegerField("
            
        elif self.column.type == "bigint":
            if self.column.max_length is not None:
                return f"models.BigIntegerField(max_value={self.column.max_length}"
            else:
                return "models.BigIntegerField("
            
        elif self.column.type == "decimal":
            if self.column.max_length is not None and self.column.decimal_places is not None:
                return f"models.DecimalField(max_digits={self.column.max_length}, decimal_places={self.column.decimal_places}"
            else:
                return "models.DecimalField("
            
        elif self.column.type == "float" or self.column.type == "double":
            return "models.FloatField("
        
        elif self.column.type == "text" or self.column.type == "long_text":
            return "models.TextField("
        
        elif self.column.type == "date":
            return "models.DateField("
        
        elif self.column.type == "time":
            return "models.TimeField("
        
        elif self.column.type == "datetime" or self.column.type == "timestamp":
            return "models.DateTimeField("
        
        elif self.column.type == "tinyint":
            return "models.BooleanField("
        
        elif self.column.type == "blob":
            return "models.BinaryField("
        
    def get_default_value(self):

        if self.column.type in ["datetime", "date", "time"]:

            if self.column.default == "CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()":
                return "auto_now=True"
            
            elif self.column.default == "CURRENT_TIMESTAMP()":
                return "auto_now_add=True"
            
        if self.column.default == "''":
            return "blank=True"
            
        return f"default={self.column.default}"
    
    def add_param(self, old_value:str, value:str):

        if old_value[-1] != "(":
            return old_value + f",{value}"
    
    def get_django_model_row(self):
        
        # Tab e nome da coluna
        row_column = f"\t{self.column.name} = "

        # Definição da tipagem
        row_column += self.get_column_type_definition()

        # Caso seja PK
        if self.column.pk:
            row_column = self.add_param(row_column, "primary_key=True")

        # Caso tenha default value
        if self.column.default != None:
            row_column = self.add_param(row_column, self.get_default_value())

        # Caso seja não obrigatório
        if not self.column.not_null:
            row_column = self.add_param(row_column, "null=True")

        # Caso seja unique
        if self.column.unique:
            row_column = self.add_param(row_column, "unique=True")

        return row_column

class ModelDjango(BaseModel):
    class_name: str
    columns: List[ModelColumn]