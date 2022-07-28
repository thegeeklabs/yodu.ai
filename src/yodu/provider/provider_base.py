from pydantic import BaseModel


class ProviderBase(BaseModel):
    def get_items(self, **kwargs):
        pass

    def init(self, **kwargs):
        pass
