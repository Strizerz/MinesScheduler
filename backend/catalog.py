import sqlite3

class Section:
    def __init__(self, row):
        self.subject = row["subject"]
        self.number = row["courseNumber"]
        self.title = row["courseTitle"]
        self.crn = row["courseReferenceNumber"]
        self.prof = row["faculty_0_displayName"]
        self.section = row["sequenceNumber"]
        #self.dayCode = row["Days"]
        self.days = self.extract_days(row)
        self.start, self.end = self.extract_time(row)

    def safe(self, row, key):
        return row[key] if key in row.keys() else None

    def extract_days(self, row):
        days = []
        for idx in range(5):
            base = f"meetingsFaculty_{idx}_meetingTime_"
            values = {
                "M": self.safe(row, base + "monday"),
                "T": self.safe(row, base + "tuesday"),
                "W": self.safe(row, base + "wednesday"),
                "R": self.safe(row, base + "thursday"),
                "F": self.safe(row, base + "friday")
            }
            for letter, v in values.items():
                if v and str(v).upper() in ("Y", "1", "TRUE"):
                    days.append(letter)
        return list(dict.fromkeys(days))

    def extract_time(self, row):
        for idx in range(5):
            base = f"meetingsFaculty_{idx}_meetingTime_"
            start = self.safe(row, base + "beginTime")
            end = self.safe(row, base + "endTime")
            if start and end:
                try:
                    return int(start), int(end)
                except:
                    return None, None
        return None, None

    def conflicts_with(self, other):
        if not self.start or not other.start:
            return False
        if not set(self.days) & set(other.days):
            return False
        return self.start < other.end and other.start < self.end

    def __repr__(self):
        return f"{self.subject}{self.number}{self.section} {self.days} {self.start}-{self.end} {self.title}"


class Catalog:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.sections = []
        self.by_course = {}
        self.by_prof = {}
        self.load_all()

    def load_all(self):
        cur = self.conn.execute("SELECT * FROM courses;")
        rows = cur.fetchall()
        for row in rows:
            section = Section(row)
            self.sections.append(section)
            key = section.subject.upper() + section.number
            self.by_course.setdefault(key, []).append(section)
            if section.prof:
                self.by_prof.setdefault(section.prof.lower(), []).append(section)
        print(f"Loaded {len(self.sections)} sections into memory.")

    def search(self, keyword):
        k = keyword.lower()
        return [
            s for s in self.sections
            if k in s.title.lower() or k in s.number.lower() or k in s.subject.lower()
        ]

    def sections_for(self, course_query):
        q = course_query.upper().strip()
        if q.isdigit():
            return [s for s in self.sections if s.number == q]
        subject = "".join(c for c in q if c.isalpha())
        number = "".join(c for c in q if c.isdigit())
        if subject and number:
            return [
                s for s in self.sections
                if s.subject.upper() == subject and s.number == number
            ]
        return []

    def sections_for_prof(self, prof_query):
        k = prof_query.lower()
        return [s for s in self.sections if k in s.prof.lower()]
