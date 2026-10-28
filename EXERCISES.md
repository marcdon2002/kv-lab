# Lab Exercises – Campus App

Start Redis and open the Redis command line:

```
docker compose up -d --wait
docker compose exec redis redis-cli
```

You are now at the `127.0.0.1:6379>` prompt. Type `exit` to leave it.
Use the key prefix **`ex:`** for your own keys.

---

## Exercise 1 · Sessions (Keys & TTL)

1. Store a login session: token `t1` belongs to user `42`. It should be valid for **15 minutes**.
2. Check how many seconds are left.
3. Make the session valid for 1 more hour (*hint:* `EXPIRE`).
4. What do `TTL` and `GET` return for a token that never existed?

## Exercise 2 · Choose the right data structure

| Requirement                                                      | Your key | Type | Commands |
|------------------------------------------------------------------|----------|------|----------|
| a) Profile of user 42 (name, course, points); add 5 points        |          |      |          |
| b) Count **unique** visitors of the campus event (u1, u2, u1, u3) |          |      |          |
| c) Show the **Top 3** of the quiz (Ana 40, Ben 70, Cem 55, Dana 90) |        |      |          |
| d) A queue of e-mails to send, processed **first in, first out**  |          |      |          |

Try each one in `redis-cli` and check the result.

## Exercise 3 · Group design (2–3 people, 6 minutes)

Design a Redis model for a **campus event app**:

- **Login:** a session is valid for 15 minutes
- **Visitors:** every user ID counts only once
- **Quiz:** show the Top 3 by points, points can change
- **Failure:** what happens to each part if Redis restarts without persistence?

For each part write down: **key name · data type · command(s) · one limitation.**

## Bonus

- Cache: Store `ex:cache:course:DB` with a TTL of 60 s. Why can the cached room be wrong after a change in
  the source database? How do you fix it?
- Two people run `GET ex:counter` → +1 → `SET ex:counter …` at the same time. What goes wrong?
  Which single command avoids it?
- `MULTI` → `SET ex:a 1` → `INCR ex:name` (a text value!) → `SET ex:b 2` → `EXEC`.
  Which keys exist afterwards? Is that a rollback?

---

### Command cheat sheet

| Type       | Write                         | Read                                    |
|------------|-------------------------------|-----------------------------------------|
| String     | `SET k v [EX s] [NX]`, `INCR k` | `GET k`, `TTL k`, `EXISTS k`          |
| Hash       | `HSET k f v …`, `HINCRBY k f n` | `HGET k f`, `HGETALL k`               |
| List       | `LPUSH k v`, `RPUSH k v`       | `RPOP k`, `LRANGE k 0 -1`              |
| Set        | `SADD k m …`                   | `SCARD k`, `SMEMBERS k`, `SISMEMBER k m` |
| Sorted Set | `ZADD k score m`, `ZINCRBY k n m` | `ZRANGE k 0 2 REV WITHSCORES`       |
| Any key    | `DEL k`, `EXPIRE k s`          | `TYPE k`, `KEYS ex:*` (only in the lab!) |
