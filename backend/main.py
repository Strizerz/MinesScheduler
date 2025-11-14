from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from catalog import Catalog

catalog = Catalog("courses.db")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search(keyword: str):
    results = catalog.search(keyword)
    return [s.__dict__ for s in results]

@app.get("/course")
def course(code: str):
    results = catalog.sections_for(code)
    return [s.__dict__ for s in results]

@app.get("/subject")
def subject(subj: str):
    results = [s for s in catalog.sections if s.subject == subj.upper()]
    return [s.__dict__ for s in results]

@app.get("/prof")
def prof(name: str):
    results = catalog.sections_for_prof(name)
    return [s.__dict__ for s in results]

@app.get("/day")
def day(days: str):
    days = days.upper()
    results = [
        s for s in catalog.sections
        if all(d in s.days for d in days) and len(s.days) == len(days)
    ]
    return [s.__dict__ for s in results]
