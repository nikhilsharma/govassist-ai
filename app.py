from flask import Flask, jsonify, render_template, request

from config import Config
from repositories.issue_repository import IssueRepository
from services.analysis_service import AnalysisService
from services.knowledge_base_service import KnowledgeBaseService


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    repository = IssueRepository(app.config["DATABASE_PATH"])
    repository.initialize()
    knowledge_base = KnowledgeBaseService(app.config["KNOWLEDGE_BASE_PATH"])
    analyzer = AnalysisService(
        api_key=app.config["OPENAI_API_KEY"],
        model=app.config["OPENAI_MODEL"],
        knowledge_base=knowledge_base,
    )

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/api/analyze")
    def analyze_issue():
        payload = request.get_json(silent=True) or {}
        issue_text = (payload.get("issue") or "").strip()
        if len(issue_text) < 15:
            return jsonify({"error": "Please enter an operational issue of at least 15 characters."}), 400
        if len(issue_text) > 8000:
            return jsonify({"error": "Please limit the issue description to 8,000 characters."}), 400

        try:
            analysis = analyzer.analyze(issue_text)
            record_id = repository.save(issue_text, analysis)
            return jsonify({"id": record_id, "analysis": analysis})
        except Exception:
            app.logger.exception("Issue analysis failed")
            return jsonify({"error": "Analysis could not be completed. Please try again."}), 500

    @app.get("/api/history")
    def history():
        return jsonify(repository.list_recent())

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
