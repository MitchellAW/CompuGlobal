"""Test base model used for all API models."""

import pytest
from inline_snapshot import snapshot
from pydantic import Field, ValidationError

from compuglobal.models.base import BaseCompuGlobalModel


class ExampleModel(BaseCompuGlobalModel):
    """Test model for verifying inherited base model validation/serialization behaviour."""

    example: str = Field(alias="Example")
    value: int = Field(alias="Value")


def test_base_compuglobal_model_config() -> None:
    base = BaseCompuGlobalModel()
    assert base.model_config == snapshot(
        {
            "extra": "forbid",
            "validate_by_name": True,
            "validate_by_alias": True,
            "serialize_by_alias": True,
            "frozen": True,
        },
    )


def test_base_compuglobal_model_children_validate_missing_field() -> None:
    payload = {}
    with pytest.raises(ValidationError, match="Field required"):
        ExampleModel.model_validate(payload)


def test_base_compuglobal_model_children_validate_unexpected_field() -> None:
    payload = {"Example": "test", "Value": 3, "_UNEXPECTED_FIELD_": True}
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        ExampleModel.model_validate(payload)


def test_base_compuglobal_model_children_validate_incorrect_type() -> None:
    payload = {"Episode": "test", "Value": "invalid_value"}
    with pytest.raises(ValidationError, match="Input should be a valid integer"):
        ExampleModel.model_validate(payload)


def test_base_compuglobal_model_children_serialize_aliases() -> None:
    example = ExampleModel(example="Test", value=123)
    dump = example.model_dump()

    assert dump == snapshot(
        {
            "Example": "Test",
            "Value": 123,
        },
    )
