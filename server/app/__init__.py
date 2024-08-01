from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('app.config.Config')

mongo = PyMongo(app)

# Import and register the blueprints after initializing 'mongo'
from .routes.examen_routes import examen_bp
from .routes.admin_routes import admin_bp

app.register_blueprint(examen_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
