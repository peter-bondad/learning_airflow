import pytest
from unittest.mock import patch, MagicMock


class TestFetchCoins:
    """Tests for fetch_coins function"""

    @patch("src.extract.extract_coin_cap.requests.get")
    def test_fetch_coins_success(self, mock_get, monkeypatch):
        """Test successful API fetch"""
        monkeypatch.setenv("COINCAP_API_KEY", "test_key")
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "bitcoin",
                    "rank": 1,
                    "symbol": "BTC",
                    "name": "Bitcoin",
                    "priceUsd": 50000.00
                },
                {
                    "id": "ethereum",
                    "rank": 2,
                    "symbol": "ETH",
                    "name": "Ethereum",
                    "priceUsd": 3000.00
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from src.extract.extract_coin_cap import fetch_coins
        result = fetch_coins(limit=2)

        assert len(result) == 2
        assert result[0]["id"] == "bitcoin"
        mock_get.assert_called_once()

    @patch("src.extract.extract_coin_cap.requests.get")
    def test_fetch_coins_empty_response(self, mock_get, monkeypatch):
        """Test empty API response"""
        monkeypatch.setenv("COINCAP_API_KEY", "test_key")
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from src.extract.extract_coin_cap import fetch_coins
        result = fetch_coins()

        assert result == []

    @patch("src.extract.extract_coin_cap.requests.get")
    def test_fetch_coins_skips_missing_fields(self, mock_get, monkeypatch):
        """Test coins with missing required fields are skipped"""
        monkeypatch.setenv("COINCAP_API_KEY", "test_key")
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "bitcoin",
                    "rank": 1,
                    "symbol": "BTC",
                    "name": "Bitcoin",
                    "priceUsd": 50000.00
                },
                {
                    "id": "incomplete",
                    "name": "Incomplete",
                    "priceUsd": 100.00
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        from src.extract.extract_coin_cap import fetch_coins
        result = fetch_coins()

        assert len(result) == 1
        assert result[0]["id"] == "bitcoin"

    @patch("src.extract.extract_coin_cap.requests.get")
    def test_fetch_coins_api_error(self, mock_get, monkeypatch):
        """Test API error raises exception"""
        monkeypatch.setenv("COINCAP_API_KEY", "test_key")
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response

        from src.extract.extract_coin_cap import fetch_coins

        with pytest.raises(Exception):
            fetch_coins()