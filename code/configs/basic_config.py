from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash

auth = HTTPBasicAuth()
users = {
    "angular_app_televisores": generate_password_hash("264dd4ae1ea6476cb21eb52b2ae4f54d")
    # "susan": generate_password_hash("bye")
}
