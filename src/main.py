from flask import Flask

from config import CONFIG
from common import Register

app = Flask(__name__)
Register.register_cors(app)
Register.register_db(app)
Register.register_db_data_init(app)
Register.register_scheduler(app)
Register.register_exception(app)
Register.register_auth(app)
Register.register_controller(app)
Register.register_static_controller(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=CONFIG["APP"]["PORT"], debug=True)
