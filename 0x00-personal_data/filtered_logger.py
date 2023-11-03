#!/usr/bin/env python3
"""
Module for logging user data
"""
import re
import csv
import os
import mysql.connector
import logging
from typing import List, Tuple


PII_FIELDS: Tuple[str, str, str, str, str] = (
    "name", "email", "phone", "ssn", "password"
)


def get_logger() -> logging.Logger:
    """
    Returns a logger object with StreamHandler and RedactingFormatter.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(fields=PII_FIELDS)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the MySQL database.
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME", "")

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Returns the log message obfuscated
        """
        message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR
        )


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Returns the log message obfuscated
    """
    for field in fields:
        message = re.sub(f"{field}=.+?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


if __name__ == "__main__":
    logger = get_logger()

    with open("user_data.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            log_message = ""
            for field in row.keys():
                log_message += f"{field}={row[field]};"
            logger.info(log_message[:-1])
