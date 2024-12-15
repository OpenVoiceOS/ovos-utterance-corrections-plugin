import regex  # Use the regex module instead of re
from typing import List, Optional

from json_database import JsonStorage
from ovos_config.meta import get_xdg_base
from ovos_plugin_manager.templates.transformers import UtteranceTransformer
from ovos_utils.parse import match_one, MatchStrategy
from ovos_utils.xdg_utils import xdg_data_home
from ovos_utils.log import LOG


class UtteranceCorrectionsPlugin(UtteranceTransformer):

    def __init__(self, name="ovos-utterance-corrections", priority=1):
        super().__init__(name, priority)
        self.db = JsonStorage(path=f"{xdg_data_home()}/{get_xdg_base()}/corrections.json")
        self.words_db = JsonStorage(path=f"{xdg_data_home()}/{get_xdg_base()}/word_corrections.json")
        self.regex_db = JsonStorage(path=f"{xdg_data_home()}/{get_xdg_base()}/regex_corrections.json")
        self.match_strategy = MatchStrategy.DAMERAU_LEVENSHTEIN_SIMILARITY  # TODO - from config

    def transform(self, utterances: List[str], context: Optional[dict] = None) -> (list, dict):
        context = context or {}

        # Step 1: Replace full utterance
        if utterances and self.db:
            replacement, conf = match_one(
                utterances[0], self.db, strategy=self.match_strategy
            )
            if conf >= self.config.get("thresh", 0.85):
                LOG.debug(f"Applying utterance replacement: {utterances[0]} -> {replacement}")
                return [replacement], context

        # Step 2: Apply regex replacements
        if utterances and self.regex_db:
            flags = regex.IGNORECASE if self.config.get("ignore_case", True) else 0
            for idx in range(len(utterances)):
                for pattern, replacement in self.regex_db.items():
                    LOG.debug(f"Applying regex pattern: {pattern}")
                    try:
                        # Validate pattern length
                        if len(pattern) > 1000:
                            LOG.warning(f"Skipping oversized pattern: {pattern}")
                            continue

                        # Compile pattern with timeout
                        compiled_pattern = regex.compile(pattern, flags=flags)
                        utterances[idx] = compiled_pattern.sub(replacement, utterances[idx])

                    except regex.error as e:
                        LOG.error(f"Invalid regex pattern: {pattern} -> {e}")
                    except TimeoutError:
                        LOG.error(f"Regex pattern timed out: {pattern}")

        # Step 3: Replace individual words
        if utterances and self.words_db:
            flags = regex.IGNORECASE if self.config.get("ignore_case", True) else 0
            for idx in range(len(utterances)):
                for w, r in self.words_db.items():
                    LOG.debug(f"Applying word replacement: {w} -> {r}")
                    # Use regex to ensure replacements are surrounded by word boundaries
                    utterances[idx] = regex.sub(rf"\b{regex.escape(w)}\b", r, utterances[idx], flags=flags)

        return utterances, context
