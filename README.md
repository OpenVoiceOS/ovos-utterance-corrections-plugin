# Utterance Corrections plugin

- "secret speech", map some random utterance to something else so you can furtively give orders to your assistant
- shortcuts, map shorter utterances or slang to utterances you know trigger the correct intent
- manually correct bad STT transcriptions you experimentally determined to be common for you

This plugin checks a user defined json for utterance fixes `~/.local/share/mycroft/corrections.json`


```json
{
    "I hate open source": "I love open source",
    "do the thing": "trigger protocol 404"
}
```