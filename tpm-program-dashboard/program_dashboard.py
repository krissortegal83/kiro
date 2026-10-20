"""Technical Program Manager's simple dependency/risk report.

Standard-library-only, using fictional JSON milestones.
"""
import json
from datetime import date
from pathlib import Path


VALID_STATUSES = {"planned", "in_progress", "completed"}


def analyze_program(program: dict, as_of: date) -> dict:
    tasks = program.get("tasks", [])
    lookup = {task["id"]: task for task in tasks}
    if len(lookup) != len(tasks):
        raise ValueError("Duplicate task IDs")

    for task in tasks:
        if task.get("status") not in VALID_STATUSES:
            raise ValueError(f"Invalid status for {task['id']}")
        date.fromisoformat(task["due_date"])

    visiting: set[str] = set()
    visited: set[str] = set()

    def verify_dependencies(task_id: str) -> None:
        if task_id in visiting:
            raise ValueError(f"Circular dependency at {task_id}")
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in lookup[task_id].get("depends_on", []):
            if dependency not in lookup:
                raise ValueError(f"Missing dependency {dependency}")
            verify_dependencies(dependency)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in lookup:
        verify_dependencies(task_id)

    findings = []
    for task in tasks:
        flags = []
        if task["status"] != "completed":
            if date.fromisoformat(task["due_date"]) < as_of:
                flags.append("overdue")
            if any(lookup[dependency]["status"] != "completed" for dependency in task.get("depends_on", [])):
                flags.append("blocked_by_dependency")
            if int(task.get("risk_score", 0)) >= 4:
                flags.append("high_risk")
        findings.append({
            "id": task["id"],
            "title": task["title"],
            "team": task["team"],
            "status": task["status"],
            "flags": flags,
        })

    completed = sum(task["status"] == "completed" for task in tasks)
    critical = sum(bool(item["flags"]) for item in findings)
    health = "at_risk" if critical else "on_track"
    return {
        "program": program.get("name", "Program"),
        "health": health,
        "completed": completed,
        "total": len(tasks),
        "findings": findings,
    }


def markdown_report(analysis: dict) -> str:
    lines = [
        f"# {analysis['program']} — Program Status",
        "",
        f"**Overall health:** {analysis['health'].replace('_', ' ').title()}",
        f"**Milestones completed:** {analysis['completed']}/{analysis['total']}",
        "",
        "| ID | Workstream | Milestone | Status | Attention |",
        "|---|---|---|---|---|",
    ]
    for item in analysis["findings"]:
        flags = ", ".join(item["flags"]) or "none"
        lines.append(f"| {item['id']} | {item['team']} | {item['title']} | {item['status']} | {flags} |")
    lines.extend(["", "## Suggested TPM actions", ""])
    for item in analysis["findings"]:
        if item["flags"]:
            lines.append(f"- **{item['id']}**: confirm owner and mitigation for {', '.join(item['flags'])}.")
    if not any(item["flags"] for item in analysis["findings"]):
        lines.append("- Continue milestone monitoring and stakeholder updates.")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sample_path = Path(__file__).with_name("sample_program.json")
    sample = json.loads(sample_path.read_text(encoding="utf-8"))
    report = analyze_program(sample, as_of=date(2026, 10, 20))
    print(markdown_report(report))
