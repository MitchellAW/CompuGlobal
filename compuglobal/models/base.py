from pydantic import BaseModel, PrivateAttr, ValidationInfo, model_validator

from ..core import BaseCompuGlobalAPI


class BaseCompuGlobalModel(BaseModel):
    _api: BaseCompuGlobalAPI = PrivateAttr()

    @model_validator(mode="after")
    def attach_api(self, info: ValidationInfo):
        if info.context is not None and "_api" in info.context:
            self._api = info.context.get("_api")
        return self
