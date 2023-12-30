from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:19112002@localhost/saleDB?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 4


db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name='dd3180gc5',
    api_key='238456219259574',
    api_secret='PbhBM7Y8F6UaWx8CYmmlpSUZqn4'
)

login = LoginManager(app=app)
