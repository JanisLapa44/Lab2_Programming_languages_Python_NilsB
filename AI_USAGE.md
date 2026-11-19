# AI Usage Disclosure

## Tools used

- Claude Code (Anthropic, model Claude Opus 5.5)

## Conversation links

There is no way to share terminal chats through a link so here is the full transcript:
=== USER ===
You are my programming languages (Python) assignment assistant. read the following assignment and explain what i need to do very simply and shortly as possible, human readable explanation with /ponytail skill. If you need the flight lab starter zip file its in this directory as a zip:

Graded lab: Flight query tool in Python
Overview
You will write a command-line Python program that validates flight schedule CSV files, stores valid flights as a JSON database, and answers queries against it. The assignment is worth 17.5% of the course grade and is graded automatically.

The program must:

Read one CSV file (-i) or every CSV file in a folder (-d).
Validate each row and assign every invalid row exactly one error code.
Write valid flights to a JSON database and invalid rows to errors.log.
Optionally load an existing JSON database (-j) instead of parsing CSVs.
Optionally run queries from a JSON file (-q) and write the results to a response file.
What to submit
Submit the URL of a GitHub repository. The required files (see Project structure) must sit at the top level, not inside a sub-folder.

Environment rules
Python 3.13: Your code is run with Python 3.13.
Standard library only: No third-party packages. Any import that is not part of the standard library makes the submission fail every test.
No network access during grading.
Time limit: each test run has up to 10 seconds. After 10 seconds the test fails automatically.
No tracebacks. Expected problems (missing files, bad JSON) must produce a clean Error: ... message on stderr, not a Python traceback.
A public test set (sample data plus expected outputs and a script to run them) is provided with the assignment. The final grade uses a larger hidden test set with different data, so code that only works on the sample files will lose points.

Starter files: download flight-lab-starter.zip from this assignment. It contains skeleton modules with the required function signatures, the sample data, an AI_USAGE.md template and the public test script. Its README.md explains how to use them.

Project structure and required functions
The auto-grader imports your modules and calls the functions below directly, so their file names, names and signatures must match exactly. You may add any other modules, classes and helper functions you like.

File	Required contents
flight_parser.py	main(argv: list[str] | None = None) -> int and the constants STUDENT_ID, FIRST_NAME, LAST_NAME
validator.py	load_airports(path: str) -> set[str], validate_row(fields: list[str], airports: set[str]) -> str | None, to_record(fields: list[str]) -> dict
csv_loader.py	parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]
query.py	run_query(db: list[dict], query: dict) -> dict, run_queries(db: list[dict], queries: dict | list) -> list[dict]
AI_USAGE.md	Your AI use disclosure (see AI use policy)
What each function does
main(argv) runs the whole program. argv is the argument list without the program name; None means use sys.argv[1:]. It returns the exit code instead of calling sys.exit().
load_airports(path) reads an airport list file and returns the set of codes.
validate_row(fields, airports) takes one row as produced by csv.reader (fields not yet stripped). It returns None if the row is valid, otherwise the error code of the first failing check (checks 1–11 in Validation). It does not check for duplicates.
to_record(fields) turns a valid row into a flight record dictionary (see Output files).
parse_files(paths, airports) processes the files in the order given. It returns the valid records and the error messages, and it performs the duplicate check across all the files. Each error message uses the <file name>:<line number>: <ERROR_CODE> | <free text> format, with no timestamp or level. parse_files does not write the log file itself.
run_query(db, query) returns one response entry for one query object.
run_queries(db, queries) accepts one query object or a list of them and always returns a list of response entries.
Rules for the entry point
Importing any of your modules must not run the program, read files or print anything. End flight_parser.py with:

if **name** == "**main**":
    sys.exit(main())
Set the student constants to your details in plain ASCII, with no spaces or underscores (for example FIRST_NAME = "Janis", LAST_NAME = "Berzins", STUDENT_ID = "241RDB123").

Command-line interface
Exactly one data source is required: -i, -d or -j. Use argparse.

