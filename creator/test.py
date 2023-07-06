import pymysql
import mysql.connector as mysql

from references.models import ModelColumn

# con = pymysql.connect(host='11.11.11.21', port='3306', user='felipe_santos', passwd='Teste@123', db='jota', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

classe = ModelColumn(
    name="abacate",
    type="varchar",
    max_length=255
)
print(classe.get_django_model_row())
print(classe.get_django_model_row()[-1])
