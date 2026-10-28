"""Key-Value Databases Lab – Campus App demos.

Run via Docker (same command on Windows and macOS):
    docker compose run --rm lab check     # verify your setup
    docker compose run --rm lab 1         # Demo 1: keys & TTL
    docker compose run --rm lab 2         # Demo 2: data structures
    docker compose run --rm lab 3         # Demo 3: cache-aside
    docker compose run --rm lab 4         # Demo 4: atomicity
    docker compose run --rm lab reset     # delete all campus:* keys

Add --no-pause to run a demo without stopping for predictions.
"""

import os
import sys
import time

import redis

HOST = os.environ.get("REDIS_HOST", "localhost")
PAUSE = sys.stdin.isatty() and "--no-pause" not in sys.argv

BOLD, DIM, GREEN, RED, CYAN, RESET = (
    ("\033[1m", "\033[2m", "\033[32m", "\033[31m", "\033[36m", "\033[0m")
    if sys.stdout.isatty() else ("",) * 6
)


def connect():
    return redis.Redis(host=HOST, port=6379, decode_responses=True, socket_timeout=5)


def title(text):
    print(f"\n{BOLD}{'=' * 60}\n{text}\n{'=' * 60}{RESET}")


def step(text):
    print(f"\n{CYAN}▶ {text}{RESET}")


def fmt(result):
    """Show results roughly the way redis-cli prints them."""
    if result is None:
        return "(nil)"
    if result is True:
        return "OK"
    if isinstance(result, dict):
        result = [x for pair in result.items() for x in pair]
    if isinstance(result, list):
        flat = [x for item in result for x in (item if isinstance(item, tuple) else (item,))]
        return "\n  ".join(f"{i}) {x:g}" if isinstance(x, float) else f"{i}) {x}"
                           for i, x in enumerate(flat, 1))
    if isinstance(result, float):
        return f"{result:g}"
    return result


def cmd(text, result):
    print(f"  {DIM}redis>{RESET} {text}\n  {GREEN}{fmt(result)}{RESET}")
    return result


def predict(question):
    """Ask the audience to predict an output before it is shown."""
    print(f"\n  {BOLD}? Predict:{RESET} {question}")
    if PAUSE:
        input(f"  {DIM}[Enter] to run …{RESET}")


def note(text):
    print(f"  {DIM}→ {text}{RESET}")


def delete_prefix(r, prefix):
    keys = list(r.scan_iter(match=f"{prefix}*", count=500))
    if keys:
        r.delete(*keys)
    return len(keys)


# --------------------------------------------------------------------------- check

def check():
    title("Setup check")
    try:
        r = connect()
        cmd("PING", r.ping())
        info = r.info("server")
        cmd("INFO server → redis_version", info["redis_version"])
        cmd("SET campus:check ok EX 10", r.set("campus:check", "ok", ex=10))
        cmd("GET campus:check", r.get("campus:check"))
    except redis.exceptions.ConnectionError as exc:
        print(f"\n{RED}✗ Cannot reach Redis at '{HOST}:6379': {exc}{RESET}")
        print("  Is the lab running?  docker compose up -d --wait")
        sys.exit(1)
    print(f"\n{GREEN}{BOLD}✓ READY – your setup works. See you in the lab!{RESET}\n")


# --------------------------------------------------------------------------- demo 1

