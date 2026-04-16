import pytest
from src.transform.transform_coin_cap import transform_coins, CoinCapSchema


class TestTransformCoins:
    """Tests for transform_coins function"""

    def test_transform_valid_coins(self):
        """Test successful transformation with valid data"""
        coins = [
            {
                "id": "bitcoin",
                "rank": 1,
                "symbol": "BTC",
                "name": "Bitcoin",
                "price_usd": 50000.00
            },
            {
                "id": "ethereum",
                "rank": 2,
                "symbol": "ETH",
                "name": "Ethereum",
                "price_usd": 3000.00
            }
        ]

        result = transform_coins(coins)

        assert len(result) == 2
        assert result[0]["id"] == "bitcoin"
        assert result[0]["rank"] == 1
        assert result[0]["price_usd"] == 50000.00

    def test_transform_skips_invalid_coin(self):
        """Test invalid coins are skipped"""
        coins = [
            {
                "id": "bitcoin",
                "rank": 1,
                "symbol": "BTC",
                "name": "Bitcoin",
                "price_usd": 50000.00
            },
            {
                "id": "invalid",
                "symbol": "INV",
                "name": "Invalid",
                "price_usd": 100.00
            }
        ]

        result = transform_coins(coins)

        assert len(result) == 1
        assert result[0]["id"] == "bitcoin"

    def test_transform_empty_list(self):
        """Test empty input returns empty list"""
        result = transform_coins([])
        assert result == []

    def test_transform_with_invalid_rank(self):
        """Test coins with non-numeric rank are skipped"""
        coins = [
            {
                "id": "bitcoin",
                "rank": "not_a_number",
                "symbol": "BTC",
                "name": "Bitcoin",
                "price_usd": 50000.00
            }
        ]

        result = transform_coins(coins)
        assert result == []


class TestCoinCapSchema:
    """Tests for Pydantic schema validation"""

    def test_valid_coin(self):
        """Test valid coin passes validation"""
        coin = {
            "id": "bitcoin",
            "rank": 1,
            "symbol": "BTC",
            "name": "Bitcoin",
            "price_usd": 50000.00
        }

        result = CoinCapSchema.model_validate(coin)

        assert result.id == "bitcoin"
        assert result.rank == 1
        assert result.price_usd == 50000.00

    def test_extra_fields_ignored(self):
        """Test extra fields are ignored due to config"""
        coin = {
            "id": "bitcoin",
            "rank": 1,
            "symbol": "BTC",
            "name": "Bitcoin",
            "price_usd": 50000.00,
            "extra_field": "should_be_ignored"
        }

        result = CoinCapSchema.model_validate(coin)
        assert result.id == "bitcoin"