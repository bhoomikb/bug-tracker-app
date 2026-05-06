# 🐛 Bug Tracker App

A full-stack bug tracking web application built from scratch with **Python (Flask)** on the backend and **HTML/CSS/JavaScript** on the frontend. Demonstrates end-to-end web development skills and QA-domain knowledge.

---

## ✨ Features

- ✅ Log bugs with title, description, severity, and assignee
- ✅ View all bugs in a clean, sortable dashboard
- ✅ Advance bug status with one click: `Open → In Progress → Resolved → Closed`
- ✅ Filter bugs by status or severity
- ✅ Live stats bar (total, open, in progress, resolved, critical count)
- ✅ Delete bugs
- ✅ SQLite persistent storage — data survives restarts
- ✅ Seeded with sample data on first run

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python 3, Flask |
| Database | SQLite (via Python's built-in `sqlite3`) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| API | RESTful JSON API |

---

## 📂 Project Structure

```
bug-tracker-app/
├── app.py                  # Flask app + REST API
├── templates/
│   └── index.html          # Full frontend (single-page)
├── requirements.txt
├── bugs.db                 # Auto-created SQLite DB (gitignored)
└── README.md
```

---

## ⚙️ Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open in browser
# → http://localhost:5000
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/bugs` | Get all bugs (filter by status/severity) |
| POST | `/api/bugs` | Create a new bug |
| PATCH | `/api/bugs/<id>` | Update a bug (status, severity, etc.) |
| DELETE | `/api/bugs/<id>` | Delete a bug |
| GET | `/api/stats` | Get summary stats |

---

## 📸 Screenshot

> Dashboard shows bugs with severity color-coding, status badges, and live counters.
> Click any status badge to advance the bug through its lifecycle.

---

## 💡 Key Concepts Demonstrated

- ✅ RESTful API design (GET, POST, PATCH, DELETE)
- ✅ SQL database operations via Python
- ✅ Dynamic frontend with Fetch API (no frameworks)
- ✅ Responsive CSS layout
- ✅ QA domain knowledge (bug lifecycle, severity levels)

---

## 👩‍💻 Author

**Bhoomi Bhavsar** — CS Graduate | Manual QA Tester | Anthropic AI Certified  
[LinkedIn](https://www.linkedin.com/in/bhoomi-bhavsar)
