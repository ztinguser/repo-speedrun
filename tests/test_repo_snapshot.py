import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath


SKILL_ROOT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "repo-speedrun"
)

sys.path.insert(0, str(SKILL_ROOT))

from scripts.repo_snapshot import (
    build_snapshot,
    classify_files,
    is_manifest,
    is_test_file,
)


def run_git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(repository),
            *arguments,
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    return result.stdout.strip()


class ManifestClassificationTests(unittest.TestCase):
    def test_recognizes_common_manifests(self) -> None:
        cases = [
            "package.json",
            "backend/pyproject.toml",
            "cmd/go.mod",
            "Dockerfile",
            "deploy/docker-compose.yml",
            "requirements-dev.txt",
        ]

        for filename in cases:
            with self.subTest(filename=filename):
                self.assertTrue(is_manifest(PurePosixPath(filename)))

    def test_rejects_ordinary_source_files(self) -> None:
        cases = [
            "src/main.py",
            "frontend/package.json.example",
            "docs/requirements.md",
        ]

        for filename in cases:
            with self.subTest(filename=filename):
                self.assertFalse(is_manifest(PurePosixPath(filename)))


class TestFileClassificationTests(unittest.TestCase):
    def test_recognizes_common_test_patterns(self) -> None:
        cases = [
            "tests/helpers.py",
            "backend/test_graph.py",
            "internal/parser_test.go",
            "src/widget.test.tsx",
            "src/widget.spec.ts",
        ]

        for filename in cases:
            with self.subTest(filename=filename):
                self.assertTrue(is_test_file(PurePosixPath(filename)))

    def test_rejects_non_test_files(self) -> None:
        cases = [
            "src/main.py",
            "docs/testing.md",
            "fixtures/user_test.json",
        ]

        for filename in cases:
            with self.subTest(filename=filename):
                self.assertFalse(is_test_file(PurePosixPath(filename)))


class FileClassificationTests(unittest.TestCase):
    def test_groups_repository_signals(self) -> None:
        files = [
            ".github/workflows/ci.yml",
            "Dockerfile",
            "README.md",
            "docs/README.zh-CN.md",
            "package.json",
            "src/main.py",
            "src/service.py",
            "tests/main.py",
            "tests/service_test.py",
        ]

        result = classify_files(files)

        self.assertEqual(
            result,
            {
                "readmes": [
                    "README.md",
                    "docs/README.zh-CN.md",
                ],
                "manifests": [
                    "Dockerfile",
                    "package.json",
                ],
                "entrypoint_candidates": [
                    "src/main.py",
                    "tests/main.py",
                ],
                "test_candidates": [
                    "tests/main.py",
                    "tests/service_test.py",
                ],
                "workflows": [
                    ".github/workflows/ci.yml",
                ],
            },
        )


class SnapshotIntegrationTests(unittest.TestCase):
    def test_builds_snapshot_from_real_git_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)

            run_git(repository, "init")
            run_git(repository, "config", "user.name", "Repo Speedrun Tests")
            run_git(
                repository,
                "config",
                "user.email",
                "repo-speedrun@example.com",
            )

            source_directory = repository / "src"
            source_directory.mkdir()

            (repository / "README.md").write_text(
                "# Tiny Repository\n",
                encoding="utf-8",
            )
            (source_directory / "main.py").write_text(
                'print("hello")\n',
                encoding="utf-8",
            )

            run_git(repository, "add", ".")
            run_git(repository, "commit", "-m", "initial commit")
            run_git(
                repository,
                "remote",
                "add",
                "origin",
                "https://github.com/example/tiny-repository.git",
            )

            expected_sha = run_git(repository, "rev-parse", "HEAD")

            snapshot = build_snapshot(source_directory)

            self.assertEqual(
                snapshot["repository_root"],
                repository.resolve().as_posix(),
            )
            self.assertEqual(
                snapshot["remote_url"],
                "https://github.com/example/tiny-repository.git",
            )
            self.assertEqual(snapshot["commit_sha"], expected_sha)
            self.assertEqual(snapshot["tracked_file_count"], 2)
            self.assertEqual(
                snapshot["signals"]["readmes"],
                ["README.md"],
            )
            self.assertEqual(
                snapshot["signals"]["entrypoint_candidates"],
                ["src/main.py"],
            )


if __name__ == "__main__":
    unittest.main()
