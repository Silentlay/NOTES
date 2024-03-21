import json
import os
from datetime import datetime


class Note:
    def __init__(self, note_id, title, body, created_at=None, updated_at=None):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = updated_at if updated_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"Номер заметки: {self.note_id}\nНазвание: {self.title}\nТекст: {self.body}\nСоздана в: {self.created_at}\nОбновлена в: {self.updated_at}"


class NoteManager:
    def __init__(self, file_path="notes.json"):
        self.file_path = file_path
        self.notes = self.load_notes()

    def load_notes(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r") as file:
            notes_data = json.load(file)
            return [Note(**note_data) for note_data in notes_data]

    def save_notes(self):
        with open(self.file_path, "w") as file:
            json.dump([note.__dict__ for note in self.notes], file)

    def list_notes(self):
        for note in self.notes:
            print(note)
            print()

    def add_note(self, title, body):
        note_id = len(self.notes) + 1  # Генерирование идентификатора на основе количества существующих заметок
        new_note = Note(note_id, title, body)
        self.notes.append(new_note)
        self.save_notes()
        print("Заметка успешно добавлена.")

    def edit_note(self, note_id, title, body):
        for note in self.notes:
            if note.note_id == note_id:
                note.title = title
                note.body = body
                note.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.save_notes()
                print("Заметка успешно отредактирована.")
                return
        print("Заметка не найдена.")

    def delete_note(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                self.notes.remove(note)
                self.save_notes()
                print("Заметка успешно удалена.")
                return
        print("Заметка не найдена.")


def main():
    note_manager = NoteManager()

    while True:
        print("\nМеню:")
        print("1. Список заметок")
        print("2. Дабавить заметку")
        print("3. Редактировать заметку")
        print("4. Удалить заметку")
        print("5. Выход")

        choice = input("Введите ваш выбор: ")

        if choice == "1":
            note_manager.list_notes()
        elif choice == "2":
            title = input("Введите названние заметки: ")
            body = input("Введите текст: ")
            note_manager.add_note(title, body)
        elif choice == "3":
            note_id = int(input("Введите номер заметки: "))
            title = input("Введите новое название: ")
            body = input("Введите новый текст: ")
            note_manager.edit_note(note_id, title, body)
        elif choice == "4":
            note_id = int(input("Введите номер заметки для удаления: "))
            note_manager.delete_note(note_id)
        elif choice == "5":
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")


if __name__ == "__main__":
    main()
