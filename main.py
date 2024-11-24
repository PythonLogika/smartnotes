from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import json

notes = {
    "Ласкаво просимо": {
        "text": "Розумні додатки",
        "tags": ["notes", "first", "smart"]
    }
}

with open("notes_data.json", "w") as file:
    json.dump(notes, file)

app = QApplication([])

window = QWidget()
window.setWindowTitle("Smart Notes")
window.resize(800, 600)

list_notes = QListWidget()
list_notes_label = QLabel("Список нотаток")

button_note_create = QPushButton("Створити нотатку")
button_note_delete = QPushButton("Видалити нотатку")
button_note_save = QPushButton("Зберегти нотатку")

field_tag = QLineEdit("")
field_tag.setPlaceholderText("Ввести тег")

field_text = QTextEdit()

button_tag_add = QPushButton("Додати тег")
button_tag_delete = QPushButton("Видалити тег")
button_tag_search = QPushButton("Знайти тег")

list_tags = QListWidget()
list_tags_label = QLabel("Список тегів")

layout_notes = QHBoxLayout()

col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_delete)

row_2 = QHBoxLayout()
row_2.addWidget(button_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_delete)

row_4 = QHBoxLayout()
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)

window.setLayout(layout_notes)


def add_note():
    note_name, ok = QInputDialog.getText(window, "Додати нотатку", "Назва нотатки:")
    if ok and note_name != "":
        notes[note_name] = {"text": "", "tags": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["tags"])
        print(notes)


def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["text"])
    list_tags.clear()
    list_tags.addItems(notes[key]["tags"])


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["text"] = field_text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Нотатка для збереження не була вибрана")

def delete_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)

        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Нотатка для видалення не була вибрана")


def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["tags"]:
            notes[key]["tags"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Нотатка для додавання тегу не була вибрана")


def delete_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["tags"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["tags"])

        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Тег для видалення не був вибраний")
       

def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == "Знайти нотатку" and tag:
        print(tag)
        notes_filtered = {} # тут будуть замітки з виділеним тегом
        for note in notes:
            if tag in notes[note]["теги"]: 
                notes_filtered[note] = notes[note]
        button_tag_search.setText("Скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == "Скинути пошук":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Знайти нотатку")
        print(button_tag_search.text())
    else:
        pass


list_notes.itemClicked.connect(show_note)

button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_delete.clicked.connect(delete_note)

button_tag_add.clicked.connect(add_tag)
button_tag_delete.clicked.connect(delete_tag)
button_tag_search.clicked.connect(search_tag)

window.show()

with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)

app.exec_()
