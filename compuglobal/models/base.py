"""Contains base model used for all API models."""

from pydantic import BaseModel, ConfigDict


class BaseCompuGlobalModel(BaseModel, frozen=True):
    """Base model class used for all API models.

    .. code-block:: python

        model_config = ConfigDict(
            extra="forbid",
            frozen=True,
            serialize_by_alias=True,
            validate_by_alias=True,
            validate_by_name=True,
        )
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_by_name=True,
        validate_by_alias=True,
        serialize_by_alias=True,
    )
