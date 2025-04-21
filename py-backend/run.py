from app import create_app
from dotenv import load_dotenv
import os
from flask import Flask
import app.routes.user_routes as user_routes

load_dotenv()

app = create_app()

if __name__ =='__main__':
    port = int(os.getenv("PORT",3000))
    app.run(host="0.0.0.0",port=port,debug=True)


