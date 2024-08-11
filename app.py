from flask import Flask, jsonify, request
from ariadne import QueryType, make_executable_schema, graphql_sync, gql
from models import db_session, Banks as BankModel, Branches as BranchModel

app = Flask(__name__)

type_defs = gql("""
    type Query {
        branches: BranchConnection!
    }

    type BranchConnection {
        edges: [BranchEdge!]!
    }

    type BranchEdge {
        node: Branch!
    }

    type Branch {
        ifsc: String!
        bank: Bank!
        branch: String
        address: String!
        city: String!
        district: String!
        state: String!
    }

    type Bank {
        id: ID!
        name: String!
    }
""")

query = QueryType()

@query.field("branches")
def resolve_branches(_, info):
    branches = db_session.query(BranchModel).all()
    edges = [{"node": branch} for branch in branches]
    return {"edges": edges}

schema = make_executable_schema(type_defs, query)

@app.route("/gql", methods=["GET"])
def graphql_playground():
    playground_html = '''
    <!DOCTYPE html>
    <html>

    <head>
        <meta charset=utf-8/>
        <title>GraphQL Playground</title>
        <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css"/>
        <link rel="shortcut icon" href="//cdn.jsdelivr.net/npm/graphql-playground-react/build/favicon.png"/>
        <script src="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js"></script>
    </head>

    <body>
        <div id="root"/>
        <script>window.addEventListener('load', function (event) { GraphQLPlayground.init(document.getElementById('root'), { endpoint: '/gql' }) })</script>
    </body>

    </html>
    '''
    return playground_html, 200

@app.route("/gql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run()