Argument	Meaning
-i FILE	Parse a single CSV file.
-d FOLDER	Parse every file in the folder whose name ends in .csv (not sub-folders), in sorted filename order.
-j FILE	Load an existing JSON database instead of parsing CSVs.
-a FILE	Airport list file. Required with -i and -d; ignored with -j.
-o FILE	Output path for the JSON database. Default: db.json in the current directory. Only allowed with -i or -d.
-q FILE	Run the queries in this JSON file against the database (parsed or loaded).
-r FOLDER	Folder for the query response file. Default: the current directory.
-h	Show help and exit.
Behavior
With -i or -d, the program writes the database to the -o path and writes errors.log to the same folder as that database file.
With -j, the program writes no database and no errors.log.
With -q, the program also writes one response file to the -r folder (see Queries).
Folders given to -o and -r already exist; you do not need to create them.
The program may print progress or summaries to stdout. Stdout is not graded.
Exit codes
Code	When
0	Success, including when some rows were invalid or some queries were invalid.
1	A runtime problem: a file or folder does not exist or cannot be read, -d finds no .csv files, the -j or -q file is not valid JSON or has the wrong shape. Print one line starting with Error: to stderr.
2	A usage error: no data source, more than one data source, -a missing with -i/-d, -o used with -j, or an unknown argument. argparse produces this code by default; for the cases it cannot express, use parser.error(...).
Input files and validation
Every invalid row gets exactly one error code: the code of the first check it fails, in the order below.

CSV files
UTF-8 text. Lines may end in \n or \r\n; handle both.
Line 1 is always the header flight_id,origin,destination,departure_datetime,arrival_datetime,price. Skip it without validating.
A line containing only whitespace is a blank line: skip it, do not log it.
A line whose first non-whitespace character is # is a comment line: skip it, do not log it.
Split all other lines with the csv module. Strip leading and trailing whitespace from every field before checking it.
Line numbers are 1-based physical line numbers in the file, counting the header, blank lines and comment lines.
Airport list file
One airport code per line. Strip whitespace; skip blank lines and lines starting with #. Codes are compared exactly (case-sensitive).

Checks, in order
WRONG_FIELD_COUNT: the row does not have exactly 6 fields.
MISSING_FIELD: any field is empty after stripping.
INVALID_FLIGHT_ID: flight_id is not 2–8 ASCII letters or digits (^[A-Za-z0-9]{2,8}$).
INVALID_ORIGIN: origin is not 3 uppercase ASCII letters, or is not in the airport list.
INVALID_DESTINATION: the same rule for destination.
SAME_ORIGIN_DESTINATION: origin equals destination.
INVALID_DEPARTURE: departure_datetime is not a real date and time written exactly as YYYY-MM-DD HH:MM (zero-padded, 24-hour, single space).
INVALID_ARRIVAL: the same rule for arrival_datetime.
ARRIVAL_NOT_AFTER_DEPARTURE: arrival is equal to or earlier than departure.
INVALID_PRICE: price cannot be converted with float(), or the result is not finite (nan, inf).
NON_POSITIVE_PRICE: price is zero or negative.
DUPLICATE_FLIGHT: an earlier valid row (in this file or an earlier file of the same run) has the same flight_id and the same departure_datetime. Checked only in parse_files, after checks 1–11 pass.
Watch out: str.isalnum() and str.isupper() accept non-ASCII letters such as Ā or é, and datetime.strptime accepts 2025-1-5 9:3. Neither is enough on its own for checks 3–8.

Output files
JSON outputs are compared as parsed data, so indentation, spacing and key order do not matter. Number values are compared numerically (159.5 equals 159.50).

Database (db.json or the -o path)
A JSON array of flight records, in input order: files in the order processed, rows in line order. Each record has exactly these keys:

Key	Type	Value
flight_id	string	stripped input value
origin	string	stripped input value
destination	string	stripped input value
departure_datetime	string	stripped input value, YYYY-MM-DD HH:MM
arrival_datetime	string	stripped input value, YYYY-MM-DD HH:MM
price	number	float(price)
Write [] if there are no valid rows.

