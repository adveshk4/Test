import strawberry
from core.schema import Query as CoreQuery, Mutation as CoreMutation
schema = strawberry.Schema(query=CoreQuery, mutation=CoreMutation)