"""Running queries against the flight database."""

from validator import parse_dt

_RECORD_KEYS = ("flight_id", "origin", "destination", "departure_datetime", "arrival_datetime", "price")
#checks if its a number

def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)

_CHECKS = {
    "flight_id": lambda v: isinstance(v, str),
    "origin": lambda v: isinstance(v, str),
    "destination": lambda v: isinstance(v, str),
    "departure_datetime": lambda v: isinstance(v, str) and parse_dt(v) is not None,
    "arrival_datetime": lambda v: isinstance(v, str) and parse_dt(v) is not None,
    "price": _is_number,
    "min_price": _is_number,
    "sort_by": lambda v: v in _RECORD_KEYS,
    "order": lambda v: v in ("asc", "desc"),
    "limit": lambda v: type(v) is int and v >=0,
}

def _valid(query) -> bool:
    if not isinstance(query, dict):
        return False
    if "order" in query and "sort_by" not in query:
        return False
    return all(k in _CHECKS and _CHECKS[k](v) for k, v in query.items())

def _matches(f: dict, q: dict) -> bool:
    for k in ("flight_id", "origin", "destination"):
        if k in q and f[k] != q[k]:
            return False
    if "departure_datetime" in q and f["departure_datetime"] < q["departure_datetime"]:
        return False
    if "arrival_datetime" in q and f["arrival_datetime"] > q["arrival_datetime"]:
        return False
    if "price" in q and f["price"] > q["price"]:
        return False
    if "min_price" in q and f["price"] < q["min_price"]:
            return False
    return True

def run_query(db: list[dict], query: dict) -> dict:
    """Return one response entry for one query object.

    Valid query:   {"query": query, "matches": [...]}
    Invalid query: {"query": query, "error": "INVALID_QUERY", "matches": []}
    """
    if not _valid(query):
        return {"query": query, "error": "INVALID_QUERY", "matches": []}
    m = [f for f in db if _matches(f, query)]
    if "sort_by" in query:
        m = sorted(m, key=lambda f: f[query["sort_by"]], reverse=query.get("order") == "desc")
    if "limit" in query:
        m = m[:query["limit"]]
    return {"query": query, "matches": m}

def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    """Accept one query object or a list of them; always return a list."""
    if isinstance(queries, dict):
        queries = [queries]
    return [run_query(db, q) for q in queries]