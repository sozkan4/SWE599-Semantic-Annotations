from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock

from .views import get_wikidata_explanations


class GetWikidataExplanationsTests(SimpleTestCase):
    """Tests for the ``get_wikidata_explanations`` helper."""

    @patch("movie_app.views.requests.get")
    def test_returns_explanation_for_valid_id(self, mock_get):
        """Should return a list with label and description when the API succeeds."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "entities": {
                "Q42": {
                    "labels": {"en": {"value": "Douglas Adams"}},
                    "descriptions": {"en": {"value": "English writer"}},
                }
            }
        }
        mock_get.return_value = mock_response

        result = get_wikidata_explanations("Q42")
        expected = [
            {
                "label": "Douglas Adams",
                "description": "English writer",
                "concepturi": "https://www.wikidata.org/wiki/Q42",
            }
        ]
        self.assertEqual(result, expected)

    @patch("movie_app.views.requests.get")
    def test_returns_empty_list_on_failure(self, mock_get):
        """Should return an empty list when the API response is not successful."""
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {}

        result = get_wikidata_explanations("Q999999")
        self.assertEqual(result, [])

