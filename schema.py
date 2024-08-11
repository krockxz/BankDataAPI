# flask_sqlalchemy/schema.py
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Banks as BankModel, Branches as BranchModel

class Banks(SQLAlchemyObjectType):
    class Meta:
        model = BankModel
        interfaces = (relay.Node, )

class Branches(SQLAlchemyObjectType):
    class Meta:
        model = BranchModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    branches = SQLAlchemyConnectionField(Branches.connection)
    all_banks = SQLAlchemyConnectionField(Banks.connection, sort=None)

schema = graphene.Schema(query=Query)
