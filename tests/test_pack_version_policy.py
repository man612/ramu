#!/usr/bin/env python3
"""Offline proof for pack version governance: compare published content, not admin metadata."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_pack_versions as policy  # noqa: E402

PACK = "id.example.course.2026.s1"
PATH = "packs/example/semester-01/manifest.json"


def snapshots(version: str):
    manifest = {
        "id": PACK, "pack_version": version,
        "project_instructions": "PROJECT-INSTRUCTIONS.md",
        "courses": [{"code": "TEST101", "file": "courses/test.md"}],
    }
    return {PACK: (PATH, manifest)}


class PackVersionPolicyTest(unittest.TestCase):
    def test_version_order(self):
        self.assertTrue(policy.version_is_newer("2026.s1.1", "2026.s1.2"))
        self.assertFalse(policy.version_is_newer("2026.s1.2", "2026.s1.1"))
        self.assertFalse(policy.version_is_newer("2026.s1.1", "2026.s1.1"))
        self.assertFalse(policy.version_is_newer("2026.s1.1", "2027.s1.1"))

    def test_changed_file_without_bump_is_rejected(self):
        with patch.object(policy, "pack_snapshots", side_effect=[snapshots("2026.s1.1"), snapshots("2026.s1.1")]), \
             patch.object(policy, "published_signature", side_effect=["old", "new"]):
            failures = policy.check("base", "head")
        self.assertEqual(len(failures), 1)
        self.assertIn("pack_version", failures[0])

    def test_changed_file_with_bump_needs_notes(self):
        with patch.object(policy, "pack_snapshots", side_effect=[snapshots("2026.s1.1"), snapshots("2026.s1.2")]), \
             patch.object(policy, "published_signature", side_effect=["old", "new"]), \
             patch.object(policy, "read_at", return_value=None):
            failures = policy.check("base", "head")
        self.assertEqual(len(failures), 1)
        self.assertIn("PACK-CHANGES.md", failures[0])

    def test_bump_with_notes_passes(self):
        with patch.object(policy, "pack_snapshots", side_effect=[snapshots("2026.s1.1"), snapshots("2026.s1.2")]), \
             patch.object(policy, "published_signature", side_effect=["old", "new"]), \
             patch.object(policy, "read_at", return_value=b"# Notes\n\n## 2026.s1.2\n\n- Updated instructions."):
            self.assertEqual(policy.check("base", "head"), [])

    def test_registry_review_or_same_published_content_needs_no_bump(self):
        with patch.object(policy, "pack_snapshots", side_effect=[snapshots("2026.s1.1"), snapshots("2026.s1.1")]), \
             patch.object(policy, "published_signature", return_value="unchanged"):
            self.assertEqual(policy.check("base", "head"), [])

    def test_new_pack_is_not_blocked_by_comparison(self):
        with patch.object(policy, "pack_snapshots", side_effect=[{}, snapshots("2026.s1.1")]):
            self.assertEqual(policy.check("base", "head"), [])


if __name__ == "__main__":
    unittest.main()
