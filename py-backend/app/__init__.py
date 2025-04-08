from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','5f8c71b4370f4c8d8f28a9ec27d94b61')

    CORS(app,supports_credentials=True,origins=["https://localhost:5173"])

    db.init_app(app)
    migrate.init_app(app,db)

    #routes Registration
    from app.routes.user_routes import user_bp
    # from app.routes.company_routes import company_bp
    # from app.routes.job_routes import job_bp
    # from app.routes.application_routes import application_bp

    app.register_blueprint(user_bp,url_prefix="/api/v1/user")
    # app.register_blueprint(company_bp,url_prefix="/api/v1/company")
    # app.register_blueprint(job_bp,url_prefix="/api/v1/job")
    # app.register_blueprint(application_bp,url_prefix="/api/v1/application")

    @app.route("/")
    def index():
        return jsonify({"message":"flask API is running"}), 200
    
    return app