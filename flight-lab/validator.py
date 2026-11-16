"""Row validation: airport list loading, single-row checks, record building."""

import math
import re
from datetime import datetime

_ID = re.compile(r"[A-Za-z0-9]{2,8}")
_CODE = re.compile(r"[A-Z]{3}") 
_DT = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}")


def load_airports(path: str) -> set[str]:
    """Read an airport list file and return the set of codes.

    One code per line. Strip whitespace; skip blank lines and lines
    starting with '#'.
    """
    with open(path, encoding="utf-8") as fh:
        return {
            s
            for line in fh
            if (s := line.strip())
            and not s.startswith("#")
        }

def parse_dt(s: str) -> datetime | None:
    if not _DT.fullmatch(s):
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M")
    except ValueError:
        return None

def validate_row(fields: list[str], airports: set[str]) -> str | None:
    """Check one CSV row (fields as returned by csv.reader, not yet stripped).

    Return None if the row is valid, otherwise the error code of the
    FIRST failing check (checks 1-11 in the specification, in order).
    Does not check for duplicates.
    """
    if len(fields) != 6:
        return "WRONG_FIELD_COUNT"
    fid, org, dst, dep, arr, price = (f.strip() for f in fields)
    if not all((fid, org, dst, dep, arr, price)):
        return "MISSING_FIELD"
    if not _ID.fullmatch(fid):
        return "INVALID_FLIGHT_ID"
    if not _CODE.fullmatch(org) or org not in airports: 
        return "INVALID_ORIGIN"
    if not _CODE.fullmatch(dst) or dst not in airports:
        return "INVALID_DESTINATION"
    if org == dst:
        return "SAME_ORIGIN_DESTINATION"
    dep_dt = parse_dt(dep)
    if dep_dt is None:
        return "INVALID_DEPARTURE"
    arr_dt = parse_dt(arr)
    if arr_dt is None:
        return "INVALID_ARRIVAL"
    if arr_dt <= dep_dt:
        return "ARRIVAL_NOT_AFTER_DEPARTURE"
    try:
        p = float(price)
    except ValueError:
        return "INVALID_PRICE"
    if not math.isfinite(p):
        return "INVALID_PRICE"
    if p <= 0:
        return "NON_POSITIVE_PRICE"
    return None

_KEYS = ("flight_id", "origin", "destination", "departure_datetime", "arrival_datetime", "price")
    
def to_record(fields: list[str]) -> dict:
    """Turn a valid row into a flight record dictionary.

    Keys: flight_id, origin, destination, departure_datetime,
    arrival_datetime (stripped strings) and price (float).
    """
    rec = dict(zip(_KEYS, (f.strip() for f in fields)))
    rec["price"] = float(rec["price"])
    return rec