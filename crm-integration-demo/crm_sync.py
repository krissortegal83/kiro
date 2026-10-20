"""Safe, deterministic CRM sync demonstration with synthetic records.

No network calls, API credentials or private production data are used.
"""
from datetime import datetime, timezone
from pprint import pprint


def parse_timestamp(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("updated_at must be an ISO 8601 string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("updated_at requires a timezone")
    return parsed.astimezone(timezone.utc)


def normalize_contact(raw: dict) -> dict:
    email = str(raw.get("email", "")).strip().lower()
    name = str(raw.get("name", "")).strip()
    if "@" not in email or not name:
        raise ValueError("A valid email and nonempty name are required")
    timestamp = str(raw.get("updated_at", ""))
    parse_timestamp(timestamp)
    return {"email": email, "name": name, "updated_at": timestamp}


def synchronize(existing: list[dict], incoming: list[dict]) -> dict:
    """Merge two contact feeds by email without overwriting newer records.

    Returns contacts and an audit log. A repeated event is idempotent.
    Equal-timestamp conflicting values are surfaced instead of silently lost.
    """
    merged: dict[str, dict] = {}
    audit: list[dict] = []

    for raw in existing:
        contact = normalize_contact(raw)
        email = contact["email"]
        previous = merged.get(email)
        if previous is None or parse_timestamp(contact["updated_at"]) > parse_timestamp(previous["updated_at"]):
            merged[email] = contact

    for raw in incoming:
        contact = normalize_contact(raw)
        email = contact["email"]
        previous = merged.get(email)
        if previous is None:
            merged[email] = contact
            action = "created"
        else:
            new_time = parse_timestamp(contact["updated_at"])
            old_time = parse_timestamp(previous["updated_at"])
            if new_time > old_time:
                merged[email] = contact
                action = "updated"
            elif new_time < old_time:
                action = "stale_ignored"
            elif contact == previous:
                action = "unchanged"
            else:
                action = "timestamp_conflict"
        audit.append({"contact": email, "action": action})

    return {
        "contacts": sorted(merged.values(), key=lambda item: item["email"]),
        "audit": audit,
    }


if __name__ == "__main__":
    original = [
        {"email": "alex@example.org", "name": "Alex Rivera", "updated_at": "2026-10-01T10:00:00Z"}
    ]
    events = [
        {"email": " ALEX@example.org ", "name": "Alex Rivera", "updated_at": "2026-10-01T10:00:00Z"},
        {"email": "bea@example.org", "name": "Bea Gomez", "updated_at": "2026-10-18T14:00:00Z"},
        {"email": "alex@example.org", "name": "Alex R.", "updated_at": "2026-10-19T11:00:00Z"},
    ]
    pprint(synchronize(original, events))
