#!/usr/bin/env python3
"""
Import ICS dump into Posteo "Familie" calendar with prefix naming.

Prefix convention:
  A = Andi, S = Suse, F = Felix, M = Marie, R = Rosa
  All five: AFMRS - Titel
  Only Andi: A - Titel

Modes:
  --overview   Write kalender-overview.md only (no upload)
  --import     Upload future events to Posteo Familie calendar
  --all        Do both (default)

Run from repo root:
  python Agents/Support/Kalender/import_ics.py --overview
  python Agents/Support/Kalender/import_ics.py --import
"""

import os
import sys
import re
import argparse
from datetime import datetime, timezone, date, timedelta
from pathlib import Path

try:
    from icalendar import Calendar, Event
    from dotenv import load_dotenv
except ImportError:
    print("Missing dependencies. Run: pip install caldav icalendar python-dotenv")
    sys.exit(1)

REPO_ROOT  = Path(__file__).parent.parent.parent.parent
ICS_FILE   = Path(__file__).parent / "andisusecalendar.ics"
OVERVIEW   = Path(__file__).parent / "kalender-overview.md"
load_dotenv(REPO_ROOT / ".env")

# Familie calendar name on Posteo (was "Kinder", renamed to "Familie")
FAMILIE_CALENDAR_NAME = "Familie"

MEMBERS = {
    "A": ["andi", "andy", "vater", "papa"],
    "S": ["suse", "mutter", "mama", "susanne"],
    "F": ["felix"],
    "M": ["marie"],
    "R": ["rosa"],
}

KINDER_KEYWORDS = ["kinder", "kids", "schule", "hausaufgabe", "turnen", "training",
                   "nachhilfe", "geburtstag", "zirkus", "augenarzt", "zahnarzt"]

# Events matching any of these keywords (in summary or location) are skipped entirely
IGNORE_KEYWORDS = ["feuerwehr"]

# Category per prefix — clients (Thunderbird, Apple Calendar) can color by category
PREFIX_CATEGORY = {
    "A":    "Andi",
    "S":    "Suse",
    "F":    "Felix",
    "M":    "Marie",
    "R":    "Rosa",
    "AS":   "Eltern",
    "AF":   "Andi-Felix",
    "AM":   "Andi-Marie",
    "AR":   "Andi-Rosa",
    "SF":   "Suse-Felix",
    "SM":   "Suse-Marie",
    "SR":   "Suse-Rosa",
    "FM":   "Kinder",
    "FR":   "Kinder",
    "MR":   "Kinder",
    "FMR":  "Kinder",
}

def get_category(prefix: str) -> str:
    if prefix in PREFIX_CATEGORY:
        return PREFIX_CATEGORY[prefix]
    if len(prefix) >= 3:
        return "Familie"
    return "Familie"

def detect_prefix(summary: str) -> str:
    s = summary.lower()
    found = set()

    for initial, keywords in MEMBERS.items():
        for kw in keywords:
            if kw in s:
                found.add(initial)

    # Keywords that imply all kids
    if any(kw in s for kw in KINDER_KEYWORDS) and not found.intersection({"F","M","R"}):
        found.update({"F", "M", "R"})

    # Default: Andi & Suse (it's their calendar dump)
    if not found:
        found = {"A", "S"}

    return "".join(sorted(found))


def format_event_title(summary: str) -> str:
    # Strip existing leading name prefixes like "Suse ", "Felix ", "Andi " etc.
    cleaned = re.sub(
        r"^(andi|andy|suse|felix|marie|rosa)\s+",
        "", summary.strip(), flags=re.IGNORECASE
    )
    prefix = detect_prefix(summary)
    return f"{prefix} - {cleaned}"


