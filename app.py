import strawberry
from flask import Flask
from modules.logger import logger
from strawberry.flask.views import GraphQLView
from constants.constants import SQLALCHEMY_DATABASE_URL, SUPER_SECRET_KEY
from models.models import db
from queries import Query
from mutations import Mutation
from flask_migrate import Migrate

from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL
app.config["JWT_SECRET_KEY"] = SUPER_SECRET_KEY
migrate = Migrate(app, db)

jwt = JWTManager(app)

db.init_app(app)

schema = strawberry.Schema(query=Query, mutation=Mutation)

if __name__== "__main__":
    logger.info("Starting app")
    app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql_view", schema=schema))
    app.run(debug=True)

