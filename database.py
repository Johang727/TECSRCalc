import sqlite3, os, bcrypt, secrets, time, datetime, jwt, sys
from random import randint

DB_FILE = "/var/lib/tecsrcalc/data.db"
DB_DIR = os.path.dirname(DB_FILE)

TOKEN_KEY = os.environ.get("TOKEN_KEY", "None")

if TOKEN_KEY == "None":
    print("Check .env! No token key found!")
    sys.exit(1)

def init_db() -> None:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at INTEGER,
                        trust FLOAT DEFAULT 50.0,
                        is_verified INTEGER DEFAULT 0,
                        permissions INTEGER DEFAULT 1,
                        submissions INTEGER DEFAULT 0,
                        auto_invalid INTEGER DEFAULT 0,
                        deletions INTEGER DEFAULT 0,
                        valid_subs INTEGER DEFAULT 0,
                        stored_subs INTEGER DEFAULT 0
                    );
                    """)

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS anon_submissions (
                        fingerprint_id TEXT NOT NULL,
                        submitted_at INTEGER NOT NULL
                    );
                    """)

    conn.commit()
    conn.close()

def register_user(username:str) -> dict:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    rand_len = randint(8, 12)
    raw_password = secrets.token_urlsafe(rand_len)

    cooked_password = bcrypt.hashpw(
        raw_password.encode("utf-8"),
        bcrypt.gensalt()
    )

    plated_password = cooked_password.decode("utf-8")

    try:
        current_time = int(time.time())

        cursor.execute(
            """
            INSERT INTO users (username, password_hash, created_at)
            VALUES (?, ?, ?);
            """,
            (username, plated_password, current_time)
        )

        conn.commit()

        return {
            "success" : "success",
            "username": username,
            "password": raw_password
        }
    except sqlite3.IntegrityError:
        return {
            "status": "error",
            "message": "Username likely taken."
        }

def verify_login(username:str, password:str) -> int:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password_hash FROM users WHERE username = ?;",
        (username,)
    )

    record = cursor.fetchone()
    conn.close()

    if not record:
        return -1
    
    user_id, hashbrown = record

    try:
        is_auth = bcrypt.checkpw(password.encode("utf-8"),
                                 hashbrown.encode("utf-8"))
        
        if is_auth:
            return user_id
        else:
            return -1
        
    except ValueError:
        return -1

def verify_token(tkn:str) -> int:
    if not tkn:
        return -1
    
    try:
        payload = jwt.decode(
            tkn,
            TOKEN_KEY,
            algorithms=["HS256"]
        )

        return payload.get("sub")

    except:
        return -1


def gen_token(usr_id:int) -> str:
    exp_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)

    payload = {
        "exp": exp_time,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "sub": usr_id
    }

    token = jwt.encode(
        payload=payload,
        key=TOKEN_KEY,
        algorithm="HS256"
    )

    return token

def get_usr_perms(usr_id:int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT permissions FROM users WHERE id = ?",
        (usr_id,)
    )

    lvl = cursor.fetchone()
    conn.close()

    return lvl[0] if lvl else 0