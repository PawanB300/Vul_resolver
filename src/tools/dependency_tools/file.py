import re
from pathlib import Path


class UpdateFile:

    def read_file(self, path: str) -> str:
        return Path(path).read_text(encoding="utf-8")

    def write_file(self, path: str, content: str) -> None:
        Path(path).write_text(content, encoding="utf-8")

    def update_requirement(
        self,
        content: str,
        package: str,
        target_version: str,
    ) -> str:
        """
        Updates a package version in requirements.txt.

        Supports:
            flask==2.0.0
            flask>=2.0.0
            flask~=2.0
            flask<=2.0
            Flask==2.0.0

        Returns updated content.
        Raises ValueError if package is not found.
        """

        pattern = re.compile(
            rf"^(\s*{re.escape(package)}\s*)(==|>=|<=|~=|>|<)?\s*([^\s#]+)(.*)$",
            flags=re.MULTILINE | re.IGNORECASE,
        )

        replacement = rf"\1=={target_version}\4"

        updated, count = pattern.subn(replacement, content)

        if count == 0:
            raise ValueError(f"Package '{package}' not found in dependency file.")

        return updated

    def file_exists(self, path: str) -> bool:
        return Path(path).exists()

    def backup(self, path: str) -> str:
        """
        Creates path.bak before modifying.
        """
        file = Path(path)
        backup = file.with_suffix(file.suffix + ".bak")
        backup.write_text(
            file.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        return str(backup)
