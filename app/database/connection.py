import os
from collections.abc import Generator

from fastapi import HTTPException, status
from psycopg import Connection, OperationalError, connect
from psycopg.rows import dict_row


def get_connection() -> Generator[Connection, None, None]:
    """Provide one PostgreSQL connection per request."""
    try:
        connection = connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            dbname=os.getenv("POSTGRES_DB"),
            row_factory=dict_row,
        )
    except OperationalError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is unavailable.",
        ) from error

    try:
        yield connection
    finally:
        connection.close()
