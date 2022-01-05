"Base Pydantic Schema"

from pydantic import BaseModel

class CamelModel(BaseModel):
     """
    Base model to auto create a camelCase alias. 
    Also allows popualtion of Pydantic model via alias
    """
