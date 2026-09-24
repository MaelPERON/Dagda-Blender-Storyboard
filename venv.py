import sys
import venv
import subprocess
import logging
from os.path import expandvars
from pathlib import Path


logger = logging.getLogger(__name__)


class BlendVenv():
    def __init__(self, venv_path: str):
        self.venv_path = Path(expandvars(venv_path))

    @property
    def is_venv_created(self) -> bool:
        return (
            self.venv_path.exists()
            and (self.venv_path / "Scripts" / "activate").exists()
        )

    @property
    def site_packages_path(self) -> Path:
        if sys.platform == "win32":
            return self.venv_path / "Lib" / "site-packages"
        else:
            return (
                self.venv_path
                / "lib"
                / f"python{sys.version_info.major}.{sys.version_info.minor}"
                / "site-packages"
            )

    def create(self):
        """Create a virtual environment if it doesn't exist,
        then reference it."""

        if not self.venv_path.exists() or not self.is_venv_created:
            logger.debug(f"Creating virtual environment at {self.venv_path}")
            venv.create(
                self.venv_path,
                with_pip=True
            )
            logger.info("Virtual environment created.")

        self.reference()

    def reference(self):
        """Add the virtual environment's site-packages to sys.path"""

        site_packages = self.site_packages_path
        if site_packages.exists():
            if str(site_packages) not in sys.path:
                sys.path.append(str(site_packages))
                logger.info(f"Added {site_packages} to sys.path")
            else:
                logger.debug(f"{site_packages} is already in sys.path")
        else:
            logger.debug(f"Site-packages path {site_packages} does not exist.")

    def install_requirements(self, requirements_file: str):
        """Install packages from a requirements.txt file
        into the virtual environment"""

        logger.debug(f"Installing requirements from {requirements_file}")
        pip_executable = self.venv_path / "Scripts" / "pip.exe"
        if pip_executable.exists():
            subprocess.run(
                [str(pip_executable), "install", "-r", requirements_file],
                check=True
            )
            logger.debug(f"Installed requirements from {requirements_file}")
        else:
            logger.debug(
                "pip executable not found in the virtual environment.")
