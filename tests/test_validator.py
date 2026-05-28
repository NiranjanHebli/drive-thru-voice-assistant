import pytest
from unittest.mock import patch, mock_open
from app.core.validator import OrderValidator
import json

MOCK_MENU = {
    "categories": [
        {"id": "c1", "name": "Breakfast", "availability": "breakfast"},
        {"id": "c2", "name": "Burgers", "availability": "all_day"},
    ],
    "items": [
        {"id": "i1", "name": "Hash Browns", "category_id": "c1", "base_price": 50},
        {
            "id": "i2",
            "name": "Maharaja Mac",
            "category_id": "c2",
            "base_price": 150,
            "modifier_group_ids": ["mg1"],
        },
    ],
}


@pytest.fixture
def validator():
    with patch("builtins.open", mock_open(read_data=json.dumps(MOCK_MENU))):
        v = OrderValidator(menu_path="dummy.json")
        return v


def test_valid_item_all_day(validator):
    result = validator.validate_add_to_cart("i2")
    assert result["valid"] is True
    assert result["item_name"] == "Maharaja Mac"


def test_invalid_item(validator):
    result = validator.validate_add_to_cart("i999")
    assert result["valid"] is False
    assert result["reason"] == "item_not_found"


@patch.object(OrderValidator, "_is_breakfast_time")
def test_breakfast_item_during_breakfast(mock_is_breakfast, validator):
    mock_is_breakfast.return_value = True
    result = validator.validate_add_to_cart("i1")
    assert result["valid"] is True


@patch.object(OrderValidator, "_is_breakfast_time")
def test_breakfast_item_outside_breakfast(mock_is_breakfast, validator):
    mock_is_breakfast.return_value = False
    result = validator.validate_add_to_cart("i1")
    assert result["valid"] is False
    assert result["reason"] == "out_of_hours"
