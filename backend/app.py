import html
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "courses.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/search")
def search_classes(
    course: str = Query("", alias="course"),
    title: str = Query("", alias="title"),
    prof: str = Query("", alias="prof"),
):
    conn = get_connection()
    cur = conn.cursor()

    conditions = []
    params = []

    if course:
        like = f"%{course}%"
        conditions.append(
            "(subject || courseNumber LIKE ? OR subject LIKE ? OR courseNumber LIKE ?)"
        )
        params.extend([like, like, like])

    if title:
        like = f"%{title}%"
        conditions.append("courseTitle LIKE ?")
        params.append(like)

    if prof:
        like = f"%{prof}%"
        conditions.append("faculty_0_displayName LIKE ?")
        params.append(like)

    sql = """
        SELECT
            courseReferenceNumber AS crn,
            subject,
            courseNumber AS number,
            sequenceNumber AS section,
            courseTitle AS title,
            faculty_0_displayName AS prof
        FROM courses
    """

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " LIMIT 100"

    cur.execute(sql, params)
    rows = []
    for r in cur.fetchall():
        d = dict(r)
        s = d["title"]
        for _ in range(5):
            ns = html.unescape(s)
            if ns == s:
                break
            s = ns
        d["title"] = s
        rows.append(d)

    conn.close()
    return rows
