from pydantic import BaseModel


class ListAgentsQuery(BaseModel):
    skip: int = 0
    limit: int = 100
