from unittest.mock import Mock, patch
import pytest
from application.vader_api import API_URL, TIMEOUT, hamta_prognos
import requests
@pytest.mark.parametrize("var,fel",
[
pytest.param("get",requests.Timeout,id="timeout"),
pytest.param("get",requests.ConnectionError,id="ingen-anslutning"),
pytest.param("raise_for_status",requests.HTTPError,id="http-fel"),
pytest.param("json",ValueError,id="trasig-json"),
])

@patch("application.vader_api.requests.get")
def test_fel_blir_vadertjanstfel(mock_get,var,fel):
    if var == "get":
        mock_get.side_effect=fel
    else:
        svar=Mock()
        getattr(svar,var).side_effect=fel
        mock_get.return_value=svar
        with pytest.raises(VaderTjanstFel):
            hamta_prognos(59.33,18.07)


def test_hamta_prognos_returnerar_svaret(mock_get):
    mock_get.return_value = Mock(json=lambda: {"current": {}, "daily": {}})
    data = hamta_prognos(59.33, 18.07)
    assert data == {"current": {}, "daily": {}}
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert args[0] == API_URL
    assert kwargs["timeout"] == TIMEOUT
    assert kwargs["params"]["latitude"] == 59.33
