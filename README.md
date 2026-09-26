# Utterance Corrections plugin

This plugin corrects speech-to-text (STT) output before intent matching. It is an [OVOS](https://github.com/OpenVoiceOS) text transformer plugin that applies user-defined replacements to each utterance.

The plugin supports three kinds of corrections:
1. **Full utterance corrections**: map a whole phrase to a different phrase, matched by fuzzy string similarity.
2. **Word-level corrections**: replace specific words or names, regardless of the rest of the sentence.
3. **Regex-based corrections**: replace text that matches a regular expression.

---

## Install

```bash
pip install ovos-utterance-corrections-plugin
```

The plugin registers itself as an OVOS transformer plugin under the entry point group `opm.transformer.text`, so [ovos-core](https://github.com/OpenVoiceOS/ovos-core) picks it up automatically once installed.

---

## 1. Full Utterance Corrections

This plugin reads a user-defined JSON file for utterance fixes at `~/.local/share/mycroft/corrections.json`.

Fuzzy matching compares each utterance against the entries in this file. If the similarity is 85% or higher, the plugin returns the mapped replacement instead of the original transcription. This lets you map a random utterance to a different one, for example to give your assistant a command through an unrelated phrase.

### Example: `corrections.json`
```json
{
    "I hate open source": "I love open source",
    "do the thing": "trigger protocol 404"
}
```

**Input**:
`"I hat open source"`

**Output**:
`"I love open source"`

---

## 2. Word-Level Corrections

Define unconditional word-level replacements in `~/.local/share/mycroft/word_corrections.json`.

Use this file when an STT model repeatedly mistranscribes specific names or words.

### Example: `word_corrections.json`
```json
{
    "Jimmy Hendricks": "Jimi Hendrix",
    "Eric Klapptern": "Eric Clapton",
    "Eric Klappton": "Eric Clapton"
}
```

**Input**:
`"I love Jimmy Hendricks"`

**Output**:
`"I love Jimi Hendrix"`

For example, Whisper STT often mistranscribes names this way.

---

## 3. Regex-Based Corrections

For more complex corrections, use regular expressions in `~/.local/share/mycroft/regex_corrections.json`.

Use this file to fix consistent patterns in STT errors, such as a model that substitutes one trigraph for another.

### Example: `regex_corrections.json`
```json
{
    "\\bsh(\\w*)": "sch\\1"
}
```

### Explanation:
- `\\bsh(\\w*)` matches words that start with `sh` at a word boundary.
- `sch\\1` replaces `sh` with `sch` and keeps the rest of the word.

### Example Usage:
**Input**:
`"shalter is a switch"`

**Output**:
`"schalter is a switch"`

For example, the Citrinet German model often makes this mistake.

---

## Configuration Paths

| File                      | Purpose                               |
|---------------------------|----------------------------------------|
| `corrections.json`        | Full utterance replacements.          |
| `word_corrections.json`   | Word-level replacements.              |
| `regex_corrections.json`  | Regex-based pattern replacements.     |

All correction files live under `~/.local/share/mycroft/`.

---

## Usage Scenarios

- **Improve intent matching**: normalize STT output so the same phrase always triggers the same intent.
- **Fix model-specific errors**: correct transcription mistakes that a given STT engine repeats.
- **Shortcut commands**: map a short phrase or slang term to the full utterance that triggers an intent.

## Related projects

- [ovos-utterance-normalizer](https://github.com/OpenVoiceOS/ovos-utterance-normalizer) — another OVOS text transformer plugin, for normalizing utterance formatting.
- [ovos-dialog-normalizer-plugin](https://github.com/OpenVoiceOS/ovos-dialog-normalizer-plugin) — normalizes dialog output.
- [ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager) — defines the transformer plugin interface this plugin implements.

## License

Apache-2.0. See [LICENSE](LICENSE).
