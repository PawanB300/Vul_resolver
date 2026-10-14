from pathlib import Path


class PatchTool:

    def apply_patch(
        self,
        file_path: str,
        original: str,
        replacement: str,
    ):

        text = Path(file_path).read_text()

        if original not in text:
            raise ValueError("Original snippet not found.")

        updated = text.replace(
            original,
            replacement,
            1,
        )

        Path(file_path).write_text(updated)
