"""Concatenate an entire project into a single text file."""

import argparse
import fnmatch
from pathlib import Path


def find_gitignore(start_path):
    """Recursively search upward for a .gitignore file."""
    current = Path(start_path).resolve()
    while current != current.parent:
        gitignore_path = current / ".gitignore"
        if gitignore_path.exists():
            return gitignore_path
        current = current.parent
    return None


def parse_gitignore(gitignore_path):
    """Parse .gitignore and return a list of glob patterns."""
    patterns = []
    with gitignore_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def is_ignored(file_path, ignore_patterns, base_dir):
    """Check if file_path matches any ignore pattern."""
    relative_path = str(file_path.relative_to(base_dir))
    for pattern in ignore_patterns:
        # Convert .gitignore pattern to a usable fnmatch pattern
        if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(
            file_path.name, pattern,
        ):
            return True
    return False


def concatenate_project(input_dir, output_file):
    comment_syntax = {
        ".py": "#",
        ".r": "#",
        ".jl": "#",
        ".sh": "#",
        ".bash": "#",
        ".ps1": "#",
        ".bat": "REM",
        ".pl": "#",
        ".awk": "#",
        ".html": "-->",
        ".htm": "-->",
        ".xml": "-->",
        ".xhtml": "-->",
        ".js": "//",
        ".jsx": "//",
        ".ts": "//",
        ".tsx": "//",
        ".css": "*/",
        ".scss": "//",
        ".less": "//",
        ".java": "//",
        ".c": "//",
        ".h": "//",
        ".cpp": "//",
        ".cc": "//",
        ".cxx": "//",
        ".c++": "//",
        ".cs": "//",
        ".go": "//",
        ".swift": "//",
        ".kt": "//",
        ".kts": "//",
        ".dart": "//",
        ".php": "//",
        ".rb": "#",
        ".lua": "--",
        ".scala": "//",
        ".groovy": "//",
        ".vbs": "'",
        ".fs": "//",
        ".fsx": "//",
        ".hs": "--",
        ".ml": "(* *)",
        ".mli": "(* *)",
        ".clj": ";",
        ".cljs": ";",
        ".lisp": ";",
        ".lsp": ";",
        ".scm": ";",
        ".rkt": ";",
        ".erl": "%",
        ".ex": "#",
        ".exs": "#",
        ".json": "",
        ".yaml": "#",
        ".yml": "#",
        ".ini": ";",
        ".toml": "#",
        ".cfg": "#",
        ".conf": "#",
        ".properties": "#",
        ".sql": "--",
        ".md": "-->",
        ".markdown": "-->",
        ".rst": "..",
        ".tex": "%",
        ".latex": "%",
        ".make": "#",
        ".mk": "#",
        "Makefile": "#",
        ".dockerfile": "#",
        "Dockerfile": "#",
        ".env": "#",
        ".gitattributes": "#",
        ".gitignore": "#",
        ".editorconfig": "#",
    }

    input_path = Path(input_dir).resolve()
    output_path = Path(output_file).resolve()

    # Load .gitignore if it exists
    gitignore_path = find_gitignore(input_path)
    ignore_patterns = parse_gitignore(gitignore_path) if gitignore_path else []

    with output_path.open("w", encoding="utf-8") as outfile:
        for file_path in input_path.rglob("*"):
            if file_path.is_file():
                if is_ignored(file_path, ignore_patterns, input_path):
                    continue

                ext = file_path.suffix.lower()
                start_comment = comment_syntax.get(ext, "#")
                end_comment = ""

                if ext not in comment_syntax and file_path.name not in comment_syntax:
                    continue

                if ext in [".html", ".css", ".xml", ".md"]:
                    outfile.write(f"{start_comment} File: {file_path} {end_comment}\n")
                else:
                    outfile.write(
                        f"{start_comment} File: {file_path} {start_comment}\n",
                    )

                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    outfile.write(content)
                    outfile.write("\n\n")
                except Exception as e:
                    outfile.write(
                        f"{start_comment} Could not read file: {file_path} - Error: {e} {end_comment}\n\n",
                    )


def main():
    parser = argparse.ArgumentParser(
        description="Concatenate project files with file path comments.",
    )
    parser.add_argument(
        "input_directory", help="The path to the project directory to process.",
    )
    parser.add_argument(
        "output_filename", help="The name of the output text file (e.g., 'repo.txt').",
    )

    args = parser.parse_args()
    input_path = Path(args.input_directory)
    output_path = Path(args.output_filename)

    if not input_path.is_dir():
        print(f"Error: Input directory '{input_path}' not found.")
        return

    if output_path.suffix != ".txt":
        print("Warning: Output filename does not end with '.txt'. Appending '.txt'.")
        output_path = output_path.with_suffix(".txt")

    concatenate_project(input_path, output_path)
    print(f"All files from '{input_path}' concatenated to '{output_path}'.")


if __name__ == "__main__":
    main()
