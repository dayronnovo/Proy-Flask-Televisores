from datetime import timedelta
from functools import wraps
from flask import Flask, jsonify
from conexion_bd_mysql import db
from configs import default_config
from flask_jwt_extended import JWTManager

# Importar los controladores
from controllers.cliente_rest_controller import cliente_controller
from controllers.multimedia_rest_controller import multimedia_controller
from controllers.televisor_rest_controller import televisor_controller
from controllers.historial_de_programacion_rest_controller import historial_de_programacion_controller
from controllers.login_rest_controller import login_controller
from configs.jwt_config import JwtConfig

app = Flask(__name__)
app.config.from_object(default_config)


# Configuraciones del Flask_JWT_Extended
app.config['JWT_ALGORITHM'] = 'RS256'
app.config['JWT_PRIVATE_KEY'] = JwtConfig.RSA_PRIVADA
app.config['JWT_PUBLIC_KEY'] = JwtConfig.RSA_PUBLICA
app.config['JWT_TOKEN_LOCATION'] = "headers"
# app.secret_key = JwtConfig.LLAVE_SECRETA
# app.config['JWT_SECRET_KEY'] = JwtConfig.LLAVE_SECRETA
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=2)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=6)

jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


# Trabajando con CORS
@app.after_request
def after_request(response):
    # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response


# Controllers
app.register_blueprint(cliente_controller, url_prefix='/cliente')
app.register_blueprint(multimedia_controller, url_prefix='/multimedia')
app.register_blueprint(televisor_controller, url_prefix='/televisor')
app.register_blueprint(
    historial_de_programacion_controller, url_prefix='/historial')
app.register_blueprint(
    login_controller, url_prefix='/login')


if __name__ == '__main__':
    db.init_app(app)
    app.run()
