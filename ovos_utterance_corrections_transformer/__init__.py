from typing import List, Optional

from json_database import JsonStorage
from ovos_config.meta import get_xdg_base
from ovos_plugin_manager.templates.transformers import UtteranceTransformer
from ovos_utils.xdg_utils import xdg_data_home


class UtteranceCorrectionsPlugin(UtteranceTransformer):

    def __init__(self, name="ovos-utterance-corrections", priority=1):
        super().__init__(name, priority)
        self.db = JsonStorage(path=f"{xdg_data_home()}/{get_xdg_base()}/corrections.json")

    def transform(self, utterances: List[str],
                  context: Optional[dict] = None) -> (list, dict):
        context = context or {}
        for u in utterances:
            if u in self.db:
                return [self.db[u]], context
        return utterances, context
