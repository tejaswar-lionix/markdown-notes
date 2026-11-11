#!/usr/bin/env python3
"""Store markdown notes as one file per note."""
import os
import re


class NotesStore:
    def __init__(self, root):
        self.root = root
        os.makedirs(root, exist_ok=True)

    @staticmethod
    def slugify(title):
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        return slug or "untitled"

    def path_for(self, slug):
        return os.path.join(self.root, slug + ".md")

    def create(self, title, body=""):
        path = self.path_for(self.slugify(title))
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(f"# {title}\n\n{body.strip()}\n")
        return path

    def list(self):
        return sorted(name for name in os.listdir(self.root) if name.endswith(".md"))

    def read(self, slug):
        with open(self.path_for(slug), encoding="utf-8") as handle:
            return handle.read()

    def search(self, query):
        needle = query.lower()
        matches = []
        for name in self.list():
            with open(os.path.join(self.root, name), encoding="utf-8") as handle:
                if needle in handle.read().lower():
                    matches.append(name[:-3])
        return matches
