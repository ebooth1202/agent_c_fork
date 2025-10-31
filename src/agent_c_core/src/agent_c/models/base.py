from pydantic import BaseModel as BM, ConfigDict

class BaseModel(BM):
    model_config = ConfigDict(populate_by_name=True, extra="ignore", protected_namespaces=(), arbitrary_types_allowed=True)


