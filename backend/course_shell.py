from tabulate import tabulate
from catalog import Catalog

DB_PATH = "courses.db"

def printCommandList():
    print("Course shell. Commands:")
    print("  search <keyword>")
    print("  course <COURSE_NUM>          (e.g. course CSCI261 or course 261)")
    print("  prof <partial_name>")
    print("  subject <SUBJECT>            (e.g. subject CSCI)")
    print("  day <DAYSOFWEEK>             (e.g. MWF, TR, MW)")
    print("  quit/exit")
    print()

def main():
    catalog = Catalog(DB_PATH)

    

    while True:
        
        try:
            printCommandList()
            cmd = input("courses> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not cmd:
            continue

        if cmd in ("quit", "exit", ".q"):
            break

        parts = cmd.split(maxsplit=1)
        action = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        

        if action == "search" and arg:
            results = catalog.search(arg)
            rows = [
                (s.subject + s.number, s.section, s.title, s.prof, "".join(s.days), s.start, s.end)
                for s in results
            ]
            print(tabulate(rows, headers=["Course", "Section", "Title", "Prof", "Days", "Start", "End"], tablefmt="psql"))

        elif action == "course" and arg:
            secs = catalog.sections_for(arg)
            rows = [
                (s.crn, s.subject + s.number, s.section, s.title, s.prof, "".join(s.days), s.start, s.end)
                for s in secs
            ]
            print(tabulate(rows, headers=["CRN", "Course", "Section", "Title", "Prof", "Days", "Start", "End"], tablefmt="psql"))

        elif action == "subject" and arg:
            subj = arg.upper()
            secs = [s for s in catalog.sections if s.subject.upper() == subj]
            rows = [
                (s.crn, s.subject + s.number, s.section, s.title, s.prof, "".join(s.days), s.start, s.end)
                for s in secs
            ]
            print(tabulate(rows, headers=["CRN", "Course", "Section", "Title", "Prof", "Days", "Start", "End"], tablefmt="psql"))

        elif action == "prof" and arg:
            secs = catalog.sections_for_prof(arg)
            rows = [
                (s.crn, s.subject + s.number, s.section, s.title, s.prof, "".join(s.days), s.start, s.end)
                for s in secs
            ]
            print(tabulate(rows, headers=["CRN", "Course", "Section", "Title", "Prof", "Days", "Start", "End"], tablefmt="psql"))
        
        elif action == "day" and arg:
            pattern = arg.upper().replace(" ", "")
            secs = [
                s for s in catalog.sections
                if all(ch in s.days for ch in pattern) and len(s.days) == len(pattern)
            ]
            rows = [
                (s.crn, s.subject + s.number, s.section, s.title, s.prof, "".join(s.days), s.start, s.end)
                for s in secs
            ]
            print(tabulate(rows, headers=["CRN", "Course", "Section", "Title", "Prof", "Days", "Start", "End"], tablefmt="psql"))

        else:
            print("Unknown or incomplete command.")

if __name__ == "__main__":
    main()
