import re
from typing import List, Optional

from json_database import JsonStorage
from ovos_config.meta import get_xdg_base
from ovos_plugin_manager.templates.transformers import UtteranceTransformer
from ovos_utils.parse import match_one, MatchStrategy
from ovos_utils.xdg_utils import xdg_data_home


class UtteranceCorrectionsPlugin(UtteranceTransformer):

    def __init__(self, name="ovos-utterance-corrections", priority=1):
        super().__init__(name, priority)
        self.db = JsonStorage(path=f"{xdg_data_home()}/{get_xdg_base()}/corrections.json")
        self.words_db = JsonStorage(path=f"{xdg_data_home()}/{get_xdg_base()}/word_corrections.json")
        self.regex_db = JsonStorage(path=f"{xdg_data_home()}/{get_xdg_base()}/regex_corrections.json")
        self.confidence_threshold = 0.85  # Default threshold, configurable
        self.match_strategy = MatchStrategy.DAMERAU_LEVENSHTEIN_SIMILARITY

    def transform(self, utterances: List[str], context: Optional[dict] = None) -> (list, dict):
        context = context or {}

        # Step 1: Replace full utterance
        if utterances and self.db:
            replacement, conf = match_one(
                utterances[0], self.db, strategy=self.match_strategy
            )
            if conf >= self.confidence_threshold:
                return [replacement], context

        # Step 2: Apply regex replacements
        if utterances and self.regex_db:
            for idx in range(len(utterances)):
                for pattern, replacement in self.regex_db.items():
                    try:
                        utterances[idx] = re.sub(pattern, replacement, utterances[idx])
                    except re.error as e:
                        print(f"Invalid regex pattern: {pattern} -> {e}")

        # Step 3: Replace individual words
        if utterances and self.words_db:
            for idx in range(len(utterances)):
                for w, r in self.words_db.items():
                    utterances[idx] = utterances[idx].replace(w, r)

        return utterances, context
