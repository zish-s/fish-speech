import unittest

from fish_speech.text.pa_normalize import normalize_punjabi


class TestPunjabiNormalize(unittest.TestCase):
    def test_addak_gemination(self):
        # ਗੱਲ ("gall") — addak geminates the consonant that follows it,
        # not the one it's written after.
        self.assertEqual(normalize_punjabi("ਗੱਲ"), "gall")

    def test_addak_word_initial(self):
        # ਅੱਜ ("ajj") — addak + word-final bare consonant (schwa dropped).
        self.assertEqual(normalize_punjabi("ਅੱਜ"), "ajj")

    def test_tippi_nasalization_on_vowel(self):
        # ਸਿੰਘ (Singh) — tippi nasalizes the preceding vowel.
        self.assertEqual(normalize_punjabi("ਸਿੰਘ"), "siṁgh")

    def test_tippi_nasalization_on_bare_consonant(self):
        # ਪੰਜਾਬ (Punjab) — tippi attaches directly to a bare
        # consonant's (kept) schwa.
        self.assertEqual(normalize_punjabi("ਪੰਜਾਬ"), "paṁjāb")

    def test_retroflex_consonants(self):
        # ਤੁਹਾਡੇ ("tuhāḍē") exercises the retroflex ਡ -> ḍ.
        self.assertEqual(normalize_punjabi("ਤੁਹਾਡੇ"), "tuhāḍē")

    def test_schwa_kept_isolated_medial_consonant(self):
        # ਵਧੀਆ ("vadhīā") — a single bare consonant not at word end
        # keeps its schwa.
        self.assertEqual(normalize_punjabi("ਵਧੀਆ"), "vadhīā")

    def test_schwa_alternation_in_consonant_run(self):
        # ਕਰਕੇ ("karkē") — two adjacent bare consonants: the one
        # closer to the end of the run drops its schwa, the next
        # one back keeps it.
        self.assertEqual(normalize_punjabi("ਕਰਕੇ"), "karkē")

    def test_word_final_schwa_deletion(self):
        # ਦਿਲ ("dil") — a lone bare consonant at the literal end of
        # the word drops its schwa.
        self.assertEqual(normalize_punjabi("ਦਿਲ"), "dil")

    def test_nukta_consonant(self):
        # ਖੁਸ਼ ("khuś") exercises the nukta-formed ਸ਼ -> ś.
        self.assertEqual(normalize_punjabi("ਖੁਸ਼"), "khuś")

    def test_independent_vowel_after_syllable(self):
        # ਗਿਆ ("giā") — a standalone independent vowel letter forming
        # its own syllable after a consonant-vowel syllable.
        self.assertEqual(normalize_punjabi("ਗਿਆ"), "giā")

    def test_non_gurmukhi_text_passes_through(self):
        self.assertEqual(normalize_punjabi("hello world 123"), "hello world 123")

    def test_mixed_script_input(self):
        self.assertEqual(normalize_punjabi("ਦਿਲ (heart)"), "dil (heart)")

    def test_full_issue_example_sentence(self):
        # The complete worked example from the originating GitHub
        # issue. This is the sentence the maintainers' listening
        # tests were run against.
        gurmukhi = (
            "ਅੱਜ ਮੌਸਮ ਬਹੁਤ ਵਧੀਆ ਹੈ, ਤੇ ਤੁਹਾਡੇ ਨਾਲ ਗੱਲ ਕਰਕੇ "
            "ਮੇਰਾ ਦਿਲ ਖੁਸ਼ ਹੋ ਗਿਆ।"
        )
        expected = (
            "ajj mausam bahut vadhīā hai, tē tuhāḍē nāl gall karkē "
            "mērā dil khuś hō giā."
        )
        self.assertEqual(normalize_punjabi(gurmukhi), expected)


if __name__ == "__main__":
    unittest.main()