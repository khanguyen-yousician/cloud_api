from flask import Flask
from apps.api import api as api_blueprint
from packages.cache import cache

app = Flask(__name__)
app.register_blueprint(api_blueprint)

cache.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
