import json
import re
from pathlib import Path


class KnowledgeBaseService:
    DOMAIN_TERMS = (
        "mplads esakshi pfms lgd vendor validation payment payments "
        "beneficiary utr portal access local government directory"
    )

    def __init__(self, source_path: Path):
        self.source_path = source_path

    def load(self) -> dict:
        with self.source_path.open(encoding="utf-8") as file:
            return json.load(file)

    def relevant_context(self, issue_text: str, limit: int = 3) -> list[dict]:
        issue_words = self._terms(issue_text)
        entries = self.load().get("issue_playbooks", [])

        def score(entry):
            keywords = self._terms(" ".join(entry.get("keywords", [])))
            return len(issue_words & keywords)

        ranked = sorted(entries, key=score, reverse=True)
        return [entry for entry in ranked[:limit] if score(entry) > 0] or entries[:limit]

    def find_matching_playbook(self, issue_text: str) -> dict | None:
        issue_words = self._terms(issue_text)
        entries = self.load().get("issue_playbooks", [])

        def score(entry):
            keywords = self._terms(" ".join(entry.get("keywords", [])))
            return len(issue_words & keywords)

        best_match = max(entries, key=score, default=None)
        return best_match if best_match and score(best_match) > 0 else None

    def is_supported_domain(self, issue_text: str) -> bool:
        supported_terms = self._terms(self.DOMAIN_TERMS)
        return bool(self._terms(issue_text) & supported_terms)

    @staticmethod
    def _terms(text: str) -> set[str]:
        terms = re.findall(r"[a-z0-9]+", text.lower())
        return {term[:-1] if term.endswith("s") and len(term) > 3 else term for term in terms}
