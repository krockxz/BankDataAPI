from flask import Flask
from flask_graphql import GraphQLView
import logging

from models import db_session
from schema import schema

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.debug = True

# Adding GraphQL endpoint
app.add_url_rule(
    '/gql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Enable GraphiQL interface
    )
)

@app.route('/')
def home():
    logger.info("Home route accessed")
    return (
        "<br/>"
        "<h2>Append '/gql' at the end of this URL to visit the GraphQL interface</h2>"
    )

@app.teardown_appcontext
def shutdown_session(exception=None):
    logger.info("Session shutdown")
    db_session.remove()

if __name__ == '__main__':
    logger.info("Starting the Flask app")
    app.run()
