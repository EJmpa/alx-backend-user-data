#!/usr/bin/env python3
"""
Module for encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns a salted, hashed password, which is a byte string.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Returns True if the provided password matches the hashed
    password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
