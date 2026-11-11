# markdown-notes

Store, search, and export markdown notes.

## Usage

```bash
python3 -c "from notes import *; s=NotesStore('notes'); print(s.create('Plan', 'ship it')); print(s.list())"
```

## Features

- One markdown file per note with slugified names
- Case-insensitive full-text search
- Back up all notes with export_all(store, dest)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
