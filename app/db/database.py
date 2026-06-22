# app/db/database.py
import sqlite3
import json
from datetime import datetime
import os

DB_PATH = "db/npc_world.db"

def get_connection():
    os.makedirs("db", exist_ok=True)  # 이 줄 추가
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # User 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # NPC 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS npcs (
            npc_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            persona TEXT,        -- JSON
            genetic_seed TEXT,   -- JSON
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Relationship 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity_a TEXT NOT NULL,
            entity_b TEXT NOT NULL,
            relation_type TEXT,
            strength REAL DEFAULT 0.0,
            world_id TEXT NOT NULL,
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Memory 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            memory_id INTEGER PRIMARY KEY AUTOINCREMENT,
            npc_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            summary TEXT,   -- JSON
            raw_log TEXT,
            updated_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Worlds 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS worlds (
            world_id TEXT PRIMARY KEY,
            owner_id TEXT NOT NULL,
            world_name TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(owner_id) REFERENCES users(user_id)
        )
    """)

    conn.commit()
    conn.close()