errors.log
Write this file with Python's logging module, not with open() and write(). Each invalid row is one WARNING record, in the same order as the database. The file is created on every -i or -d run, even when there are no errors.

Set the logger up like this:

import logging

logger = logging.getLogger("flight_parser")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")
handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(handler)
...
logger.warning("db.csv:13: INVALID_FLIGHT_ID | BA_BAD,RIX,LON,...")
...
logger.removeHandler(handler)
handler.close()
Two rules matter for grading. Do not use logging.basicConfig(), and remove and close the handler before main() returns, also when it returns early with an error (use try/finally). The autograder calls main() many times in one process, so a handler left behind writes duplicate lines into the next run's log or into the wrong file.

Each warning line in the file looks like this:

<YYYY-MM-DD HH:MM:SS> WARNING <file name>:<line number>: <ERROR_CODE> | <free text>
<file name> is the file's base name only (db.csv, not data/db.csv).
The autograder ignores the timestamp and every line that is not a WARNING. On WARNING lines it checks everything between WARNING and | . After | you may write any helpful text; we suggest the original line.
You may also log INFO lines (for example how many rows each file had) and ERROR lines for runtime problems. These are not graded, and an ERROR must still be printed to stderr as described in Exit codes.
Example:

2026-11-03 14:22:05 WARNING db.csv:13: INVALID_FLIGHT_ID | BA_BAD,RIX,LON,2025-11-15 11:00,INVALID_DATE,250.00
JSON database loaded with -j
It must be a JSON array of objects, otherwise exit with code 1. You may assume the records in it are valid.

Queries
A query file contains one query object or an array of query objects; anything else exits with code 1. A flight matches a query when it passes every condition in it (AND). An empty object {} matches every flight.

