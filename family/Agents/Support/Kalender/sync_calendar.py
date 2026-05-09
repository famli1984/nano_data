#!/usr/bin/env python3
"""
CalDAV → Markdown sync for Family Assistant. No external deps required.

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
  - aufgaben.md            combined task overview
  - aufgaben-andi.md
  - aufgaben-suse.md
  - aufgaben-familie.md

Run from repo root:  python groups/family/Agents/Support/Kalender/sync_calendar.py
"""

import base64
import os
import re
import ssl
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SCRIPT_DIR    = Path(__file__).resolve().parent
GROUP_ROOT    = SCRIPT_DIR.parent.parent.parent      # groups/family/
NANOCLAW_ROOT = GROUP_ROOT.parent.parent             # nanoclaw/
CAL_DIR       = GROUP_ROOT / "Areas" / "Family"
DAYS_AHEAD    = int(os.getenv("DAYS_AHEAD", "30"))

def _load_env():
    env_path = NANOCLAW_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())

_load_env()

USERNAME = os.environ.get("POSTEO_USERNAME", "")
PASSWORD = os.environ.get("POSTEO_PASSWORD", "")
if not USERNAME or not PASSWORD:
    print("ERROR: POSTEO_USERNAME / POSTEO_PASSWORD not set", file=sys.stderr)
    sys.exit(1)

CALDAV_BASE = f"https://posteo.de:8443/calendars/{USERNAME.split('@')[0]}/"

CALENDAR_LABELS = {"Familie": "Familie", "Andi": "Andi", "Suse": "Suse"}

PERSON_FILES = {
    "Andi":    "kalender-andi.md",
    "Suse":    "kalender-suse.md",
    "Familie": "kalender-familie.md",
    "Felix":   "kalender-felix.md",
    "Marie":   "kalender-marie.md",
    "Rosa":    "kalender-rosa.md",
}

TASK_FILES = {
    "Andi":    "aufgaben-andi.md",
    "Suse":    "aufgaben-suse.md",
    "Familie": "aufgaben-familie.md",
}

# ---------------------------------------------------------------------------
# CalDAV helpers
# ---------------------------------------------------------------------------

_ctx   = ssl.create_default_context()
_token = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

def _request(method, url, data=None, extra_headers=None):
    headers = {
        "Authorization": f"Basic {_token}",
        "Content-Type":  "application/xml; charset=utf-8",
    }
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers, method=method, data=data)
    return urllib.request.urlopen(req, context=_ctx)


def list_calendars():
    """Return list of (display_name, href) tuples."""
    body = b"""<?xml version="1.0" encoding="utf-8"?>
<propfind xmlns="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">
  <prop><displayname/><resourcetype/></prop>
</propfind>"""
    with _request("PROPFIND", CALDAV_BASE, data=body, extra_headers={"Depth": "1"}) as r:
        raw = r.read().decode()
    ns = {"d": "DAV:", "c": "urn:ietf:params:xml:ns:caldav"}
    root = ET.fromstring(raw)
    result = []
    for resp in root.findall("d:response", ns):
        href = resp.findtext("d:href", namespaces=ns)
        rt   = resp.find(".//d:resourcetype", ns)
        if rt is None or rt.find("c:calendar", ns) is None:
            continue
        name = resp.findtext(".//d:displayname", namespaces=ns) or ""
        result.append((name.strip(), href))
    return result


def _ics_prop(ical_text, prop):
    """Extract first value of a property from raw iCalendar text."""
    for line in ical_text.splitlines():
        # handle property params like DTSTART;TZID=...:value
        if line.startswith(prop + ":") or line.startswith(prop + ";"):
            return line.split(":", 1)[-1].strip()
    return ""


