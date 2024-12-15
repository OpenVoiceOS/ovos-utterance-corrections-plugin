# Utterance Corrections plugin

This plugin provides tools to correct or adjust speech-to-text (STT) outputs for better intent matching or improved user experience.

### Key Features:
1. **"Secret Speech"**: Map random utterances to something else so you can furtively give orders to your assistant.
2. **Shortcuts**: Map shorter utterances or slang to known utterances that trigger the correct intent.
3. **Manual STT Fixes**: Correct common STT transcription errors you experimentally determined.

---

## 1. Full Utterance Corrections

This plugin checks a user-defined JSON file for **utterance fixes** at `~/.local/share/mycroft/corrections.json`.

**Fuzzy matching** is used to determine if an utterance matches a transcription. If similarity is greater than or equal to **85%**, the replacement is returned instead of the original transcription.

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

You can also define unconditional word-level replacements in `~/.local/share/mycroft/word_corrections.json`.  

This is particularly useful when STT models repeatedly transcribe specific names or words incorrectly.

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


> **use case**: whisper STT often does this mistake in it's transcriptions

---

## 3. Regex-Based Corrections

For more complex corrections, you can use **regular expressions** in `~/.local/share/mycroft/regex_corrections.json`.  

This is useful for fixing consistent patterns in STT errors, such as replacing incorrect trigraphs.

### Example: `regex_corrections.json`
```json
{
    "\\bsh(\\w*)": "sch\\1"
}
```

### Explanation:
- **`\\bsh(\\w*)`**: Matches words starting with `sh` at a word boundary.
- **`sch\\1`**: Replaces `sh` with `sch` and appends the rest of the word.

### Example Usage:
**Input**:  
`"shalter is a switch"`  

**Output**:  
`"schalter is a switch"`

> **use case**: citrinet german model often does this mistake in it's transcriptions

---

## Configuration Paths

| File                      | Purpose                               |
|---------------------------|---------------------------------------|
| `corrections.json`        | Full utterance replacements.          |
| `word_corrections.json`   | Word-level replacements.              |
| `regex_corrections.json`  | Regex-based pattern replacements.     |

All correction files are stored under:  
`~/.local/share/mycroft/`

---

### Usage Scenarios
- **Improve Intent Matching**: Ensure consistent STT output for accurate intent triggers.
- **Fix Model-Specific Errors**: Handle recurring transcription mistakes in certain STT engines.
- **Shortcut Commands**: Simplify complex commands with shorter phrases or slang.

Let us know how you're using this plugin, and feel free to contribute regex examples to this README or new use cases! 🚀