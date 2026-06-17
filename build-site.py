#!/usr/bin/env python3
"""
Generate course-data.json — the navigation manifest the website (index.html) reads.
Re-run this whenever you add or rename modules/lessons/deliverables:

    python build-site.py

Then serve the folder (python -m http.server 8000) and open http://localhost:8000
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

def h1(relpath, fallback=None):
    """Return the first level-1 heading of a markdown file (backticks stripped)."""
    p = os.path.join(ROOT, relpath)
    try:
        with open(p, encoding="utf-8") as f:
            for line in f:
                if line.startswith("# "):
                    return line[2:].strip().replace("`", "")
    except OSError:
        pass
    return fallback or os.path.basename(relpath)

def exists(relpath):
    return os.path.isfile(os.path.join(ROOT, relpath))

def md_files(reldir):
    d = os.path.join(ROOT, reldir)
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if f.endswith(".md"))

# ---- Course group --------------------------------------------------------
course_children = []
for path, label in [
    ("README.md", "Home"),
    ("AUTHORING-GUIDE.md", "Authoring Guide"),
    ("course/curriculum.md", "Curriculum"),
    ("course/learning-path.md", "Learning Path"),
    ("course/weekly-study-plan.md", "Weekly Study Plan"),
]:
    if exists(path):
        course_children.append({"title": label, "path": path})

# ---- Modules group -------------------------------------------------------
modules_children = []
mod_root = os.path.join(ROOT, "modules")
module_dirs = sorted(d for d in os.listdir(mod_root)
                     if os.path.isdir(os.path.join(mod_root, d))) if os.path.isdir(mod_root) else []
lesson_count = 0
for mod in module_dirs:
    rel = f"modules/{mod}"
    readme = f"{rel}/README.md"
    lessons = []
    for f in md_files(rel):
        if re.match(r"^\d\d-", f):
            lessons.append({"title": h1(f"{rel}/{f}", f), "path": f"{rel}/{f}"})
    lesson_count += len(lessons)
    node = {"title": h1(readme, mod), "path": readme}
    if lessons:
        node["children"] = lessons
    modules_children.append(node)

# ---- Deliverables group --------------------------------------------------
deliv_children = []
if exists("deliverables/README.md"):
    deliv_children.append({"title": "Overview", "path": "deliverables/README.md"})

for folder, label in [
    ("deliverables/cheat-sheets", "Cheat Sheets"),
    ("deliverables/interview-prep", "Interview Prep"),
    ("deliverables/capstone-project", "Capstone Project"),
]:
    files = md_files(folder)
    if not files:
        continue
    files.sort(key=lambda f: (f != "README.md", f))  # README first
    kids = [{"title": ("Overview" if f == "README.md" else h1(f"{folder}/{f}", f)),
             "path": f"{folder}/{f}"} for f in files]
    deliv_children.append({"title": label, "children": kids})

# top-level deliverable docs (resources, exams, extras …)
top = [f for f in md_files("deliverables") if f != "README.md"]
for f in sorted(top):
    deliv_children.append({"title": h1(f"deliverables/{f}", f), "path": f"deliverables/{f}"})

data = {
    "title": h1("README.md", "Jetpack Compose Masterclass — 2026 Edition"),
    "nav": [
        {"label": "Course", "children": course_children},
        {"label": "Modules", "children": modules_children},
        {"label": "Deliverables", "children": deliv_children},
    ],
}

out = os.path.join(ROOT, "course-data.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"course-data.json written:")
print(f"  course docs : {len(course_children)}")
print(f"  modules     : {len(modules_children)}  ({lesson_count} lessons)")
print(f"  deliverables: {len(deliv_children)} entries")
