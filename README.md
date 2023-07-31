# Utterance Corrections plugin

- "secret speech", map some random utterance to something else so you can furtively give orders to your assistant
- shortcuts, map shorter utterances or slang to utterances you know trigger the correct intent
- manually correct bad STT transcriptions you experimentally determined to be common for you

This plugin checks a user defined json for utterance fixes `~/.local/share/mycroft/corrections.json`

fuzzy matching is used to determine if a utterance matches the transcription
if >=0.85% similarity then the replacement is returned instead of the original transcription
```json
{
    "I hate open source": "I love open source",
    "do the thing": "trigger protocol 404"
}
```

you can also define unconditional replacements at word level `~/.local/share/mycroft/word_corrections.json`

for example whisper STT often gets artist names wrong, this allows you to correct them
```json
{
    "Jimmy Hendricks": "Jimi Hendrix",
    "Eric Klapptern": "Eric Clapton",
    "Eric Klappton": "Eric Clapton"
}
```