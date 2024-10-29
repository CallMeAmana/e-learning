from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS



app = Flask(__name__)
app.config.from_object('app.config.Config')
CORS(app)
mongo = PyMongo(app)

# Import and register the blueprints after initializing 'mongo'
from .routes.examen_routes import examen_bp
from .routes.admin_routes import admin_bp
from .routes.users_routes import users_bp

app.register_blueprint(examen_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(users_bp, url_prefix='/api') 

if __name__ == '__main__':
    app.run(debug=True)
