import pymysql
import mysql.connector as mysql
from references.db_ref import DBColumn

from references.models import ModelColumn, ModelTable

# con = pymysql.connect(host='11.11.11.21', port='3306', user='felipe_santos', passwd='Teste@123', db='jota', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

column = ModelColumn(
    name="nome",
    type="varchar",
    max_length=255
)

column2 = ModelColumn(
    name="id",
    type="int",
    pk=True,
    max_length=11,
    auto_increment=True
)

column3 = ModelColumn(
    name="tipo_pessoa_id",
    type="int",
    fk=True,
    fk_table_name="tipo_pessoa"
)

model = ModelTable(
    table_name="pedidos_usuario",
    columns=[column, column2, column3]
)

print(model.get_str_model())