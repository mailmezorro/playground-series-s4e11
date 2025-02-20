
from nbformat import read, write, v4

import json
import re

def generate_toc_from_ipynb(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as file:
        notebook = json.load(file)

    toc = ["# Inhaltsverzeichnis\n"]
    for cell in notebook["cells"]:
        if cell["cell_type"] == "markdown":
            for line in cell["source"]:
                match = re.match(r"^(#{1,6})\s+(.*)", line.strip())
                if match:
                    level = len(match.group(1))  # Anzahl der `#`
                    title = match.group(2)       # Titel der Überschrift
                    anchor = title.lower().replace(" ", "-").replace(",", "").replace(".", "")
                    toc.append(f"{'  ' * (level - 1)}- [{title}](#{anchor})")

    return "\n".join(toc)

def insert_toc_into_notebook(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as file:
        notebook = read(file, as_version=4)

    toc = generate_toc_from_ipynb(notebook_path)
    
    # Erstelle eine neue Markdown-Zelle für das Inhaltsverzeichnis
    toc_cell = v4.new_markdown_cell(source=toc)
    
    # Füge das TOC als erste Zelle hinzu
    notebook.cells.insert(0, toc_cell)

    # Speichere das Notebook mit TOC
    with open(notebook_path, "w", encoding="utf-8") as file:
        write(notebook, file)