def parse_ics(ics_path: Path):
    raw = ics_path.read_bytes()
    cal = Calendar.from_ical(raw)
    events = []
    for component in cal.walk():
        if component.name != "VEVENT":
            continue
        summary = str(component.get("SUMMARY", "(Kein Titel)")).strip()
        location = str(component.get("LOCATION", "")).strip()

        # Skip ignored events
        combined = (summary + " " + location).lower()
        if any(kw in combined for kw in IGNORE_KEYWORDS):
            continue

        dtstart = component.get("DTSTART")
        dtend   = component.get("DTEND", component.get("DTSTART"))
        if dtstart is None:
            continue
        dtstart_dt = dtstart.dt
        dtend_dt   = dtend.dt if dtend else dtstart_dt

        # Normalize to comparable
        if isinstance(dtstart_dt, datetime):
            sort_key = dtstart_dt.astimezone(None).replace(tzinfo=None)
        else:
            sort_key = datetime(dtstart_dt.year, dtstart_dt.month, dtstart_dt.day)

        location = str(component.get("LOCATION", "")).strip()
        desc     = str(component.get("DESCRIPTION", "")).strip()
        uid      = str(component.get("UID", ""))

        is_allday = not isinstance(dtstart_dt, datetime)

        events.append({
            "uid":      uid,
            "summary":  summary,
            "new_title": format_event_title(summary),
            "dtstart":  dtstart_dt,
            "dtend":    dtend_dt,
            "sort_key": sort_key,
            "is_allday": is_allday,
            "location": location,
            "desc":     desc,
            "component": component,
        })

    events.sort(key=lambda e: e["sort_key"])
    return events


def write_overview(events):
    now = datetime.now()
    today = now.date()

    future = [e for e in events if e["sort_key"].date() >= today
              if isinstance(e["sort_key"], datetime)
              or e["sort_key"] >= today]

    # Group by month
    by_month: dict[str, list] = {}
    for ev in future:
        sk = e["sort_key"] if isinstance(e := ev, dict) else ev["sort_key"]
        month_key = sk.strftime("%Y-%m")
        by_month.setdefault(month_key, []).append(ev)

    lines = [
        "---",
        "tags: [calendar, overview, import]",
        f"updated: {now.strftime('%Y-%m-%d %H:%M')}",
        "---",
        "",
        "# 📅 Kalender-Übersicht (Import-Dump)",
        "",
        f"> Quelle: `andisusecalendar.ics`  ",
        f"> Generiert: {now.strftime('%d.%m.%Y %H:%M')}  ",
        f"> Gesamt: {len(events)} Einträge · Zukünftig: {len(future)}",
        "",
        "**Präfix-Legende:** A=Andi · S=Suse · F=Felix · M=Marie · R=Rosa",
        "",
    ]

    if not future:
        lines.append("_Keine zukünftigen Termine gefunden._")
    else:
        for month_key, month_events in sorted(by_month.items()):
            month_label = datetime.strptime(month_key, "%Y-%m").strftime("%B %Y")
            lines.append(f"## {month_label}")
            lines.append("")
            for ev in month_events:
                sk = ev["sort_key"]
                if ev.get("is_allday"):
                    start = ev["dtstart"]
                    end   = ev["dtend"]
                    # Convert datetime instances to date for comparison
                    if isinstance(start, datetime): start = start.date()
                    if isinstance(end, datetime):   end   = end.date()
                    # iCal DTEND for all-day is exclusive (day after last day)
                    last = end - timedelta(days=1) if end > start else start
                    if last > start:
                        day_str = f"{start.strftime('%d.%m.')}–{last.strftime('%d.%m.')}"
                    else:
                        day_str = start.strftime("%d.%m.")
                else:
                    # Timed event
                    start_dt = ev["dtstart"]
                    end_dt   = ev["dtend"]
                    if isinstance(start_dt, datetime):
                        start_dt = start_dt.astimezone(None)
                        end_dt   = end_dt.astimezone(None) if isinstance(end_dt, datetime) else None
                    start_str = start_dt.strftime("%d.%m. %H:%M")
                    # Show end date/time if the event spans into a different day
                    if end_dt and end_dt.date() > start_dt.date():
                        day_str = f"{start_str}–{end_dt.strftime('%d.%m. %H:%M')}"
                    else:
                        day_str = start_str
                loc = f" · 📍 {ev['location']}" if ev["location"] else ""
                lines.append(f"- `{day_str}` **{ev['new_title']}**{loc}")
            lines.append("")

    OVERVIEW.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Übersicht gespeichert: {OVERVIEW}")
    return future


