from flask import Flask
from conexion_bd_mysql import db
from configs import default_config

# Importar los controladores
from controllers.cliente_rest_controller import cliente_controller
from controllers.multimedia_rest_controller import multimedia_controller
# from controllers.image_rest_controller import image_controller

app = Flask(__name__)
app.config.from_object(default_config)


@app.before_first_request
def create_tables():
    db.create_all()


# Controllers
app.register_blueprint(cliente_controller, url_prefix='/cliente')
app.register_blueprint(multimedia_controller, url_prefix='/multimedia')
# app.register_blueprint(image_controller, url_prefix='/imagen')


if __name__ == '__main__':
    db.init_app(app)
    app.run()
