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


class RenameTests(unittest.TestCase):
    def test_rename_moves_file_and_preserves_content(self):
        import os

        with tempfile.TemporaryDirectory() as directory:
            store = NotesStore(directory)
            source = store.create("Plan", "ship it")
            with open(source, "rb") as handle:
                original = handle.read()
            destination = store.rename("plan", "New Plan")
            self.assertTrue(destination.endswith("new-plan.md"))
            self.assertFalse(os.path.exists(source))
            with open(destination, "rb") as handle:
                self.assertEqual(handle.read(), original)

    def test_rename_conflict_raises_and_leaves_original_intact(self):
        import os

        with tempfile.TemporaryDirectory() as directory:
            store = NotesStore(directory)
            store.create("Plan", "ship it")
            store.create("Other", "keep me")
            with self.assertRaises(FileExistsError):
                store.rename("plan", "Other")
            self.assertTrue(os.path.exists(store.path_for("plan")))
            self.assertTrue(os.path.exists(store.path_for("other")))
            self.assertIn("ship it", store.read("plan"))
            self.assertIn("keep me", store.read("other"))

    def test_rename_to_same_slug_raises(self):
        with tempfile.TemporaryDirectory() as directory:
            store = NotesStore(directory)
            store.create("Plan", "ship it")
            with self.assertRaises(FileExistsError):
                store.rename("plan", "Plan")


class DeleteTests(unittest.TestCase):
    def test_delete_removes_file_and_list_excludes_it(self):
        import os

        with tempfile.TemporaryDirectory() as directory:
            store = NotesStore(directory)
            path = store.create("Plan", "ship it")
            self.assertEqual(store.delete("plan"), path)
            self.assertFalse(os.path.exists(path))
            self.assertEqual(store.list(), [])

    def test_delete_missing_note_raises(self):
        with tempfile.TemporaryDirectory() as directory:
            store = NotesStore(directory)
            with self.assertRaises(FileNotFoundError):
                store.delete("missing")


class TitleTests(unittest.TestCase):
    def test_titles_parses_first_heading(self):
        with tempfile.TemporaryDirectory() as directory:
            store = NotesStore(directory)
            store.create("My Plan", "body")
            self.assertEqual(store.titles(), {"my-plan": "My Plan"})

    def test_titles_falls_back_to_slug_without_heading(self):
        import os

        with tempfile.TemporaryDirectory() as directory:
            store = NotesStore(directory)
            path = os.path.join(directory, "plain.md")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("no heading here\n")
            self.assertEqual(store.titles(), {"plain": "plain"})


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
