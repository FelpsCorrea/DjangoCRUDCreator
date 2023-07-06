from pydantic import BaseModel
from typing import List

from references.db_ref import DBColumn, DBTable

class ModelColumn(DBColumn):

    def get_column_type_definition(self):

        if self.auto_increment:
            self.not_null = True
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
            return old_value + f", {value}"
    
    def get_django_model_row(self):
        
        # Tab e nome da coluna
        row_column = f"\t{self.name} = "

        # Definição da tipagem
        row_column += self.get_column_type_definition()

        # Caso seja PK
        if self.pk and not self.auto_increment:
            row_column = self.add_param(row_column, "primary_key=True")

        # Caso tenha default value
        if self.default != None:
            row_column = self.add_param(row_column, self.get_default_value())

        # Caso seja não obrigatório
        if not self.not_null:
            row_column = self.add_param(row_column, "null=True")

        # Caso seja unique
        if self.unique:
            row_column = self.add_param(row_column, "unique=True")

        return row_column+")"

class ModelTable(DBTable):
    columns: List[ModelColumn]

    def get_str_model(self):

        str_model = f"class {self.class_name}(SoftDeletionModel):\n"

        for column in self.columns:
            str_model += f"{column.get_django_model_row()}\n"

        str_model += f"\n\tclass Meta:\n\t\tdb_table='{self.table_name}'"

        return str_model