import unittest

from fastapi import HTTPException
from pydantic import ValidationError

from backend import (
    MAX_BODY_CHARS,
    MAX_BODY_WORDS,
    ConcordanceRequest,
    create_concordance,
)


class ConcordanceApiLimitsTest(unittest.TestCase):
    def test_normal_request(self):
        response = create_concordance(
            ConcordanceRequest(exclusion_words="", body_text="hello world")
        )

        self.assertEqual(len(response["lines"]), 2)

    def test_rejects_body_over_character_limit(self):
        with self.assertRaises(ValidationError):
            ConcordanceRequest(
                exclusion_words="",
                body_text="x" * (MAX_BODY_CHARS + 1),
            )

    def test_rejects_body_over_word_limit(self):
        request = ConcordanceRequest(
            exclusion_words="",
            body_text="x " * (MAX_BODY_WORDS + 1),
        )

        with self.assertRaises(HTTPException) as raised:
            create_concordance(request)

        self.assertEqual(raised.exception.status_code, 413)


if __name__ == "__main__":
    unittest.main()
