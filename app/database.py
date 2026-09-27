import sqlite3
from pathlib import Path
from typing import Any

from .config import get_settings


def get_connection() -> sqlite3.Connection:
    settings = get_settings()

    database_path = Path(settings.database_path)

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        database_path,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


def init_db() -> None:
    connection = get_connection()

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS recommendation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            planner_type TEXT NOT NULL,
            input_json TEXT NOT NULL,
            result_json TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        );
        """
    )

    connection.commit()
    connection.close()


def fetch_one(
    query: str,
    params: tuple[Any, ...] = ()
):
    connection = get_connection()

    row = connection.execute(
        query,
        params
    ).fetchone()

    connection.close()

    return row


def fetch_all(
    query: str,
    params: tuple[Any, ...] = ()
):
    connection = get_connection()

    rows = connection.execute(
        query,
        params
    ).fetchall()

    connection.close()

    return rows


def execute(
    query: str,
    params: tuple[Any, ...] = ()
) -> int:
    connection = get_connection()

    cursor = connection.execute(
        query,
        params
    )

    connection.commit()

    row_id = cursor.lastrowid

    connection.close()

    return row_id