def _parse_dt(value):
    """Parse iCalendar DTSTART/DTEND/DUE value; returns date or datetime."""
    value = value.strip()
    try:
        if len(value) == 8:  # all-day: YYYYMMDD
            from datetime import date
            return datetime(int(value[:4]), int(value[4:6]), int(value[6:8]))
        if value.endswith("Z"):
            dt = datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
            return dt.astimezone().replace(tzinfo=None)
        return datetime.strptime(value[:15], "%Y%m%dT%H%M%S")
    except Exception:
        return None


def _report(href, component):
    """Fetch all VEVENT or VTODO objects from a calendar."""
    url  = f"https://posteo.de:8443{href}"
    body = f"""<?xml version="1.0" encoding="utf-8"?>
<C:calendar-query xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">
  <D:prop><D:getetag/><C:calendar-data/></D:prop>
  <C:filter>
    <C:comp-filter name="VCALENDAR">
      <C:comp-filter name="{component}"/>
    </C:comp-filter>
  </C:filter>
</C:calendar-query>""".encode()

    with _request("REPORT", url, data=body, extra_headers={"Depth": "1"}) as r:
        raw = r.read().decode()

    objects = []
    for block in re.split(r"(?=BEGIN:VCALENDAR)", raw):
        if f"BEGIN:{component}" not in block:
            continue
        # extract the component block
        m = re.search(rf"BEGIN:{component}(.+?)END:{component}", block, re.DOTALL)
        if m:
            objects.append(m.group(0).replace("\\n", "\n"))
    return objects


def fetch_events(href, label):
    cutoff = datetime.now() + timedelta(days=DAYS_AHEAD)
    events = []
    for raw in _report(href, "VEVENT"):
        summary  = _ics_prop(raw, "SUMMARY")
        dtstart  = _parse_dt(_ics_prop(raw, "DTSTART"))
        dtend_v  = _ics_prop(raw, "DTEND") or _ics_prop(raw, "DTSTART")
        dtend    = _parse_dt(dtend_v)
        location = _ics_prop(raw, "LOCATION")
        desc     = _ics_prop(raw, "DESCRIPTION").replace("\\n", "\n").strip()

        if dtstart is None or dtstart > cutoff:
            continue

        # format time string
        orig_line = next((l for l in raw.splitlines() if l.startswith("DTSTART")), "")
        is_allday = "T" not in _ics_prop(raw, "DTSTART") and len(_ics_prop(raw, "DTSTART")) == 8
        if is_allday:
            time_str = "Ganztag"
        else:
            ts = dtstart.strftime("%H:%M")
            te = dtend.strftime("%H:%M") if dtend else ts
            if dtend and dtend.date() > dtstart.date():
                te = dtend.strftime("%d.%m. %H:%M")
            time_str = f"{ts}–{te}"

        events.append({
            "summary":  summary or "(Kein Titel)",
            "date":     dtstart,
            "time":     time_str,
            "location": location,
            "desc":     desc,
        })
    return events


