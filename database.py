import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "plantpulse.db")


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disease TEXT NOT NULL,
            confidence REAL NOT NULL,
            affected_area REAL NOT NULL,
            severity TEXT NOT NULL,
            image_filename TEXT,
            heatmap_filename TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_scan(
    disease,
    confidence,
    affected_area,
    severity,
    image_filename=None,
    heatmap_filename=None
):

    connection = get_connection()
    cursor = connection.cursor()

    created_at = datetime.now().isoformat(timespec="seconds")

    cursor.execute("""
        INSERT INTO scans (
            disease,
            confidence,
            affected_area,
            severity,
            image_filename,
            heatmap_filename,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        disease,
        confidence,
        affected_area,
        severity,
        image_filename,
        heatmap_filename,
        created_at
    ))

    connection.commit()
    connection.close()


def get_scans():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM scans
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    scans = []

    for row in rows:
        scans.append(dict(row))

    connection.close()

    return scans