def demo1():
    r = connect()
    delete_prefix(r, "campus:d1:")
    title("Demo 1 · Keys & TTL – a login session expires")

    step("Store a session token for user:42, valid for 5 seconds")
    cmd("SET campus:d1:session:demo user:42 EX 5",
        r.set("campus:d1:session:demo", "user:42", ex=5))
    cmd("GET campus:d1:session:demo", r.get("campus:d1:session:demo"))
    cmd("TTL campus:d1:session:demo", r.ttl("campus:d1:session:demo"))

    predict("What does GET return after more than 5 seconds? And TTL?")
    print(f"  {DIM}waiting 6 seconds …{RESET}")
    time.sleep(6)
    cmd("GET campus:d1:session:demo", r.get("campus:d1:session:demo"))
    cmd("TTL campus:d1:session:demo", r.ttl("campus:d1:session:demo"))
    note("TTL -2 = key does not exist (any more).")

    step("A key without expiry")
    cmd("SET campus:d1:welcome \"Welcome to Aalen\"", r.set("campus:d1:welcome", "Welcome to Aalen"))
    predict("What is the TTL of a key that never got an expiry?")
    cmd("TTL campus:d1:welcome", r.ttl("campus:d1:welcome"))
    note("TTL -1 = key exists, but has no expiry.")

    step("SET … NX only writes if the key does not exist yet")
    cmd("SET campus:d1:lock app-1 NX", r.set("campus:d1:lock", "app-1", nx=True))
    predict("A second client tries the same SET … NX. Result?")
    cmd("SET campus:d1:lock app-2 NX", r.set("campus:d1:lock", "app-2", nx=True))
    cmd("GET campus:d1:lock", r.get("campus:d1:lock"))

    step("INCR counts directly on the server")
    cmd("INCR campus:d1:visits", r.incr("campus:d1:visits"))
    cmd("INCR campus:d1:visits", r.incr("campus:d1:visits"))
    note("Takeaway: expiry is part of the write path – it never happens by itself.")


# --------------------------------------------------------------------------- demo 2

def demo2():
    r = connect()
    delete_prefix(r, "campus:d2:")
    title("Demo 2 · Data structures – four requirements, four types")

    step("Hash: a user profile with fields")
    cmd("HSET campus:d2:user:42 name Mira course CS points 0",
        r.hset("campus:d2:user:42", mapping={"name": "Mira", "course": "CS", "points": 0}))
    cmd("HGET campus:d2:user:42 name", r.hget("campus:d2:user:42", "name"))
    predict("HINCRBY … points 10 – what is returned?")
    cmd("HINCRBY campus:d2:user:42 points 10", r.hincrby("campus:d2:user:42", "points", 10))
    cmd("HGETALL campus:d2:user:42", r.hgetall("campus:d2:user:42"))

    step("Set: unique visitors")
    predict("SADD u42 u42 u99 – how many members are in the set?")
    cmd("SADD campus:d2:visitors u42 u42 u99", r.sadd("campus:d2:visitors", "u42", "u42", "u99"))
    cmd("SCARD campus:d2:visitors", r.scard("campus:d2:visitors"))

    step("List: a job queue (LPUSH in, RPOP out)")
    cmd("LPUSH campus:d2:jobs job1", r.lpush("campus:d2:jobs", "job1"))
    cmd("LPUSH campus:d2:jobs job2", r.lpush("campus:d2:jobs", "job2"))
    predict("Which job comes out first with RPOP?")
    cmd("RPOP campus:d2:jobs", r.rpop("campus:d2:jobs"))
    note("LPUSH + RPOP = FIFO. A popped job is not yet reliably processed.")

    step("Sorted Set: the quiz leaderboard")
    cmd("ZADD campus:d2:quiz 95 Noah 80 Mira 70 Lea",
        r.zadd("campus:d2:quiz", {"Noah": 95, "Mira": 80, "Lea": 70}))
    cmd("ZRANGE campus:d2:quiz 0 2 REV WITHSCORES",
        r.zrange("campus:d2:quiz", 0, 2, desc=True, withscores=True))
    predict("Lea scores +30 points. What does the Top 3 look like now?")
    cmd("ZINCRBY campus:d2:quiz 30 Lea", r.zincrby("campus:d2:quiz", 30, "Lea"))
    cmd("ZRANGE campus:d2:quiz 0 2 REV WITHSCORES",
        r.zrange("campus:d2:quiz", 0, 2, desc=True, withscores=True))
    note("Takeaway: the right structure makes the business rule visible in the data model.")


# --------------------------------------------------------------------------- demo 3

SOURCE_DB = {"course:DB": {"name": "Database Technologies", "room": "A1"}}


def load_from_source(course_id):
    time.sleep(0.4)  # simulated slow source database
    return dict(SOURCE_DB[course_id])


def get_course(r, course_id):
    key = f"campus:d3:cache:{course_id}"
    cached = r.hgetall(key)
    if cached:
        print(f"  {GREEN}HIT{RESET}  read from Redis")
        return cached
    print(f"  {RED}MISS{RESET} → load from source database (slow) → store in Redis with EX 60")
    data = load_from_source(course_id)
    r.hset(key, mapping=data)
    r.expire(key, 60)
    return data


