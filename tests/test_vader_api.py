from unittest.mock import Mock,patch
from application.vader_api import API_URL,TIMEOUT,hamta_prognos
data = hamta_prognos(59.33, 18.07)





@patch("application.vader_api.requests.get")

def test_hamta_prognos_returnerar_svaret(mock_get):
    mock_get.return_value = Mock(json=lambda:{"current":{},"daily":{}})
    assert data == {"current": {}, "daily": {}}
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert args[0] == API_URL
    assert kwargs["timeout"] == TIMEOUT
    assert kwargs["params"]["latitude"] == 59.33