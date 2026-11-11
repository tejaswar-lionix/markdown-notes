import tempfile
import unittest

from notes import NotesStore


class NotesTests(unittest.TestCase):
    def test_create_slugifies_title(self):
        with tempfile.TemporaryDirectory() as directory:
            store = NotesStore(directory)
            path = store.create("My First Note", "hello world")
            self.assertTrue(path.endswith("my-first-note.md"))
            self.assertEqual(store.list(), ["my-first-note.md"])

    def test_read_returns_markdown_content(self):
        with tempfile.TemporaryDirectory() as directory:
            store = NotesStore(directory)
            store.create("Plan", "ship it")
            self.assertIn("# Plan", store.read("plan"))
            self.assertIn("ship it", store.read("plan"))

    def test_search_is_case_insensitive(self):
        with tempfile.TemporaryDirectory() as directory:
            store = NotesStore(directory)
            store.create("Plan", "Ship the release")
            self.assertEqual(store.search("RELEASE"), ["plan"])

    def test_search_misses_unrelated_notes(self):
        with tempfile.TemporaryDirectory() as directory:
            store = NotesStore(directory)
            store.create("Plan", "Ship it")
            self.assertEqual(store.search("zebra"), [])


class ExportTests(unittest.TestCase):
    def test_export_all_copies_notes(self):
        import os

        from notes import NotesStore, export_all

        with tempfile.TemporaryDirectory() as directory:
            source = os.path.join(directory, "notes")
            target = os.path.join(directory, "backup")
            store = NotesStore(source)
            store.create("Plan", "ship it")
            exported = export_all(store, target)
            self.assertEqual(exported, ["plan.md"])
            self.assertTrue(os.path.exists(os.path.join(target, "plan.md")))


if __name__ == "__main__":
    unittest.main()
