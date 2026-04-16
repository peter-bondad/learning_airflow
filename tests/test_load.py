import pytest
from unittest.mock import MagicMock, patch


class TestInsertCoins:

    @patch("src.load.load_coin_cap.execute_values")
    def test_insert_coins_success(self, mock_execute_values):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        from src.load.load_coin_cap import insert_coins

        coins = [{
            "id": "bitcoin",
            "rank": 1,
            "symbol": "BTC",
            "name": "Bitcoin",
            "price_usd": 50000.00
        }]

        insert_coins(coins, conn=mock_conn)

        mock_execute_values.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.rollback.assert_not_called()


    def test_insert_coins_empty_list(self):
        from src.load.load_coin_cap import insert_coins

        mock_conn = MagicMock()

        insert_coins([], conn=mock_conn)

        mock_conn.cursor.assert_not_called()


    @patch("src.load.load_coin_cap.execute_values")
    def test_insert_coins_rollback_on_error(self, mock_execute_values):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        mock_execute_values.side_effect = Exception("DB Error")

        from src.load.load_coin_cap import insert_coins

        coins = [{
            "id": "bitcoin",
            "rank": 1,
            "symbol": "BTC",
            "name": "Bitcoin",
            "price_usd": 50000.00
        }]

        with pytest.raises(Exception):
            insert_coins(coins, conn=mock_conn)

        mock_conn.rollback.assert_called_once()
        mock_conn.commit.assert_not_called()