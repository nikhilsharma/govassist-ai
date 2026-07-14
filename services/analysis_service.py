import json

from openai import OpenAI


class AnalysisService:
    def __init__(self, api_key, model, knowledge_base):
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = model
        self.knowledge_base = knowledge_base

    def analyze(self, issue_text: str) -> dict:
        if not self.knowledge_base.is_supported_domain(issue_text):
            return self._no_matching_playbook_analysis()

        matching_playbook = self.knowledge_base.find_matching_playbook(issue_text)
        context = self.knowledge_base.relevant_context(issue_text)
        if not self.client:
            analysis = self._demo_analysis(issue_text, context)
        else:
            response = self.client.responses.create(
                model=self.model,
                instructions=(
                    "You are GovAssist AI, an internal decision-support assistant for government officers. "
                    "Use only the supplied knowledge-base context for procedures. Do not invent laws, deadlines, "
                    "case numbers, or facts. Be neutral, practical, and concise. Return valid JSON only."
                ),
                input=(
                    f"Operational issue:\n{issue_text}\n\n"
                    f"Local knowledge-base context:\n{json.dumps(context, ensure_ascii=False)}\n\n"
                    "Return this exact JSON object shape: "
                    '{"issue_category":"", "summary":"", "relevant_stakeholder":"", '
                    '"verification_steps":[""], "suggested_action":"", "draft_official_reply":""}'
                ),
            )
            analysis = self._parse_response(response.output_text)

        if self._has_confirmed_playbook_match(analysis) and matching_playbook and matching_playbook.get("draft_reply"):
            analysis["draft_official_reply"] = matching_playbook["draft_reply"]
        if self._has_confirmed_playbook_match(analysis) and matching_playbook:
            analysis["matched_operational_playbook"] = {
                "title": matching_playbook.get("title", ""),
                "id": matching_playbook.get("id", ""),
            }
        return analysis

    @staticmethod
    def _has_confirmed_playbook_match(analysis: dict) -> bool:
        category = (analysis.get("issue_category") or "").strip().lower()
        summary = (analysis.get("summary") or "").strip().lower()
        no_match_indicators = (
            "no matching operational playbook",
            "no matching kb entry",
            "no suitable knowledge-base match",
            "no suitable knowledge base match",
            "no suitable operational playbook",
            "outside the supported operational domain",
        )
        return bool(category) and not any(indicator in f"{category} {summary}" for indicator in no_match_indicators)

    @staticmethod
    def _no_matching_playbook_analysis() -> dict:
        return {
            "issue_category": "No Matching Operational Playbook",
            "summary": "The submitted issue is outside the supported MPLADS operational domain.",
            "relevant_stakeholder": "N/A",
            "verification_steps": ["No matching operational playbook found for the submitted issue."],
            "suggested_action": "Please submit an issue related to the supported MPLADS operational workflows.",
            "draft_official_reply": (
                "This prototype currently supports MPLADS operational issues only. "
                "No suitable operational playbook was found for the submitted issue."
            ),
        }

    @staticmethod
    def _parse_response(output_text: str) -> dict:
        try:
            result = json.loads(output_text)
        except json.JSONDecodeError as error:
            raise ValueError("The AI response was not valid JSON.") from error

        required = {
            "issue_category", "summary", "relevant_stakeholder", "verification_steps",
            "suggested_action", "draft_official_reply",
        }
        if not required.issubset(result) or not isinstance(result["verification_steps"], list):
            raise ValueError("The AI response did not match the required format.")
        return result

    @staticmethod
    def _demo_analysis(issue_text: str, context: list[dict]) -> dict:
        playbook = context[0] if context else {}
        category = playbook.get("category", "General operational issue")
        stakeholder = playbook.get("primary_stakeholder", "Relevant department nodal officer")
        steps = playbook.get("verification_steps", [
            "Record the complaint and acknowledge receipt.",
            "Verify the facts with the responsible field unit.",
            "Document the outcome and next action.",
        ])
        return {
            "issue_category": category,
            "summary": f"The reported issue concerns: {issue_text[:280]}",
            "relevant_stakeholder": stakeholder,
            "verification_steps": steps,
            "suggested_action": playbook.get("suggested_action", "Assign the matter to the appropriate officer and track closure."),
            "draft_official_reply": (
                "Dear Citizen,\n\nYour concern has been registered for verification by the concerned department. "
                "We will update you after the verification is completed.\n\nRegards,\nAuthorized Officer"
            ),
            "mode": "demo",
        }
