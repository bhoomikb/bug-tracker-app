"""
Bug Tracker App
A lightweight full-stack bug tracking web application.
Built with Python (Flask) + HTML/CSS/JavaScript.

Features:
- Log new bugs with title, description, severity, and assignee
- View all bugs in a sortable table
- Update bug status (Open → In Progress → Resolved → Closed)
- Delete bugs
- Filter by status or severity
- Persistent storage using SQLite

Author: Bhoomi Bhavsar
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "bugs.db"


# ============================================================
# DATABASE SETUP
# ============================================================

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bugs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT,
            severity    TEXT NOT NULL DEFAULT 'Medium',
            status      TEXT NOT NULL DEFAULT 'Open',
            assignee    TEXT,
            reporter    TEXT,
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL
        )
    """)
    # Seed some sample bugs if empty
    count = conn.execute("SELECT COUNT(*) FROM bugs").fetchone()[0]
    if count == 0:
        sample_bugs = [
            ("Login button unresponsive on mobile",
             "The login button does not respond to tap events on iOS Safari.",
             "High", "Open", "Dev Team", "QA - Bhoomi"),
            ("Incorrect total on checkout page",
             "Discount code does not update the subtotal correctly.",
             "Critical", "In Progress", "Backend Team", "QA - Bhoomi"),
            ("Typo in error message",
             "Error message says 'pasword' instead of 'password'.",
             "Low", "Resolved", "Frontend Team", "QA - Bhoomi"),
            ("Profile photo upload fails for PNG files",
             "Only JPG uploads work. PNG files throw a 500 error.",
             "Medium", "Open", "Dev Team", "QA - Bhoomi"),
        ]
        for bug in sample_bugs:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            conn.execute("""
                INSERT INTO bugs (title, description, severity, status, assignee, reporter, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (*bug, now, now))
    conn.commit()
    conn.close()


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/bugs", methods=["GET"])
def get_bugs():
    status_filter   = request.args.get("status", "")
    severity_filter = request.args.get("severity", "")

    conn = get_db()
    query = "SELECT * FROM bugs WHERE 1=1"
    params = []

    if status_filter:
        query += " AND status = ?"
        params.append(status_filter)
    if severity_filter:
        query += " AND severity = ?"
        params.append(severity_filter)

    query += " ORDER BY created_at DESC"
    bugs = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict(b) for b in bugs])


@app.route("/api/bugs", methods=["POST"])
def create_bug():
    data = request.get_json()
    now  = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO bugs (title, description, severity, status, assignee, reporter, created_at, updated_at)
        VALUES (?, ?, ?, 'Open', ?, ?, ?, ?)
    """, (
        data.get("title"),
        data.get("description", ""),
        data.get("severity", "Medium"),
        data.get("assignee", "Unassigned"),
        data.get("reporter", "Anonymous"),
        now, now
    ))
    conn.commit()
    bug_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": bug_id, "message": "Bug created successfully"}), 201


@app.route("/api/bugs/<int:bug_id>", methods=["PATCH"])
def update_bug(bug_id):
    data = request.get_json()
    now  = datetime.now().strftime("%Y-%m-%d %H:%M")

    allowed_fields = {"title", "description", "severity", "status", "assignee"}
    updates = {k: v for k, v in data.items() if k in allowed_fields}

    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values     = list(updates.values()) + [now, bug_id]

    conn = get_db()
    conn.execute(f"UPDATE bugs SET {set_clause}, updated_at = ? WHERE id = ?", values)
    conn.commit()
    conn.close()

    return jsonify({"message": "Bug updated successfully"})


@app.route("/api/bugs/<int:bug_id>", methods=["DELETE"])
def delete_bug(bug_id):
    conn = get_db()
    conn.execute("DELETE FROM bugs WHERE id = ?", (bug_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Bug deleted"})


@app.route("/api/stats", methods=["GET"])
def get_stats():
    conn = get_db()
    stats = {
        "total":       conn.execute("SELECT COUNT(*) FROM bugs").fetchone()[0],
        "open":        conn.execute("SELECT COUNT(*) FROM bugs WHERE status = 'Open'").fetchone()[0],
        "in_progress": conn.execute("SELECT COUNT(*) FROM bugs WHERE status = 'In Progress'").fetchone()[0],
        "resolved":    conn.execute("SELECT COUNT(*) FROM bugs WHERE status = 'Resolved'").fetchone()[0],
        "critical":    conn.execute("SELECT COUNT(*) FROM bugs WHERE severity = 'Critical'").fetchone()[0],
    }
    conn.close()
    return jsonify(stats)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    init_db()
    print("🐛 Bug Tracker running at http://localhost:5000")
    app.run(debug=True)
