`INTEGER`: Usado para números inteiros. O intervalo de valores depende do sistema de gerenciamento de banco de dados específico.

`SMALLINT`: Um tipo de dados numérico que pode ser usado para números menores para economizar espaço.

`BIGINT`: Usado para números inteiros muito grandes.

`DECIMAL ou NUMERIC`: Usado para números precisos, onde você pode especificar o número total de dígitos e o número de dígitos após o ponto decimal.

`FLOAT ou REAL`: Usado para números de ponto flutuante.

`CHAR(n)`: Uma string de caracteres fixa de comprimento 'n'.

`VARCHAR(n)`: Uma string de caracteres variável de comprimento máximo 'n'.

`TEXT`: Para strings de texto longas.

`DATE`: Para datas.

`TIME`: Para tempo.

`DATETIME ou TIMESTAMP`: Para data e hora.

`BOOLEAN ou BIT`: Para valores verdadeiro/falso.

`BLOB ou BYTEA`: Para dados binários, como imagens, áudio, etc.

`TINYINT`: É um tipo de dados numérico usado para números inteiros muito pequenos. Em sistemas como MySQL, ele tem um alcance de -128 a 127 para TINYINT assinado, e de 0 a 255 para TINYINT não assinado.

'''
SELECT * 
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'jota'
AND TABLE_NAME = 'abacate';

SELECT 
  C.*,
  K.REFERENCED_TABLE_NAME as FK_REFERENCED_TABLE
FROM 
  INFORMATION_SCHEMA.COLUMNS as C
LEFT JOIN 
  INFORMATION_SCHEMA.KEY_COLUMN_USAGE as K
ON 
  C.TABLE_NAME = K.TABLE_NAME 
  AND C.COLUMN_NAME = K.COLUMN_NAME
  AND C.TABLE_SCHEMA = K.TABLE_SCHEMA
WHERE 
  C.TABLE_SCHEMA = 'jota'
  AND C.TABLE_NAME = 'abacate';

INTEGER: models.IntegerField()
SMALLINT: models.SmallIntegerField()
BIGINT: models.BigIntegerField()
DECIMAL ou NUMERIC: models.DecimalField(max_digits=_, decimal_places=_) - você precisa especificar max_digits (o número total de dígitos) e decimal_places (o número de dígitos após o ponto decimal).
FLOAT ou REAL: models.FloatField()
CHAR(n): models.CharField(max_length=_) - você precisa especificar max_length.
VARCHAR(n): models.CharField(max_length=_) - você precisa especificar max_length.
TEXT: models.TextField()
DATE: models.DateField()
TIME: models.TimeField()
DATETIME ou TIMESTAMP: models.DateTimeField()
BOOLEAN ou BIT: models.BooleanField()
BLOB ou BYTEA: models.BinaryField()
TINYINT: Django não tem um campo específico para TINYINT, mas você pode usar models.IntegerField() e garantir que o valor esteja dentro do alcance de um TINYINT.
MEDIUMINT: Django também não tem um campo específico para MEDIUMINT, mas você pode usar models.IntegerField().
DOUBLE PRECISION: models.FloatField()
ENUM: Django não tem suporte nativo para ENUM, mas você pode imitar o comportamento de um ENUM usando models.CharField() e a opção choices.
SET: Django não tem suporte nativo para o tipo SET, mas você pode conseguir algo similar usando models.ManyToManyField().
JSON: models.JSONField()
UUID: models.UUIDField()
ARRAY: Django não tem suporte nativo para o tipo ARRAY, mas alguns pacotes de terceiros (como django-postgres-extra) fornecem esse tipo de campo.
GEOMETRY, POINT, LINE, POLYGON, etc.: Django tem suporte a campos geoespaciais através de seu módulo GIS. Consulte a documentação do Django para mais informações.
INTERVAL: Django não tem suporte nativo para INTERVAL, mas você pode usar models.DurationField() para armazenar durações de tempo que podem servir a um propósito similar.
CIDR, INET, MACADDR: Django tem models.GenericIPAddressField() para endereços IP, mas não tem suporte nativo para CIDR ou MACADDR.
Lembre-se, a implementação exata e a disponibilidade desses campos podem variar dependendo da versão do Django e do banco de dados backend que você está usando. Consulte a documentação do Django para obter as informações mais atualizadas.
'''