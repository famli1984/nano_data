#!/usr/bin/env python3
"""
CalDAV → Obsidian Markdown sync for Family Assistant.

Posteo calendars:
  - Familie  → shared family calendar (all events, prefixed with AFMRS initials)
  - Andi
  - Suse

Local output (Areas/Family/):
  - kalender.md            combined overview
  - kalender-andi.md
  - kalender-suse.md
  - kalender-familie.md    full family calendar
  - kalender-felix.md      copy of Familie
  - kalender-marie.md      copy of Familie
  - kalender-rosa.md       copy of Familie

Run from repo root:  python Agents/Support/Kalender/sync_calendar.py
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    import caldav
    from icalendar import Calendar
    from dotenv import load_dotenv
except ImportError:
    print("Missing dependencies. Run: pip install caldav icalendar python-dotenv")
    sys.exit(1)

# Load .env from repo root (three levels up from this script)
REPO_ROOT = Path(__file__).parent.parent.parent.parent
load_dotenv(REPO_ROOT / ".env")

PRINCIPAL_URL = f"https://posteo.de:8443/calendars/{os.environ['POSTEO_USERNAME']}/"
USERNAME      = os.environ["POSTEO_USERNAME"]
PASSWORD      = os.environ["POSTEO_PASSWORD"]
DAYS_AHEAD    = int(os.getenv("DAYS_AHEAD", "30"))
CAL_DIR       = REPO_ROOT / "Areas" / "Family"

# Posteo display name → internal label
CALENDAR_LABELS = {
    "Familie": "Familie",
    "Andi":    "Andi",
    "Suse":    "Suse",
}

# Individual output files per person/label
PERSON_FILES = {
    "Andi":    "kalender-andi.md",
    "Suse":    "kalender-suse.md",
    "Familie": "kalender-familie.md",
    # Kids share the Familie calendar
    "Felix":   "kalender-felix.md",
    "Marie":   "kalender-marie.md",
    "Rosa":    "kalender-rosa.md",
}


def parse_events_from_calendar(cal_obj, label):
    start = datetime.now(timezone.utc)
    end   = start + timedelta(days=DAYS_AHEAD)
    events = []
    try:
        raw = cal_obj.search(start=start, end=end, event=True, expand=True)
    except Exception as e:
        print(f"  Warnung: Fehler beim Lesen von '{label}': {e}")
        return events

    for vevent in raw:
        ical = Calendar.from_ical(vevent.data)
        for component in ical.walk():
            if component.name != "VEVENT":
                continue
            summary  = str(component.get("SUMMARY", "(Kein Titel)"))
            dtstart  = component.get("DTSTART").dt
            dtend    = component.get("DTEND", component.get("DTSTART")).dt
            location = str(component.get("LOCATION", ""))
            desc     = str(component.get("DESCRIPTION", ""))

            if hasattr(dtstart, "hour"):
                dtstart  = dtstart.astimezone(None)
                dtend    = dtend.astimezone(None)
                start_str = dtstart.strftime("%H:%M")
                if dtend.date() > dtstart.date():
                    time_str = f"{start_str}–{dtend.strftime('%d.%m. %H:%M')}"
                else:
                    time_str = f"{start_str}–{dtend.strftime('%H:%M')}"
                sort_key  = dtstart.replace(tzinfo=None)
                is_allday = False
            else:
                # All-day event (dtstart/dtend are date objects)
                last = dtend - timedelta(days=1) if dtend > dtstart else dtstart
                if last > dtstart:
                    time_str = f"{dtstart.strftime('%d.%m.')}–{last.strftime('%d.%m.')}"
                else:
                    time_str = "Ganztag"
                sort_key  = datetime(dtstart.year, dtstart.month, dtstart.day)
                is_allday = True

            events.append({
                "summary":  summary,
                "date":     sort_key,
                "time":     time_str,
                "is_allday": is_allday,
                "location": location,
                "desc":     desc.strip(),
            })
    return events


def render_events(events, title, tags, person=None):
    now = datetime.now()
    lines = [
        "---",
        f"tags: [{', '.join(tags)}]",
        f"updated: {now.strftime('%Y-%m-%d %H:%M')}",
        "calendar_source: posteo",
        f"person: {person or tags[1].capitalize()}",
        "type: calendar",
        f"sync_days_ahead: {DAYS_AHEAD}",
        "---",
        "",
        f"# 📅 {title}",
        "",
        f"> Automatisch synchronisiert am {now.strftime('%d.%m.%Y um %H:%M')} Uhr  ",
        f"> Zeigt Ereignisse der nächsten {DAYS_AHEAD} Tage.",
        "",
    ]

    if not events:
        lines.append(f"_Keine Termine in den nächsten {DAYS_AHEAD} Tagen._")
        return "\n".join(lines) + "\n"

    current_day = None
    for ev in sorted(events, key=lambda e: e["date"]):
        day       = ev["date"].strftime("%Y-%m-%d")
        day_label = ev["date"].strftime("%A, %d. %B %Y")
        if day != current_day:
            if current_day is not None:
                lines.append("")
            lines.append(f"## {day_label}")
            current_day = day
        loc = f" 📍 {ev['location']}" if ev["location"] else ""
        lines.append(f"- **{ev['time']}** – {ev['summary']}{loc}")
        if ev["desc"]:
            for dl in ev["desc"].splitlines():
                lines.append(f"  > {dl}")

    return "\n".join(lines) + "\n"


def render_combined(events_by_label):
    now = datetime.now()
    lines = [
        "---",
        "tags: [calendar, family, overview]",
        f"updated: {now.strftime('%Y-%m-%d %H:%M')}",
        "calendar_source: posteo",
        "person: Familie",
        "type: calendar",
        f"sync_days_ahead: {DAYS_AHEAD}",
        "---",
        "",
        "# 📅 Familienkalender – Übersicht",
        "",
        f"> Automatisch synchronisiert am {now.strftime('%d.%m.%Y um %H:%M')} Uhr  ",
        f"> Zeigt Ereignisse der nächsten {DAYS_AHEAD} Tage.",
        "",
    ]

    for label in ["Andi", "Suse", "Familie"]:
        events = events_by_label.get(label, [])
        lines.append(f"## 👤 {label}")
        lines.append("")
        if not events:
            lines.append(f"_Keine Termine._")
            lines.append("")
            continue
        current_day = None
        for ev in sorted(events, key=lambda e: e["date"]):
            day       = ev["date"].strftime("%Y-%m-%d")
            day_label = ev["date"].strftime("%A, %d. %B %Y")
            if day != current_day:
                if current_day is not None:
                    lines.append("")
                lines.append(f"### {day_label}")
                current_day = day
            loc = f" 📍 {ev['location']}" if ev["location"] else ""
            lines.append(f"- **{ev['time']}** – {ev['summary']}{loc}")
            if ev["desc"]:
                for dl in ev["desc"].splitlines():
                    lines.append(f"  > {dl}")
        lines.append("")

    return "\n".join(lines) + "\n"


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✓ {path.relative_to(REPO_ROOT)}")


def main():
    client    = caldav.DAVClient(url=PRINCIPAL_URL, username=USERNAME, password=PASSWORD)
    principal = client.principal()

    events_by_label = {}
    for cal in principal.calendars():
        server_name = cal.get_display_name()
        label = CALENDAR_LABELS.get(server_name)
        if label is None:
            continue
        print(f"  Lese '{label}' ({server_name}) ...")
        events = parse_events_from_calendar(cal, label)
        print(f"    → {len(events)} Termine")
        events_by_label[label] = events

    if not events_by_label:
        print("Keine bekannten Kalender gefunden.")
        sys.exit(1)

    familie_events = events_by_label.get("Familie", [])

    print("\nSchreibe lokale Kalender-Kopien:")

    # Individual files for Andi and Suse
    for person in ["Andi", "Suse"]:
        evs = events_by_label.get(person, [])
        md  = render_events(evs, f"Kalender – {person}", ["calendar", person.lower()], person=person)
        write(CAL_DIR / PERSON_FILES[person], md)

    # Familie aggregated
    md = render_events(familie_events, "Kalender – Familie", ["calendar", "familie"], person="Familie")
    write(CAL_DIR / PERSON_FILES["Familie"], md)

    # Individual kid copies (same events, different file/label)
    for kid in ["Felix", "Marie", "Rosa"]:
        md = render_events(familie_events, f"Kalender – {kid}", ["calendar", kid.lower()], person=kid)
        write(CAL_DIR / PERSON_FILES[kid], md)

    # Combined overview
    md = render_combined(events_by_label)
    write(CAL_DIR / "kalender.md", md)

    print("\nFertig.")


if __name__ == "__main__":
    main()

