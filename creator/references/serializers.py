from typing import List

from references.db_ref import DBColumn, DBTable

class SerializerValidation(DBColumn):

    def get_validation(self, method:str):
        
        string = f"{self.name} = "
        
        ###################### FK
        if self.fk:
            string = f"serializers.PrimaryKeyRelatedField(\n"
            string += f"\tqueryset={self.fk_class_name}.objects.filter(ativo=True),\n"
            string+= f"\tsource='{self.fk_table_name}'"
        
        ###################### Int / BigInt / MediumInt / SmallInt
        elif self.type in  ["int", "mediumint", "bigint", "smallint"]:
            
            string = f"serializers.IntegerField("
            
            if self.max_length is not None:
                string += f"\n\tmax_value={self.max_length}"
        
        ###################### Varchar / Char / Text / LongText / Blob
        elif self.type in ["varchar", "char", "text", "long_text", "blob"]:
            
            string = "serializers.CharField("
                       
            if self.max_length is not None:
                string += f"\n\tmax_length={self.max_length}"
        
        ###################### Decimal
        elif self.type == "decimal":
            
            string = "serializers.DecimalField("
            
            if self.max_length is not None:
                string += f"\n\tmax_digits={self.max_length}"
            
            if self.decimal_places is not None:
                if string[-1] != "(":
                    string += ","
                
                string += f"\n\tmax_decimal_places={self.decimal_places}"
        
        ###################### Float / Double  
        elif self.type in ["float", "double"]:
            string = "serializers.FloatField("
        
        ###################### Date
        elif self.type == "date":
            string = "serializers.DateField("
        
        ###################### Time
        elif self.type == "time":
            string = "serializers.TimeField("
        
        ###################### Datetime / TimeStamp
        elif self.type in ["datetime", "timestamp"]:
            string = "serializers.DateTimeField("
        
        ###################### Boolean
        elif self.type == "tinyint":
            string = "serializers.BooleanField("
            
        else:
            return ""
        
        ###################### Validação para not null
        if method == "POST" and self.not_null:
            string = self.add_validation(string, "required=True")
            
        if string[-1] != "(":
            string += "\n"
        
        string += ")"
        
        return string
        
    
    def add_validation(self, old_value:str, value:str):

        if old_value[-1] != "(":
            return old_value + f",\n\t{value}"
        
    def get_value(self):
        
        # Caso seja PK, retorna o serializer referente
        if self.pk:
            return f"\t{self.name} = {self.fk_class_name}(many=True)"
        
        return ""

class SerializerClass(DBTable):
    validations: List[SerializerValidation]

    def get_str_model(self):

        str_model = f"class {self.class_name}(SoftDeletionModel):\n"

        for column in self.columns:
            str_model += f"{column.get_django_model_row()}\n"

        str_model += f"\n\tclass Meta:\n\t\tdb_table='{self.table_name}'"

        return str_model