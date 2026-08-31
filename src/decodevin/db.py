import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Optional

DB_PATH = Path(os.environ.get("DECODEVIN_DB_PATH", "decodevin.db"))


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS vin_cache (
                vin TEXT PRIMARY KEY,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                model_year TEXT NOT NULL,
                body_class TEXT NOT NULL
            )
            """
        )


def get_cached(vin: str) -> Optional[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM vin_cache WHERE vin = ?", (vin,)
        ).fetchone()


def insert_cached(vin: str, make: str, model: str, model_year: str, body_class: str) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO vin_cache (vin, make, model, model_year, body_class)
            VALUES (?, ?, ?, ?, ?)
            """,
            (vin, make, model, model_year, body_class),
        )


def delete_cached(vin: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM vin_cache WHERE vin = ?", (vin,))
        return cursor.rowcount > 0


def fetch_all() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM vin_cache").fetchall()
