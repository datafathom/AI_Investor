import os
import shutil
import logging
from pathlib import Path
from services.system.secret_manager import get_secret_manager

logger = logging.getLogger(__name__)

class HousekeepingService:
    """
    Service for performing project maintenance, cleanup, and organization tasks.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HousekeepingService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.root = Path(os.getcwd())
        self.docs = self.root / "docs"
        self.logs = self.root / "logs"
        self.scripts_dir = self.root / "scripts"
        self.tests_dir = self.root / "tests"

    def organize_root(self):
        """Moves transient files and documentation from the root to their proper folders."""
        logger.info("Starting root organization...")
        
        # Ensure target directories exist
        subdirs = [
            self.docs / "cli", self.docs / "coverage", 
            self.docs / "testing", self.docs / "launch",
            self.logs
        ]
        for d in subdirs:
            d.mkdir(parents=True, exist_ok=True)

        moves = []
        
        # Define root documentation mapping
        doc_map = {
            "CLI_*": self.docs / "cli",
            "COVERAGE_*": self.docs / "coverage",
            "PRE_LAUNCH_*": self.docs / "launch",
            "TEST_RUNNER_*": self.docs / "testing",
            "LAUNCH_READINESS_REPORT.md": self.docs / "launch",
            "TESTING_IMPLEMENTATION_SUMMARY.md": self.docs / "testing",
            "FRONTEND_VERIFICATION_GUIDE.md": self.docs / "testing",
            "VERIFY_FRONTEND.md": self.docs / "testing",
            "CLI_UNIFICATION_COMPLETE.md": self.docs / "cli",
            "CLI_USAGE_GUIDE.md": self.docs / "cli",
        }

        for pattern, dest in doc_map.items():
            for f in self.root.glob(pattern):
                if f.is_file():
                    moves.append((f, dest / f.name))

        # Logs and transient text and json files (excluding requirements and git stuff)
        patterns = ["*.log", "*.txt", "*.json", "debug_body.html"]
        excluded_files = [
            "requirements.txt", "requirements-core.txt", "requirements-dev.txt",
            "requirements-linux-dev.txt", "requirements-linux-storage-host.txt",
            "requirements-ml.txt", "requirements-windows-dev.txt",
            "requirements-windows-storage-host.txt", "package.json", "package-lock.json",
            "tsconfig.json", "jsconfig.json"
        ]

        for pattern in patterns:
            for f in self.root.glob(pattern):
                if f.name not in excluded_files and "requirements" not in f.name:
                    moves.append((f, self.logs / f.name))

        self._execute_moves(moves)

    def archive_legacy_scripts(self):
        """Moves phase-specific and temporary scripts to an archive directory."""
        logger.info("Archiving legacy scripts and organizing scripts/ util...")
        archive_dir = self.scripts_dir / "archive" / "legacy_phases"
        build_archive_dir = self.scripts_dir / "archive" / "build_cycles"
        one_off_archive_dir = self.scripts_dir / "archive" / "one_off_tasks"
        util_dir = self.scripts_dir / "util"
        
        for d in [archive_dir, build_archive_dir, one_off_archive_dir, util_dir]:
            d.mkdir(parents=True, exist_ok=True)

        moves = []

        # Legacy Phases
        phase_patterns = ["verify_phase_*.py", "update_phase_*.py", "move_screenshots_phase*.py", 
                          "update_roadmap_*.py", "batch_update_checkmarks_*.py", "debug_phase_*.py"]
        for pattern in phase_patterns:
            for f in self.scripts_dir.glob(pattern):
                moves.append((f, archive_dir / f.name))

        # Build Cycle related
        build_patterns = ["update_plans*.py", "batch_update_checkmarks.py", "housekeeping_batch_update.py", 
                          "audit_remaining_sprints.py"]
        for pattern in build_patterns:
            for f in self.scripts_dir.glob(pattern):
                moves.append((f, build_archive_dir / f.name))

        # Utilities
        util_patterns = ["categorize_cli.py", "extract_api_*.py", "generate_lan_certs.py", 
                         "list_postman_folders.py", "migrate_test_handlers.py", "move_*.py", 
                         "stop_prev_runtimes.py"]
        for pattern in util_patterns:
            for f in self.scripts_dir.glob(pattern):
                moves.append((f, util_dir / f.name))

        # Remaining one-off scripts in scripts/ root
        for f in self.scripts_dir.glob("*.py"):
            if f.is_file() and f.parent == self.scripts_dir:
                moves.append((f, one_off_archive_dir / f.name))

        self._execute_moves(moves)

    def organize_tests(self):
        """Moves all tests from tests/ root to logical subfolders (unit/ or integration/)."""
        logger.info("Organizing tests/ root...")
        unit_dir = self.tests_dir / "unit"
        integration_dir = self.tests_dir / "integration"
        system_dir = self.tests_dir / "system"
        
        for d in [unit_dir, integration_dir, system_dir]:
            d.mkdir(parents=True, exist_ok=True)

        moves = []
        for f in self.tests_dir.glob("test_*.py"):
            if f.parent == self.tests_dir:
                # Basic heuristic: if it's a 'system' or 'integration' styled test
                if "integration" in f.name.lower():
                    moves.append((f, integration_dir / f.name))
                elif "system" in f.name.lower() or "selenium" in f.name.lower():
                    moves.append((f, system_dir / f.name))
                else:
                    # Default most single-component tests to unit/ for now
                    moves.append((f, unit_dir / f.name))

        # Rename non-test files in tests/system if they are actually tests
        self._execute_moves(moves)
        self._standardize_test_filenames(system_dir)

    def _standardize_test_filenames(self, target_dir):
        """Ensures all files in the target directory start with 'test_' for discovery."""
        for f in target_dir.glob("*.py"):
            if not f.name.startswith("test_") and f.name != "__init__.py":
                new_name = f"test_{f.name}"
                logger.info(f"Standardizing: {f.name} -> {new_name}")
                f.rename(target_dir / new_name)

    def _execute_moves(self, moves):
        """Handles the actual file movement with error recovery."""
        for src, dst in moves:
            try:
                if src.exists() and src != dst:
                    if dst.exists() and not dst.is_dir():
                        dst.unlink()
                    shutil.move(str(src), str(dst))
                    logger.debug(f"Moved: {src.name} -> {dst.parent.relative_to(self.root)}")
            except Exception as e:
                logger.error(f"Error moving {src.name}: {e}")

def get_housekeeping_service() -> HousekeepingService:
    return HousekeepingService()