Allowed keys
Key	Value type	A flight matches when
flight_id	string	equal (case-sensitive)
origin	string	equal
destination	string	equal
departure_datetime	string YYYY-MM-DD HH:MM	flight departs at or after this time
arrival_datetime	string YYYY-MM-DD HH:MM	flight arrives at or before this time
price	number	flight price ≤ value
min_price	number	flight price ≥ value
sort_by	one of the six record keys	sort matches by that key
order	"asc" or "desc"	sort direction; default "asc"; requires sort_by
limit	integer ≥ 0	keep only the first limit matches, after sorting
Ordering
Without sort_by, matches keep database order. With sort_by, flights with equal sort values keep database order, in both directions (Python's sorted() with reverse=True already does this).

Invalid queries
A query is invalid if it has an unknown key, a value of the wrong type, a datetime not in the exact format, a negative limit, or order without sort_by. Booleans are not numbers. An invalid query does not stop the run: its entry gets an error and no matches.

Response file
Name: response_<STUDENT_ID>*<FIRST_NAME>*<LAST_NAME>_<YYYYMMDD_HHMM>.json, using the current local time, written to the -r folder. Write exactly one response file per run.

Content: always a JSON array with one entry per query, in query order.

[
  { "query": { "origin": "LHR" }, "matches": [ ... ] },
  { "query": { "colour": "red" }, "error": "INVALID_QUERY", "matches": [] }
]
query is the query object exactly as it appeared in the file.
matches is a list of full flight records.
error appears only on invalid queries, and its value is always INVALID_QUERY.
Worked example
The sample db.csv below has 7 valid rows and 12 invalid ones. These files and the expected outputs are part of the public test set.

airports.txt
AMS
ARN
BRU
CDG
DOH
DXB
FRA
HEL
JFK
LAX
LHR
OSL
RIX
SYD
WAW
db.csv
flight_id,origin,destination,departure_datetime,arrival_datetime,price
# === Valid flights ===
BA2490,LHR,JFK,2025-11-14 10:30,2025-11-14 13:05,489.99
LH172,FRA,RIX,2025-11-12 07:15,2025-11-12 10:30,159.50
FR1234,RIX,OSL,2025-11-15 08:00,2025-11-15 08:55,99.99
BT102,RIX,HEL,2025-11-14 09:40,2025-11-14 10:25,120.00
AA9999,JFK,LHR,2025-11-15 20:15,2025-11-16 08:10,550.00
DY4501,OSL,ARN,2025-12-01 06:00,2025-12-01 07:10,75.00
AF112,CDG,DXB,2025-11-20 21:10,2025-11-21 05:45,620.00

# === Invalid flights ===
BADLINE,NO_DATE,NO_TIME
BA_BAD,RIX,LON,2025-11-15 11:00,INVALID_DATE,250.00
SK404,OSL,RIX,2025-11-15 14:00,2025-11-15 12:00,120.00
W61025,XXX,RIX,2025-11-16 11:00,2025-11-16 13:00,80.00
QR1,DOH,SYD,INVALID_DATETIME,2025-11-17 23:30,980.00
KL1999,AMS,,2025-11-14 09:00,2025-11-14 11:15,180.00
AY503,HEL,RIX,2025-11-15 13:20,2025-11-15 14:15,-10.00
LH999999999,FRA,LAX,2025-11-13 09:30,2025-11-13 18:10,700.00
SN2902,BRU,LHR,2025-13-40 10:00,2025-13-40 12:00,99.99
BT650,RIX,RIX,2025-11-18 07:00,2025-11-18 08:00,60.00
FR1234,RIX,OSL,2025-11-15 08:00,2025-11-15 08:55,89.99
LO780,WAW,RIX,2025-11-19 16:00,2025-11-19 18:05,abc
Expected errors.log (graded part only)
Lines 1, 2, 10 and 11 are the header, comments and a blank line, so they are not logged. Timestamps and free text are left out below; in the file, each line looks like 2026-11-03 14:22:05 WARNING db.csv:12: WRONG_FIELD_COUNT | BADLINE,NO_DATE,NO_TIME.

db.csv:12: WRONG_FIELD_COUNT
db.csv:13: INVALID_FLIGHT_ID
db.csv:14: ARRIVAL_NOT_AFTER_DEPARTURE
db.csv:15: INVALID_ORIGIN
db.csv:16: INVALID_DEPARTURE
db.csv:17: MISSING_FIELD
db.csv:18: NON_POSITIVE_PRICE
db.csv:19: INVALID_FLIGHT_ID
db.csv:20: INVALID_DEPARTURE
db.csv:21: SAME_ORIGIN_DESTINATION
db.csv:22: DUPLICATE_FLIGHT
db.csv:23: INVALID_PRICE
Note line 13: BA_BAD also has an unknown destination and a bad arrival time, but only the first failing check (the flight ID) is reported. Line 20 fails on departure before arrival is checked.

Expected database
db.json holds the 7 rows from lines 3–9, in that order. The first record:

{
  "flight_id": "BA2490",
  "origin": "LHR",
  "destination": "JFK",
  "departure_datetime": "2025-11-14 10:30",
  "arrival_datetime": "2025-11-14 13:05",
  "price": 489.99
}
query.json and expected matches
[
  { "origin": "LHR", "destination": "JFK" },
  { "price": 200.00 },
  { "departure_datetime": "2025-11-15 00:00", "arrival_datetime": "2025-11-16 00:00" },
  { "origin": "RIX", "sort_by": "price", "order": "desc", "limit": 1 },
  { "destination": "XYZ", "colour": "red" }
]
Example	Query	Matching flights, in order
1	LHR to JFK	BA2490
2	price ≤ 200	LH172, FR1234, BT102, DY4501
3	departs ≥ 15 Nov 00:00 and arrives ≤ 16 Nov 00:00	FR1234
4	from RIX, most expensive first, top 1	BT102
5	unknown key colour	none; entry has "error": "INVALID_QUERY"
Each match in the response file is the full flight record, as in the database.

Examples of commands
python flight_parser.py -i data/db.csv -a data/airports.txt
python flight_parser.py -d data/flights/ -a data/airports.txt -o out/db.json
python flight_parser.py -j out/db.json -q data/query.json -r out/
python flight_parser.py -i data/db.csv -a data/airports.txt -q data/query.json
Grading
The assignment is graded out of 100 points by an auto-grader running hidden tests. Test groups are independent, so a broken CLI does not cost you the validation or query points earned through direct function calls.

Test groups
Group	What is tested	Points
A. Structure	Required files and functions exist, imports have no side effects, standard library only	5
B. Row validation	validate_row and to_record on single rows: every error code, the check order, edge cases	25
C. Parsing a file	-i: database and errors.log contents, logging setup and handler cleanup, line numbers, blank and comment lines, \r\n endings	20
D. CLI and folders	-d ordering and combined output, -o, -a, exit codes, usage errors, no tracebacks	15
E. Duplicates	DUPLICATE_FLIGHT within one file and across several files	5
F. Basic queries	-j loading, exact-match fields, datetime and price filters, AND logic, single object vs array	15
G. Extended queries	min_price, sort_by, order, limit, INVALID_QUERY	10
H. Response file	File name pattern, one file per run, entry structure	5
Points to grade
Points	Grade
95–100	10
85–94	9
75–84	8
65–74	7
55–64	6
45–54	5
35–44	4
below 35	not passed
Late submissions
Late submissions are not accepted. A repository URL submitted after the deadline gets 0 points for this assignment, and only commits pushed before the deadline are graded.

Before you submit
Run the public test script on your project. Passing it does not guarantee full points, because the hidden tests use different data, but failing it means you will lose points. Submissions without AI_USAGE.md are not graded.

AI use policy
You may use AI tools (ChatGPT, Claude, Copilot and others) for this assignment, provided you disclose how you used them. You have to provide URL links to the AI tool conversation and specify what part of the code was created, modified etc. using the AI tool. Disclosed use costs no points.

Your submission must include a file named AI_USAGE.md in the project root. If you used no AI tools, write "No AI tools were used." Otherwise, list:

Tools used: name and version, if known.
What you used them for: for example, "explaining argparse", "debugging the date validation", "generating test data".
Which parts of the code were AI-generated or substantially AI-assisted, by file or function name.
Key prompts: two or three of your most important prompts, copied or summarised.
What you changed or verified yourself: one or two sentences.
Submissions without AI_USAGE.md are not graded. Undisclosed AI use is treated as plagiarism under the university's academic integrity rules.

You are responsible for every line you submit. The exam covers the same concepts, so make sure you understand your code.

[tool: Skill] ponytail:ponytail

[tool: Bash] List directory and zip contents

=== CLAUDE ===
I read the assignment. One thing first: `flight-lab-starter.zip` isn't in this folder. The only zip here is `calc-tests.zip`, so download the starter before you write any code.

## What you're building

A command-line Python program that:

1. **Reads flight CSV files** (one file with `-i`, or a whole folder with `-d`).
2. **Checks each row** and splits the rows into good and bad.
3. **Saves the good flights** to `db.json` and logs the bad ones to `errors.log`.
4. **Answers searches** (`-q queries.json`) and writes the results to a `response_...json` file.

## The 5 files you hand in (top level of a GitHub repo)

| File | What it does |
|---|---|
| `validator.py` | Checks one row and returns `None` if it's fine, or the name of the first error it finds. Also turns a good row into a dict. |
| `csv_loader.py` | Goes through the files line by line. Skips the header, blank lines and `#` comments. Catches duplicate flights. |
| `query.py` | Filters the flights, sorts them, applies `limit`, and returns `INVALID_QUERY` for bad searches. |
| `flight_parser.py` | The `main()` function, the argparse setup, the exit codes and your student ID and name. |
| `AI_USAGE.md` | Says how you used AI, including the link to this chat. **Without it you get 0 points.** |

The starter zip already gives you these files with the function names filled in. You only write the bodies.

## The parts most likely to cost you points

- **Error order matters.** Each bad row gets only the **first** check it fails, out of 12 checks in a fixed order.
- **Be strict about formats.** `isalnum()` and `isupper()` accept letters like `Ā`, so use a regex such as `^[A-Z]{3}$`. Dates must be exactly `YYYY-MM-DD HH:MM`, so check the pattern with a regex **and** check it's a real date with `strptime`.
- **Prices:** `nan` and `inf` count as invalid, and 0 or below counts as a different error.
- **Line numbers** count every physical line in the file, including the header, comments and blank lines.
- **Logging:** use the exact logger setup given in the assignment, and remove the handler in a `try/finally` block. The grader calls `main()` many times, so a handler left behind writes duplicate lines into the next log.
- **Exit codes:** 0 means OK, 1 means a missing file or bad JSON (print `Error: ...` to stderr, never a traceback), 2 means wrong arguments.
- **Standard library only.** One outside import and every test fails.
- **Importing your files must do nothing.** No prints and no file reads at import time.

## Order to work in

1. `validator.py` (25 points, easiest to test on its own)
2. `csv_loader.py`
3. `flight_parser.py`
4. `query.py`
5. Run the public test script from the zip.
6. Write `AI_USAGE.md`, push to GitHub and submit the repo link.

I didn't open the starter zip because it isn't here, so I haven't checked its README or test script. The hidden tests use different data than the sample files, so code that only passes the sample will lose points.

=== USER ===
/ponytail:ponytail think of the easiest way to implement this while satisfying all task requirements, then   /superpowers:writing-plans write a development plan for this with hints as to which functions need to be written at each step to make it work

[tool: Skill] superpowers:writing-plans

=== CLAUDE ===
I'm using the writing-plans skill to create the implementation plan.

[tool: Bash] Check Python version and look for the starter zip

=== CLAUDE ===
The starter zip is there now. I'll extract it into an empty folder and read it so the plan matches the skeletons.

[tool: Bash] Extract starter zip to a temp folder and show README

[tool: Bash] Read skeleton modules, sample folder data and test script outline

[tool: Bash] Read how the public tests call main and check outputs

[tool: Bash] List test group classes and expected folder errors

=== CLAUDE ===
Now I'll write the plan.

[tool: Write] /home/nils/Documents/UNI/ProgrammingLanguages/docs/superpowers/plans/2026-11-16-flight-lab.md

[tool: Bash] Check AI usage and import-silence tests

=== CLAUDE ===
I wrote the plan and saved it to `docs/superpowers/plans/2026-11-16-flight-lab.md`. It sits outside the future repo, so it won't be submitted. I based it on the real starter zip: the skeleton files, the sample data and the public test script.

## The easiest way to do it

- **Keep the starter's 4 files.** Only add 3 small helper functions: `parse_dt` (validator), `_valid` (query), and `_load_json` / `_write_json` (main).
- **Use regex with `[0-9]`, not `\d`, plus `strptime`** for the strict checks. `\d` also matches non-English digits, which is the trap the assignment warns about.
- **Compare dates as plain text in queries.** `"2025-11-15 08:00" >= "2025-11-15 00:00"` already works because the format has a fixed width, so you never convert them to datetime objects.
- **`sorted(..., reverse=True)`** keeps equal flights in database order, which is exactly what the assignment asks for.
- **Catch argparse's exit inside `main`** with `except SystemExit as e: return e.code`. That gives exit code 2 for usage errors and 0 for `-h`, and `main()` still returns instead of exiting.
- **One `except (OSError, ValueError)`** covers every exit-code-1 case: missing files, bad JSON and bad encoding.
- **Use the public tests as your test suite.** Add only one small `tests/test_extra.py` for 5 edge cases they don't cover: non-ASCII letters, `nan`/`inf` prices, indented comments, logging handler cleanup, and bad query files.

## Which functions to write at each task

| Task | You write | Check with |
|---|---|---|
| 1 | `parse_dt`, `load_airports`, `validate_row`, `to_record` + your student constants | public test groups A and B |
| 2 | `parse_files` | `test_parse_files_function` |
| 3 | `_valid`, `run_query`, `run_queries` | public test group G |
| 4 | `main`, `_load_json`, `_write_json` | the full public test script, A to H |
| 5 | `AI_USAGE.md`, test on Python 3.13, push | Moodle submission |

Please review the plan. Which execution approach would you prefer?

- **Write it yourself, using the plan as a guide.** I'd recommend this: the exam covers the same concepts, and you have to understand every line you submit.
- **Native:** I implement every task here, then one reviewer checks the whole thing.
- **Subagent-driven:** a separate agent implements and reviews each task. That's overkill for 5 small tasks that build on each other.

You only have Python 3.10 on this machine, but grading uses 3.13, so run the final check in Codespaces before you submit. I didn't run any of the plan's code or the public tests yet, so treat the code hints as untested until Task 1 runs.

=== USER ===
can you update python?

[tool: Bash] Check OS and existing Python installers

[tool: Bash] Install uv and Python 3.13 in the home folder

[tool: Bash] Check the new commands are on PATH in a fresh shell

=== CLAUDE ===
Python 3.13 is installed and works in a new terminal. I'll update the plan's note about the local Python version to match.

[tool: Edit] /home/nils/Documents/UNI/ProgrammingLanguages/docs/superpowers/plans/2026-11-16-flight-lab.md

=== CLAUDE ===
Yes, Python 3.13 is now installed: version 3.13.18, available as `python3.13`.

- **Your old Python is untouched.** Typing `python3` still gives 3.10, because Ubuntu's own tools rely on it.
- **For the assignment, type `python3.13` instead of `python`**, for example `python3.13 tests/run_public_tests.py`. I updated the plan to say this.
- **It works in a new terminal.** In a terminal that was already open, run `source ~/.bashrc` first.
- **It went in without sudo**, using `uv`, Astral's Python installer, into your home folder (`~/.local`).

I didn't make `python` itself point to 3.13, because that could break system scripts. If you'd rather type plain `python`, add `alias python=python3.13` to your `~/.bashrc`.

=== USER ===
can you explain task 1 a bit more? do i use the preexisting zip files? or what do you mean by modify

=== CLAUDE ===
Yes, use the starter zip. It already contains every file you need. "Modify" means: open the file and replace the placeholder line `raise NotImplementedError` with your own code. You never create the 4 `.py` files from scratch.

## Task 1, step by step

### 1. Unzip the starter into your own project folder

```bash
cd ~/Documents/UNI/ProgrammingLanguages
unzip flight-lab-starter.zip            # creates the folder flight-lab-starter/
mv flight-lab-starter flight-lab        # optional rename
cd flight-lab
git init && git add -A && git commit -m "starter files"
```

This `flight-lab` folder becomes your GitHub repo later. The README suggests a private GitHub repo created from the template on Moodle, but a plain private repo you push this folder to works the same, as long as the files sit at the top level.

### 2. Put in your details

In `flight_parser.py`, change these 3 lines:

```python
STUDENT_ID = "000RDB000"   # -> your real ID, e.g. "241RDB123"
FIRST_NAME = "Firstname"   # -> "Nils"
LAST_NAME = "Lastname"     # -> your last name, plain ASCII (no ā, š...)
```

### 3. Fill in `validator.py`

Right now every function looks like this:

```python
def load_airports(path: str) -> set[str]:
    """..."""
    raise NotImplementedError      # <- delete this line, write your code here
```

Here is what each function should do:

| Function | In plain words | Hint |
|---|---|---|
| `load_airports(path)` | Read the airports file and return a set of codes like `{"RIX", "LHR", ...}`. | Loop over the lines and `.strip()` each one. Skip it if it's empty or starts with `#`. |
| `parse_dt(s)` (new helper you add) | Return a datetime if `s` is exactly `2025-11-14 10:30` and a real date, otherwise `None`. | First a regex `[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}` with `.fullmatch()`, then `datetime.strptime` inside `try/except ValueError`. |
| `validate_row(fields, airports)` | Return the name of the **first** problem, or `None` if the row is fine. | Check `len(fields) != 6` first. Then strip all the fields and do the 11 checks in order, each as `if bad: return "CODE"`. |
| `to_record(fields)` | Turn the 6 fields into the dict that goes into `db.json`. | Strip each value, and make `price` a `float(...)`. |

`validate_row` is just 11 `if` statements in a row. Here are the first few:

```python
if len(fields) != 6:
    return "WRONG_FIELD_COUNT"
f = [x.strip() for x in fields]
if any(x == "" for x in f):
    return "MISSING_FIELD"
if not re.fullmatch(r"[A-Za-z0-9]{2,8}", f[0]):
    return "INVALID_FLIGHT_ID"
# ... origin, destination, same airport, departure, arrival, order, price ...
return None
```

### 4. Add the extra test file

Create a new file `tests/test_extra.py` and paste in the test code from Task 1 Step 2 of the plan. It checks the tricky cases the public tests might miss, like `ĀB12`, `nan` and `2025-02-29`.

### 5. Run the tests

```bash
python3.13 -m unittest tests/test_extra.py -v
python3.13 -m unittest -k A_Structure -k B_RowValidation tests/run_public_tests.py
```

Before you write the code, these fail. When everything says `OK`, Task 1 is done, so commit:

```bash
git add -A && git commit -m "feat: row validation"
```

I left the full function bodies out on purpose, so you write them yourself (the exam covers this). If you get stuck on one check, ask and I'll walk you through it. The table and the code above are only hints, and none of it has been run yet.

=== USER ===
fill the ai usage md file accordingly, i wrote the code myself, but with an assisted development plan

[tool: Bash] Inspect project files, AI_USAGE.md and git history

[tool: Bash] Check git status and the nested flight-lab folder

[tool: Write] /home/nils/Documents/UNI/ProgrammingLanguages/Lab2_Programming_languages_Python_NilsB/AI_USAGE.md

=== CLAUDE ===
I filled in `AI_USAGE.md`. It says you wrote all the code yourself, and that Claude explained the assignment, wrote the development plan, explained Task 1 and helped install Python 3.13. The table lists each of your 4 files as "Explained: code written by me", with the specific hints the plan gave for each one.

Before you push, fix two things:

1. **Paste the conversation link.** I put `TODO` where it goes, because I can't see this chat's share link. The assignment requires the link.
2. **Check the last sentence.** It says you ran the public test script with Python 3.13. If you haven't yet, run `python3.13 tests/run_public_tests.py` before you submit, or change that sentence.

Also, `flight_parser.py` has changes you haven't committed yet, so commit it together with `AI_USAGE.md`.

=== USER ===
export this chat in text file

[tool: Bash] Find this conversation's transcript file

[tool: Bash] Inspect transcript format


## What I used them for

- Explaining the assignment in short, simple terms.
- Writing a step-by-step development plan: which functions to write in which order, what each one should do, and which public test group checks it.
- Explaining the first plan step (how to use the starter zip and what to put in `validator.py`) in more detail.
- Setting up Python 3.13 on my machine (installed with `uv` next to the system Python) so I could run the tests with the same version as the grader.

## Which parts of the code were AI-generated or substantially AI-assisted

I wrote all the code myself. The AI did not write any of the submitted functions. I used its plan as a guide.

| File | Function or part | How (generated / modified / explained) |
| --- | --- | --- |
| `validator.py` | `load_airports`, `parse_dt`, `validate_row`, `to_record` | Explained: the plan suggested the order of checks, regex with `[0-9]` instead of `\d`, and `strptime` inside `try/except`. Code written by me. |
| `csv_loader.py` | `parse_files` | Explained: the plan described skipping header/blank/comment lines, line numbering and the duplicate check. Code written by me. |
| `query.py` | `run_query`, `run_queries` and helpers | Explained: the plan listed the validation rule for each query key and suggested comparing the datetime strings directly. Code written by me. |
| `flight_parser.py` | `main` | Explained: the plan described the argparse setup, catching `SystemExit` to return exit code 2, and the order of steps. Code written by me. |

## Key prompts

1. "Read the following assignment and explain what I need to do very simply and as short as possible."
2. "Think of the easiest way to implement this while satisfying all task requirements, then write a development plan with hints as to which functions need to be written at each step."
3. "Can you explain task 1 a bit more? Do I use the preexisting zip files?"

## What I changed or verified myself

I wrote every function myself, following the plan only as a guide, and I organized some parts my own way (for example the `_is_number` and `_matches` helpers in `query.py`). I ran the public test script with Python 3.13 to check my code.
