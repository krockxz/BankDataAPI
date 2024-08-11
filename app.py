from flask import Flask, jsonify, request
from ariadne import QueryType, make_executable_schema, graphql_sync, gql
from models import db_session, Banks as BankModel, Branches as BranchModel

app = Flask(__name__)

# Define your GraphQL schema
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

# Create a resolver for branches
query = QueryType()

@query.field("branches")
def resolve_branches(_, info):
    branches = db_session.query(BranchModel).all()
    edges = [{"node": {
        "ifsc": branch.ifsc,
        "bank": {
            "id": branch.bank.id,
            "name": branch.bank.name,
        },
        "branch": branch.branch,
        "address": branch.address,
        "city": branch.city,
        "district": branch.district,
        "state": branch.state,
    }} for branch in branches]
    return {"edges": edges}

# Create an executable schema
schema = make_executable_schema(type_defs, query)

# Manually define the GraphQL Playground HTML
PLAYGROUND_HTML = '''
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
    <div id="root"></div>
    <script type="text/javascript">
        window.addEventListener('load', function (event) {
            GraphQLPlayground.init(document.getElementById('root'), { endpoint: '/gql' })
        })
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return "<h1>Welcome to the Bank Branch API</h1><p>Visit <a href='/gql'>/gql</a> for the GraphQL Playground.</p>"

@app.route("/gql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

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

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()
