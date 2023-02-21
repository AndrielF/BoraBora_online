from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'senha123'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}:{port}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='Fv3jlXAeIcXP7L42wYIu',
        servidor='containers-us-west-110.railway.app',
        port='6309',
        database='railway'
)
db = SQLAlchemy(app)


from app import routes