def demo3():
    r = connect()
    delete_prefix(r, "campus:d3:")
    title("Demo 3 · Cache-aside – fast, but up to date?")
    note("The source database is simulated in Python; the cache is real Redis. Not a benchmark.")

    step("Read the course twice")
    for _ in range(2):
        t0 = time.perf_counter()
        course = get_course(r, "course:DB")
        print(f"  room = {course['room']}   ({(time.perf_counter() - t0) * 1000:.0f} ms)")

    step("The room changes in the source database: A1 → B2")
    SOURCE_DB["course:DB"]["room"] = "B2"
    predict("Which room does the app show now, while the cache entry is still valid?")
    print(f"  room = {get_course(r, 'course:DB')['room']}")
    note("Stale data: the cache still holds the old copy.")

    step("Invalidate the cache entry explicitly")
    cmd("DEL campus:d3:cache:course:DB", r.delete("campus:d3:cache:course:DB"))
    print(f"  room = {get_course(r, 'course:DB')['room']}")
    note("Takeaway: TTL limits staleness, DEL invalidates – neither gives strict consistency.")


# --------------------------------------------------------------------------- demo 4

def demo4():
    r = connect()
    delete_prefix(r, "campus:d4:")
    title("Demo 4 · Atomicity – two updates, one result?")
    a, b = connect(), connect()  # two independent clients

    step("Client A and B both want to add +1 using GET → +1 in the client → SET")
    r.set("campus:d4:counter", 0)
    va = int(cmd("A: GET campus:d4:counter", a.get("campus:d4:counter")))
    vb = int(cmd("B: GET campus:d4:counter", b.get("campus:d4:counter")))
    cmd(f"A: SET campus:d4:counter {va + 1}", a.set("campus:d4:counter", va + 1))
    predict("B now writes its value. What is the final counter?")
    cmd(f"B: SET campus:d4:counter {vb + 1}", b.set("campus:d4:counter", vb + 1))
    cmd("GET campus:d4:counter", r.get("campus:d4:counter"))
    note(f"{RED}Lost update{RESET}{DIM}: two increments, but the result is 1.")

    step("Same thing with INCR – the server does the increment atomically")
    r.set("campus:d4:counter", 0)
    cmd("A: INCR campus:d4:counter", a.incr("campus:d4:counter"))
    cmd("B: INCR campus:d4:counter", b.incr("campus:d4:counter"))
    cmd("GET campus:d4:counter", r.get("campus:d4:counter"))

    step("MULTI/EXEC runs a block without foreign commands in between")
    predict("Inside the block INCR fails on a text value. Is 'done' still written?")
    pipe = r.pipeline(transaction=True)
    pipe.set("campus:d4:tx:label", "hello")
    pipe.incr("campus:d4:tx:label")
    pipe.set("campus:d4:tx:done", "yes")
    results = pipe.execute(raise_on_error=False)
    print(f"  {DIM}redis>{RESET} MULTI · SET label hello · INCR label · SET done yes · EXEC")
    for i, line in enumerate(results, 1):
        shown = f"(error) {line}" if isinstance(line, Exception) else fmt(line)
        print(f"  {GREEN}{i}) {shown}{RESET}")
    cmd("GET campus:d4:tx:done", r.get("campus:d4:tx:done"))
    note("No rollback: Redis transactions isolate, they do not undo runtime errors.")


# --------------------------------------------------------------------------- main

def reset():
    n = delete_prefix(connect(), "campus:")
    print(f"Deleted {n} campus:* keys.")


COMMANDS = {"check": check, "1": demo1, "2": demo2, "3": demo3, "4": demo4, "reset": reset}

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    choice = args[0] if args else "help"
    if choice not in COMMANDS:
        print(__doc__)
        sys.exit(0 if choice == "help" else 2)
    try:
        COMMANDS[choice]()
    except redis.exceptions.ConnectionError as exc:
        print(f"\n{RED}✗ Cannot reach Redis: {exc}\n  Start the lab first: docker compose up -d --wait{RESET}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
