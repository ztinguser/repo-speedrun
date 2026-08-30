import sys
import unittest
from pathlib import Path, PurePosixPath


SKILL_ROOT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "repo-speedrun"
)

sys.path.insert(0, str(SKILL_ROOT))

from scripts.repo_snapshot import (
    classify_files,
    is_manifest,
    is_test_file,
)


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


if __name__ == "__main__":
    unittest.main()
