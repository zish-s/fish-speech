# Punjabi (Gurmukhi) → Latin Transliteration Scheme

This document specifies the mapping used in `fish_speech/text/pa_normalize.py`
to convert Gurmukhi text into a diacritic-aware Latin transliteration before
it's passed to the model, when the `normalize_punjabi` request flag is set.

**Why** 
Since raw Gurmukhi text and a plain Latin produce remarkably worse pronunciation than a 
diacritic-marked Latin spelling. 
The vowel and consonant symbols follow ISO 15919/IAST convention. 
The schwa-deletion and addak-gemination rules are NOT part of ISO 15919 — that standard always writes the inherent vowel as 'a' and has no mechanism to drop it without an explicit virama. These are a separate, deliberate phonetic layer built on top.

## Vowels

| Gurmukhi | Independent (word-initial) | As a vowel sign (matra) | Latin |
|---|---|---|---|
| ਅ / — | ਅ | (none — inherent vowel) | a |
| ਆ / ਾ | ਆ | ਾ | ā |
| ਇ / ਿ | ਇ | ਿ | i |
| ਈ / ੀ | ਈ | ੀ | ī |
| ਉ / ੁ | ਉ | ੁ | u |
| ਊ / ੂ | ਊ | ੂ | ū |
| ਏ / ੇ | ਏ | ੇ | ē |
| ਐ / ੈ | ਐ | ੈ | ai |
| ਓ / ੋ | ਓ | ੋ | ō |
| ਔ / ੌ | ਔ | ੌ | au |

Long vowels get a macron (ā, ī, ū, ē, ō); short vowels don't. This is the
single biggest source of pronunciation improvement over plain Latin
spelling — e.g. `tuhāḍē` vs. the ambiguous `tuhade`.

## Consonants

| Gurmukhi | Latin | Gurmukhi | Latin | Gurmukhi | Latin |
|---|---|---|---|---|---|
| ਕ | k | ਟ | ṭ | ਤ | t |
| ਖ | kh | ਠ | ṭh | ਥ | th |
| ਗ | g | ਡ | ḍ | ਦ | d |
| ਘ | gh | ਢ | ḍh | ਧ | dh |
| ਙ | ṅ | ਣ | ṇ | ਨ | n |
| ਚ | c | ਪ | p | ਯ | y |
| ਛ | ch | ਫ | ph | ਰ | r |
| ਜ | j | ਬ | b | ਲ | l |
| ਝ | jh | ਭ | bh | ਵ | v |
| ਞ | ñ | ਮ | m | ਸ | s |
|   |   |   |   | ਹ | h |

Retroflex consonants (ਟ ਠ ਡ ਢ ਣ) get a dot below (ṭ ṭh ḍ ḍh ṇ) to distinguish
them from their dental counterparts (ਤ ਥ ਦ ਧ ਨ) — this distinction is
completely lost in plain Latin spelling (both map to `t`/`d`/`n`).

### Nukta-modified consonants (borrowed sounds)

| Gurmukhi | Latin |
|---|---|
| ਸ਼ | ś |
| ਜ਼ | z |
| ਖ਼ | x |
| ਗ਼ | ġ |
| ਫ਼ | f |
| ਲ਼ | ḷ |

## Gemination (addak, `ੱ` U+0A71)

Addak doubles the consonant that **follows** it, not the one it's visually
adjacent to on the left. `ਗੱਲ` (ਗ + ੱ + ਲ) → `gall`, not `ggal`.

## Nasalization (bindi `ਂ` U+0A02 / tippi `ੰ` U+0A70)

Both are rendered as a trailing `ṁ` attached to the syllable they modify —
whether that syllable has an explicit vowel (`ਸਿੰਘ` → `siṁgh`) or is a bare
consonant carrying its own (kept) inherent vowel (`ਪੰਜਾਬ` → `paṁjāb`).

## Inherent vowel ("schwa") deletion

Every Gurmukhi consonant letter with no explicit vowel sign carries an
implicit "a" sound (traditionally called a schwa) that is often — but not
always — dropped in speech. Getting this right is the hardest part of the
scheme. The rule implemented here:

1. Find runs of consecutive bare consonants (an addak doesn't break a run,
   since it carries no vowel of its own).
2. A run of exactly one bare consonant that is **not** at the literal end
   of the word keeps its schwa.
   - `ਵਧੀਆ` → `va`dhīā (ਵ is isolated, mid-word → keeps "a")
3. Every other run — length 1 at the end of a word, or length 2+ anywhere —
   is resolved right-to-left, alternating starting with **delete** at the
   rightmost consonant of the run:
   - `ਦਿਲ` → dil (ਲ is a length-1 run at word end → deletes)
   - `ਮੌਸਮ` → mausam (ਸ,ਮ run: ਮ deletes, ਸ keeps → "sam")
   - `ਕਰਕੇ` → karkē (ਕ,ਰ run: ਰ deletes, ਕ keeps → "kar")


**This is a heuristic, not a full phonological analysis.** It was derived
directly from, and exactly reproduces, the example sentence in the
originating issue.

Further testing over a wider varied vocabulary is remaining, for now the testing in the tests folder has been done for specified sentences in the issue 1321.