"""Source-word false positives must not weaken actual credential matching."""
import unittest
from scripts.scan_secrets import PATTERNS

class TokenBoundaryTests(unittest.TestCase):
    def test_openai_like_tokens_still_detected(self):
        token='s'+'k-'+('a'*24)
        project='s'+'k-proj-'+('b'*24)
        for text in (token, '"'+token+'"', 'Bearer '+token, '/'+project, '=' + project):
            self.assertIsNotNone(PATTERNS['OpenAI-style token'].search(text))
    def test_risk_word_in_official_document_slug_is_not_a_token(self):
        public='https://docs.os.uk/osngd/code-lists/higher-risk-'+('a'*24)
        self.assertIsNone(PATTERNS['OpenAI-style token'].search(public))
if __name__=='__main__':unittest.main()
