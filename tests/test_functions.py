from requests.models import Response

import StocksMA.StocksMA as Stocks
import StocksMA.utils as utils


def mock_get_isin_request(*args, **kwargs) -> Response:
    response = Response()
    response.status_code = 200
    response._content = b'{"result": [{"name": "Maroc Telecom", "isin": "US0378331005"}]}'
    return response


def test_get_isin(monkeypatch) -> None:
    monkeypatch.setattr(utils, 'get_request', mock_get_isin_request)
    assert isinstance(Stocks.get_isin("IAM"), tuple)


def test_get_market_status() -> None:
    stat = Stocks.get_market_status()
    assert isinstance(stat, str)
