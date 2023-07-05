# Os values representam os parametros na ordem que são recebidos.
def django_model_type_definition(type, value=None, value2=None):
    
    if type == "int" or type == "mediumint":
        if value is not None:
            f"models.SmallIntegerField(max_digits={value}"
        else:
            return "models.IntegerField("
    
    elif type == "varchar" or type == "char":
        if value is not None:
            return f"models.CharField(max_length={value}"
        else:
            return "models.CharField("
        
    elif type == "smallint":
        if value is not None:
            return f"models.SmallIntegerField(max_digits={value}"
        else:
            return "models.SmallIntegerField("
        
    elif type == "bigint":
        if value is not None:
            return f"models.BigIntegerField(max_digits={value}"
        else:
            return "models.BigIntegerField("
        
    elif type == "decimal":
        if value is not None and value2 is not None:
            return f"models.DecimalField(max_digits={value}, decimal_places={value2}"
        else:
            return "models.DecimalField("
        
    elif type == "float" or type == "double":
        return "models.FloatField("
    
    elif type == "text" or type == "long_text":
        return "models.TextField("
    
    elif type == "date":
        return "models.DateField("
    
    elif type == "time":
        return "models.TimeField("
    
    elif type == "datetime" or type == "timestamp":
        return "models.DateTimeField("
    
    elif type == "tinyint":
        return "models.BooleanField("
    
    elif type == "blob":
        return "models.BinaryField("
    
