import strawberry
from flask import Flask
from modules.logger import logger
from strawberry.flask.views import GraphQLView
from constants.constants import SQLALCHEMY_DATABASE_URL
from models.models import db
from queries import Query
from mutations import Mutation

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL

db.init_app(app)

schema = strawberry.Schema(query=Query, mutation=Mutation)

if __name__== "__main__":
    logger.info("Starting app")
    app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql_view", schema=schema))
    app.run(debug=True)

