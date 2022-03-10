# Proy Flask Televisores

### Dependencies
* [Flask](https://flask.palletsprojects.com/) - The framework used
* [Autopep8](https://pypi.org/project/autopep8/) - The formatter
* [Flask-MySQLdb](https://flask-mysqldb.readthedocs.io/en/latest/) - MySQL connection for Flask
* [PyMySQL](https://pypi.org/project/PyMySQL/) - Interaction with MySQL databases
* [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) - Validation and serialization
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - ORM

Install all project dependencies using:

```
$ pip install -r requirements.txt
```

### Running

```
python .\code\app.py
```

### Note
El sistema de gestión de bases de datos relacional que se usa es MySQL. La configuracion para la conexion con la base de datos esta en 'configs/default_config.py' en modo desarrollo y para modo produccion en 'configs/config.py'.
