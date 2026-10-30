"""
Database Engine and Schema Initialization for AgriGuard AI.
Uses SQLite for zero-dependency local execution, with clean relational structure
fully compatible with PostgreSQL for production deployment.
"""

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional
from contextlib import contextmanager

from app.config import settings

DB_FILE = Path(__file__).resolve().parent.parent / "agri_guard.db"


def get_db_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with dict row factory."""
    conn = sqlite3.connect(str(DB_FILE))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def db_session():
    """Context manager for safe database transactions."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Creates tables and indexes if they do not exist."""
    with db_session() as conn:
        cursor = conn.cursor()

        # 1. Crops table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            common_name TEXT NOT NULL,
            common_name_ta TEXT NOT NULL,
            scientific_name TEXT,
            category TEXT NOT NULL,
            description TEXT,
            description_ta TEXT,
            icon TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 2. Disease Classes table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS disease_classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_code TEXT UNIQUE NOT NULL,
            crop_code TEXT NOT NULL,
            disease_name TEXT NOT NULL,
            disease_name_ta TEXT NOT NULL,
            disease_type TEXT NOT NULL, -- fungal, bacterial, viral, pest, healthy, nutrient_deficiency
            severity TEXT DEFAULT 'Moderate',
            symptoms TEXT,
            symptoms_ta TEXT,
            causes TEXT,
            causes_ta TEXT,
            environmental_conditions TEXT,
            prevention TEXT,
            prevention_ta TEXT,
            ipm_methods TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (crop_code) REFERENCES crops (code) ON DELETE CASCADE
        );
        """)

        # 3. Verified Agricultural Guidance table (Strict verification citations)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agricultural_guidance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_code TEXT NOT NULL,
            target_disease_or_pest TEXT NOT NULL,
            treatment_category TEXT NOT NULL, -- fungicide, insecticide, bactericide, biological, cultural, organic
            active_ingredient TEXT,
            approved_product_name TEXT,
            dosage_guidance TEXT,
            non_chemical_control TEXT NOT NULL,
            prevention_practices TEXT NOT NULL,
            source_org TEXT NOT NULL, -- ICAR, DPPQS, TNAU, CIBRC
            source_url TEXT,
            reference_citation TEXT NOT NULL,
            jurisdiction TEXT DEFAULT 'India (CIBRC / ICAR Approved Package)',
            approved_label_restrictions TEXT,
            safety_precautions TEXT NOT NULL,
            harvest_waiting_period_days INTEGER DEFAULT 0,
            verification_date TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (crop_code) REFERENCES crops (code) ON DELETE CASCADE
        );
        """)

        # 4. Analysis History table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            crop_name TEXT NOT NULL,
            crop_name_ta TEXT,
            disease_name TEXT NOT NULL,
            disease_name_ta TEXT,
            disease_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            is_healthy INTEGER NOT NULL,
            is_uncertain INTEGER DEFAULT 0,
            growth_stage TEXT,
            district TEXT,
            image_filename TEXT,
            image_data_url TEXT,
            symptoms_summary TEXT,
            alternatives_json TEXT,
            guidance_json TEXT,
            feedback_status TEXT DEFAULT 'none',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 5. User Feedback table (Separated for data integrity)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id TEXT NOT NULL,
            feedback_type TEXT NOT NULL, -- correct, incorrect, poor_image, expert_required
            comment TEXT,
            crop_name TEXT,
            predicted_disease TEXT,
            reviewed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (analysis_id) REFERENCES analysis_history (id) ON DELETE CASCADE
        );
        """)

        # 6. Advisory Contacts table (Official KVK, Kisan Call Centers, Universities)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS advisory_contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            organization TEXT NOT NULL,
            service_type TEXT NOT NULL, -- toll_free_helpline, agricultural_university, kvk, web_portal
            phone TEXT,
            email TEXT,
            website TEXT,
            state_region TEXT,
            notes TEXT
        );
        """)

        # 7. Application Settings table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS application_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Create indices for fast querying
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_timestamp ON analysis_history(timestamp DESC);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_crop ON analysis_history(crop_name);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_guidance_crop ON agricultural_guidance(crop_code);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_guidance_target ON agricultural_guidance(target_disease_or_pest);")
