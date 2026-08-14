"""Business operations for the local vector database."""

from pathlib import Path
from typing import Dict

from app.config import config
from app.modules import vector_db


class DatabaseService:
    @staticmethod
    def get_stats() -> Dict:
        return vector_db.get_vector_db_stats()

    @staticmethod
    def clear_database() -> Dict:
        directory, vectors_path, metadata_path = vector_db._paths()
        directory.mkdir(parents=True, exist_ok=True)
        vectors_path.unlink(missing_ok=True)
        metadata_path.unlink(missing_ok=True)
        for temporary in directory.glob(".*.tmp"):
            temporary.unlink(missing_ok=True)
        return {"message": "Database cleared successfully", "status": "success"}

    @staticmethod
    def get_detailed_stats() -> Dict:
        directory, vectors_path, metadata_path = vector_db._paths()
        files = [path for path in (vectors_path, metadata_path) if path.exists()]
        return {
            "database_path": str(directory),
            "vectors_file": config.VECTOR_DB_FILE,
            "metadata_file": config.METADATA_FILE,
            "database_exists": len(files) == 2,
            "size_mb": round(sum(path.stat().st_size for path in files) / (1024 * 1024), 4),
        }
