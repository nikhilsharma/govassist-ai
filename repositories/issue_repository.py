import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class IssueRepository:
    def __init__(self, database_path: Path):
        self.database_path = database_path

    def _connection(self):
        return sqlite3.connect(self.database_path)

    def initialize(self):
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connection() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS issue_analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    issue_text TEXT NOT NULL,
                    analysis_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

    def save(self, issue_text: str, analysis: dict) -> int:
        created_at = datetime.now(timezone.utc).isoformat()
        with self._connection() as connection:
            cursor = connection.execute(
                "INSERT INTO issue_analyses (issue_text, analysis_json, created_at) VALUES (?, ?, ?)",
                (issue_text, json.dumps(analysis), created_at),
            )
            return cursor.lastrowid

    def list_recent(self, limit: int = 10) -> list[dict]:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT id, issue_text, analysis_json, created_at FROM issue_analyses "
                "ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [
            {"id": row[0], "issue": row[1], "analysis": json.loads(row[2]), "created_at": row[3]}
            for row in rows
        ]