def fetch_tasks(href, label):
    tasks = []
    for raw in _report(href, "VTODO"):
        status  = _ics_prop(raw, "STATUS").upper() or "NEEDS-ACTION"
        if status in ("COMPLETED", "CANCELLED"):
            continue
        summary  = _ics_prop(raw, "SUMMARY")
        due_raw  = _ics_prop(raw, "DUE")
        due_dt   = _parse_dt(due_raw) if due_raw else None
        priority = _ics_prop(raw, "PRIORITY")
        desc     = _ics_prop(raw, "DESCRIPTION").replace("\\n", "\n").strip()

        due_str = ""
        if due_dt:
            due_str = due_dt.strftime("%d.%m.%Y %H:%M") if due_dt.hour or due_dt.minute else due_dt.strftime("%d.%m.%Y")

        tasks.append({
            "summary":  summary or "(Kein Titel)",
            "due":      due_str,
            "due_sort": due_dt,
            "priority": int(priority) if priority.isdigit() else 0,
            "desc":     desc,
        })
    return tasks


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_events(events, title, tags, person=None):
    now   = datetime.now()
    lines = [
        "---",
        f"tags: [{', '.join(tags)}]",
        f"updated: {now.strftime('%Y-%m-%d %H:%M')}",
        "calendar_source: posteo",
        f"person: {person or title}",
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
    now   = datetime.now()
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
        lines.append(f"## 👤 {label}")
        lines.append("")
        evs = events_by_label.get(label, [])
        if not evs:
            lines.append("_Keine Termine._")
            lines.append("")
            continue
        current_day = None
        for ev in sorted(evs, key=lambda e: e["date"]):
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


def render_tasks(tasks, title, tags, person=None):
    now   = datetime.now()
    lines = [
        "---",
        f"tags: [{', '.join(tags)}]",
        f"updated: {now.strftime('%Y-%m-%d %H:%M')}",
        "calendar_source: posteo",
        f"person: {person or title}",
        "type: tasks",
        "---",
        "",
        f"# ✅ {title}",
        "",
        f"> Automatisch synchronisiert am {now.strftime('%d.%m.%Y um %H:%M')} Uhr",
        "",
    ]
    if not tasks:
        lines.append("_Keine offenen Aufgaben._")
        return "\n".join(lines) + "\n"

    def sort_key(t):
        if t["due_sort"] is None:
            return (1, datetime.max, t["priority"])
        return (0, t["due_sort"], t["priority"])

    for t in sorted(tasks, key=sort_key):
        due_part = f" – fällig: {t['due']}" if t["due"] else ""
        prio = " 🔴" if 1 <= t["priority"] <= 3 else (" 🟡" if 4 <= t["priority"] <= 6 else "")
        lines.append(f"- [ ] {t['summary']}{due_part}{prio}")
        if t["desc"]:
            for dl in t["desc"].splitlines():
                lines.append(f"  > {dl}")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✓ {path.relative_to(GROUP_ROOT)}")


def main():
    print(f"Lese Kalender von {CALDAV_BASE} ...")
    calendars = list_calendars()
    print(f"  Gefunden: {[n for n, _ in calendars]}")

    events_by_label = {}
    tasks_by_label  = {}

    for name, href in calendars:
        label = CALENDAR_LABELS.get(name)
        if label is None:
            continue
        print(f"  Lese '{label}' ...")
        evs  = fetch_events(href, label)
        tsks = fetch_tasks(href, label)
        print(f"    → {len(evs)} Termine, {len(tsks)} Aufgaben")
        events_by_label[label] = evs
        tasks_by_label[label]  = tsks

    if not events_by_label:
        print("Keine bekannten Kalender gefunden.", file=sys.stderr)
        sys.exit(1)

    familie_events = events_by_label.get("Familie", [])

    print("\nSchreibe Kalender-Dateien:")
    for person in ["Andi", "Suse"]:
        md = render_events(events_by_label.get(person, []),
                           f"Kalender – {person}", ["calendar", person.lower()], person=person)
        write(CAL_DIR / PERSON_FILES[person], md)

    md = render_events(familie_events, "Kalender – Familie", ["calendar", "familie"], person="Familie")
    write(CAL_DIR / PERSON_FILES["Familie"], md)

    for kid in ["Felix", "Marie", "Rosa"]:
        md = render_events(familie_events, f"Kalender – {kid}", ["calendar", kid.lower()], person=kid)
        write(CAL_DIR / PERSON_FILES[kid], md)

    write(CAL_DIR / "kalender.md", render_combined(events_by_label))

    print("\nSchreibe Aufgaben-Dateien:")
    for person in ["Andi", "Suse", "Familie"]:
        md = render_tasks(tasks_by_label.get(person, []),
                          f"Aufgaben – {person}", ["tasks", person.lower()], person=person)
        write(CAL_DIR / TASK_FILES[person], md)

    all_tasks = [t for ts in tasks_by_label.values() for t in ts]
    write(CAL_DIR / "aufgaben.md",
          render_tasks(all_tasks, "Aufgaben – Übersicht", ["tasks", "family", "overview"], person="Familie"))

    print("\nFertig.")


if __name__ == "__main__":
    main()
