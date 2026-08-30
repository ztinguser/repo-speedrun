#!/usr/bin/env python3
"""Collect stable metadata from an acquired Git repository."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath


MANIFEST_NAMES = {
    "cargo.toml",
    "cmakelists.txt",
    "composer.json",
    "compose.yaml",
    "compose.yml",
    "gemfile",
    "go.mod",
    "mix.exs",
    "package.json",
    "pom.xml",
    "pyproject.toml",
    "setup.cfg",
    "setup.py",
}

ENTRYPOINT_NAMES = {
    "__main__.py",
    "app.py",
    "cli.py",
    "index.js",
    "index.ts",
    "main.go",
    "main.py",
    "main.rs",
    "main.ts",
    "main.tsx",
    "server.js",
    "server.py",
    "server.ts",
}


class SnapshotError(RuntimeError):
    """Raised when repository metadata cannot be collected."""


def run_git(repository: Path, *arguments: str) -> str:
    command = [
        "git",
        "-C",
        str(repository),
        *arguments,
    ]

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        raise SnapshotError("git executable was not found") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        message = detail or f"git {' '.join(arguments)} failed"
        raise SnapshotError(message) from exc

    return result.stdout.strip()


def get_tracked_files(repository: Path) -> list[str]:
    output = run_git(repository, "ls-files", "-z")
    return sorted(path for path in output.split("\0") if path)


def is_manifest(path: PurePosixPath) -> bool:
    name = path.name.lower()

    return (
        name in MANIFEST_NAMES
        or name.startswith("dockerfile")
        or name.startswith("docker-compose.")
        or name.startswith("compose.")
        or (
            name.startswith("requirements")
            and name.endswith(".txt")
        )
    )


def is_test_file(path: PurePosixPath) -> bool:
    name = path.name.lower()
    directories = {
        part.lower()
        for part in path.parts[:-1]
    }

    return (
        bool(directories & {"test", "tests", "__tests__"})
        or name.startswith("test_")
        or name.endswith(("_test.py", "_test.go", "_test.rs"))
        or ".test." in name
        or ".spec." in name
    )


def classify_files(files: list[str]) -> dict[str, list[str]]:
    signals: dict[str, list[str]] = {
        "readmes": [],
        "manifests": [],
        "entrypoint_candidates": [],
        "test_candidates": [],
        "workflows": [],
    }

    for item in files:
        path = PurePosixPath(item)
        name = path.name.lower()

        if name.startswith("readme"):
            signals["readmes"].append(item)

        if is_manifest(path):
            signals["manifests"].append(item)

        if name in ENTRYPOINT_NAMES:
            signals["entrypoint_candidates"].append(item)

        if is_test_file(path):
            signals["test_candidates"].append(item)

        if (
            len(path.parts) >= 3
            and path.parts[0] == ".github"
            and path.parts[1] == "workflows"
        ):
            signals["workflows"].append(item)

    return signals


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect metadata from a local Git repository.",
    )
    parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        type=Path,
        help="Path to an acquired repository; defaults to the current directory.",
    )
    return parser.parse_args()


def build_snapshot(repository: Path) -> dict[str, object]:
    requested_path = repository.expanduser().resolve()

    if not requested_path.is_dir():
        raise SnapshotError(
            f"repository directory does not exist: {requested_path}"
        )

    root = Path(
        run_git(requested_path, "rev-parse", "--show-toplevel")
    ).resolve()

    files = get_tracked_files(root)

    return {
        "repository_root": root.as_posix(),
        "remote_url": run_git(root, "remote", "get-url", "origin"),
        "commit_sha": run_git(root, "rev-parse", "HEAD"),
        "tracked_file_count": len(files),
        "signals": classify_files(files),
    }


def main() -> int:
    args = parse_args()

    try:
        snapshot = build_snapshot(args.repository)
    except SnapshotError as exc:
        print(f"repo_snapshot: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
