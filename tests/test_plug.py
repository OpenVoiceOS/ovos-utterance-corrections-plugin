import unittest
from unittest.mock import patch

from ovos_utterance_corrections_transformer import UtteranceCorrectionsPlugin


class TestUtteranceCorrectionsPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = UtteranceCorrectionsPlugin()

    def test_transform_full_utterance_replacement(self):
        # Mock the match_one function
        self.plugin.config = {"thresh": 0.85}  # Set threshold for replacement
        self.plugin.db = {"test utterance": "replaced utterance"}

        # Test input
        utterances = ["test utterance"]
        transformed, context = self.plugin.transform(utterances)

        # Assertions
        self.assertEqual(transformed, ["replaced utterance"])
        self.assertEqual(context, {})

    def test_transform_regex_no_match(self):
        # Mock the regex_db with a pattern that won't match
        self.plugin.config = {"ignore_case": True}
        self.plugin.regex_db = {
            r"\bsh(\w*)": "sch\\1"
        }

        # Test input with no match
        utterances = ["hello"]
        transformed, context = self.plugin.transform(utterances)

        # Assertions
        self.assertEqual(transformed, ["hello"])
        self.assertEqual(context, {})

    def test_transform_regex_replacement(self):
        # Mock the regex_db with a valid pattern and replacement
        self.plugin.config = {"ignore_case": True}
        self.plugin.regex_db = {
            r"\bsh(\w*)": "sch\\1"
        }

        # Test input with matching regex pattern
        utterances = ["shalter"]
        transformed, context = self.plugin.transform(utterances)

        # Assertions
        self.assertEqual(transformed, ["schalter"])
        self.assertEqual(context, {})

    @patch("ovos_utterance_corrections_transformer.regex.compile")  # Mock regex compile
    def test_transform_regex_timeout(self, MockRegexCompile):
        # Mock the regex_db with a valid pattern and replacement
        self.plugin.config = {"ignore_case": True}
        self.plugin.regex_db = {
            r"\bsh(\w*)": "sch\\1"
        }

        # Mock regex to raise a TimeoutError
        MockRegexCompile.side_effect = TimeoutError("Regex pattern timed out")

        # Test input with matching regex pattern
        utterances = ["shalter"]
        transformed, context = self.plugin.transform(utterances)

        # Assertions - no change because of timeout
        self.assertEqual(transformed, ["shalter"])
        self.assertEqual(context, {})

    def test_transform_oversized_regex_pattern(self):
        # Mock the regex_db with a large pattern that exceeds the size limit
        self.plugin.config = {"ignore_case": True}
        self.plugin.regex_db = {
            "a" * 1001: "replaced"  # Pattern longer than 1000 characters
        }

        # Test input
        utterances = ["this is a test"]
        transformed, context = self.plugin.transform(utterances)

        # Assertions
        self.assertEqual(transformed, ["this is a test"])  # No change due to oversized pattern
        self.assertEqual(context, {})

    def test_transform_word_replacement(self):
        # Mock the words_db with a valid word and replacement
        self.plugin.words_db = {"test": "exam"}

        # Test input with word replacement
        utterances = ["this is a test"]
        transformed, context = self.plugin.transform(utterances)

        # Assertions
        self.assertEqual(transformed, ["this is a exam"])
        self.assertEqual(context, {})

    def test_transform_multiple_replacements(self):
        # Mock the words_db with multiple words and replacements
        self.plugin.words_db = {"test": "exam", "hello": "hi"}

        # Test input with multiple word replacements
        utterances = ["hello, this is a test"]
        transformed, context = self.plugin.transform(utterances)

        # Assertions
        self.assertEqual(transformed, ["hi, this is a exam"])
        self.assertEqual(context, {})

    def test_transform_empty_input(self):
        # Test with empty input
        utterances = []
        transformed, context = self.plugin.transform(utterances)

        # Assertions
        self.assertEqual(transformed, [])
        self.assertEqual(context, {})

    def test_transform_no_match(self):
        # Test input with no matching patterns
        self.plugin.regex_db = {
            r"\bxyz(\w*)": "abc\\1"
        }

        utterances = ["test"]
        transformed, context = self.plugin.transform(utterances)

        # Assertions
        self.assertEqual(transformed, ["test"])
        self.assertEqual(context, {})


if __name__ == "__main__":
    unittest.main()