def import_to_posteo(future_events):
    try:
        import caldav
    except ImportError:
        print("caldav not installed. Run: pip install caldav")
        sys.exit(1)

    username = os.environ["POSTEO_USERNAME"]
    password = os.environ["POSTEO_PASSWORD"]
    principal_url = f"https://posteo.de:8443/calendars/{username}/"

    client    = caldav.DAVClient(url=principal_url, username=username, password=password)
    principal = client.principal()

    familie_cal = None
    for cal in principal.calendars():
        if cal.get_display_name() == FAMILIE_CALENDAR_NAME:
            familie_cal = cal
            break

    if familie_cal is None:
        print(f"Kalender '{FAMILIE_CALENDAR_NAME}' nicht gefunden!")
        print("Verfügbare Kalender:", [c.get_display_name() for c in principal.calendars()])
        sys.exit(1)

    print(f"Importiere {len(future_events)} Termine in '{FAMILIE_CALENDAR_NAME}' ...")
    ok = 0
    fail = 0
    for ev in future_events:
        component = ev["component"]
        component["SUMMARY"] = ev["new_title"]

        # Set category based on prefix
        prefix   = ev["new_title"].split(" - ")[0].strip()
        category = get_category(prefix)
        if "CATEGORIES" in component:
            del component["CATEGORIES"]
        if "COLOR" in component:
            del component["COLOR"]
        component.add("CATEGORIES", category)

        from icalendar import Calendar as iCal
        wrapper = iCal()
        wrapper.add("prodid", "-//FamilyAssistant//EN")
        wrapper.add("version", "2.0")
        wrapper.add_component(component)
        try:
            familie_cal.save_event(wrapper.to_ical())
            ok += 1
        except Exception as e:
            print(f"  ✗ {ev['new_title']}: {e}")
            fail += 1

    print(f"Fertig: {ok} importiert, {fail} Fehler.")


def delete_all_from_posteo():
    try:
        import caldav
    except ImportError:
        print("caldav not installed.")
        sys.exit(1)

    username = os.environ["POSTEO_USERNAME"]
    password = os.environ["POSTEO_PASSWORD"]
    principal_url = f"https://posteo.de:8443/calendars/{username}/"

    client    = caldav.DAVClient(url=principal_url, username=username, password=password)
    principal = client.principal()

    familie_cal = None
    for cal in principal.calendars():
        if cal.get_display_name() == FAMILIE_CALENDAR_NAME:
            familie_cal = cal
            break

    if familie_cal is None:
        print(f"Kalender '{FAMILIE_CALENDAR_NAME}' nicht gefunden!")
        sys.exit(1)

    events = familie_cal.events()
    print(f"Lösche {len(events)} vorhandene Einträge aus '{FAMILIE_CALENDAR_NAME}' ...")
    for ev in events:
        try:
            ev.delete()
        except Exception as e:
            print(f"  ✗ Löschen fehlgeschlagen: {e}")
    print("Gelöscht.")


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--overview",  action="store_true", help="Only generate overview MD")
    group.add_argument("--import",    action="store_true", dest="do_import", help="Upload to Posteo")
    group.add_argument("--reimport",  action="store_true", help="Delete all existing + re-upload with colors")
    args = parser.parse_args()

    print(f"Lese {ICS_FILE.name} ...")
    events = parse_ics(ICS_FILE)
    print(f"  {len(events)} Einträge gefunden.")

    if args.reimport:
        delete_all_from_posteo()
        future = [e for e in events if e["sort_key"] >= datetime.now()]
        import_to_posteo(future)
        return

    do_overview = not args.do_import
    do_import   = args.do_import or (not args.overview)

    future = write_overview(events) if do_overview else [
        e for e in events if e["sort_key"] >= datetime.now()
    ]

    if do_import:
        import_to_posteo(future)


if __name__ == "__main__":
    main()
