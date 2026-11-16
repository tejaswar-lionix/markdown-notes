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

    def append(self, slug, body):
        path = self.path_for(slug)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        with open(path, "a", encoding="utf-8") as handle:
            handle.write("\n" + body.strip() + "\n")
        return path

    def rename(self, slug, new_title):
        source = self.path_for(slug)
        if not os.path.exists(source):
            raise FileNotFoundError(source)
        destination = self.path_for(self.slugify(new_title))
        if os.path.exists(destination):
            raise FileExistsError(destination)
        os.rename(source, destination)
        return destination

    def list(self):
        return sorted(name for name in os.listdir(self.root) if name.endswith(".md"))

    def read(self, slug):
        with open(self.path_for(slug), encoding="utf-8") as handle:
            return handle.read()

    def delete(self, slug):
        path = self.path_for(slug)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        os.remove(path)
        return path

    def titles(self):
        titles = {}
        for name in self.list():
            slug = name[:-3]
            title = slug
            with open(os.path.join(self.root, name), encoding="utf-8") as handle:
                for line in handle:
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
            titles[slug] = title
        return titles

    def search(self, query):
        needle = query.lower()
        matches = []
        for name in self.list():
            with open(os.path.join(self.root, name), encoding="utf-8") as handle:
                if needle in handle.read().lower():
                    matches.append(name[:-3])
        return matches


def export_all(store, destination):
    """Copy every markdown note in store into destination."""
    import shutil

    os.makedirs(destination, exist_ok=True)
    for name in store.list():
        shutil.copy2(os.path.join(store.root, name), os.path.join(destination, name))
    return sorted(store.list())
