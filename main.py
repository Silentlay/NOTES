import json
import os
import csv
from datetime import datetime, timezone, timedelta


class Note:
    def __init__(self, note_id, title, body, created_at=None, updated_at=None):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.created_at = created_at if created_at else self.get_current_time()
        self.updated_at = updated_at if updated_at else self.get_current_time()

    def get_current_time(self):
        moscow_timezone = timezone(timedelta(hours=3))  # Московское время (UTC+3)
        return datetime.now(moscow_timezone).strftime("%d-%m-%Y %H:%M:%S")

    def __repr__(self):
        return f"Номер заметки: {self.note_id}\nНазвание: {self.title}\nТекст: {self.body}\nСоздана в: {self.created_at}\nОбновлена в: {self.updated_at}"


class NoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = self.load_notes()

    def load_notes(self):
        if not os.path.exists(self.file_path):
            return []
        if self.file_path.endswith('.json'):
            with open(self.file_path, "r", encoding="utf-8") as file:
                notes_data = json.load(file)
                return [Note(**note_data) for note_data in notes_data]
        elif self.file_path.endswith('.csv'):
            with open(self.file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=';')
                return [Note(*row) for row in reader]
        else:
            raise ValueError("Неподдерживаемый формат файла")

    def save_notes(self):
        if self.file_path.endswith('.json'):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([note.__dict__ for note in self.notes], file, ensure_ascii=False)
        elif self.file_path.endswith('.csv'):
            with open(self.file_path, "w", encoding="utf-8", newline='') as file:
                writer = csv.writer(file, delimiter=';')
                for note in self.notes:
                    writer.writerow([note.note_id, note.title, note.body, note.created_at, note.updated_at])
        else:
            raise ValueError("Неподдерживаемый формат файла")
    
    
    def print_notes(self):
        if not self.notes:
            print("Нет ни одной заметки.")
        else:
            for note in self.notes:
                print("Номер заметки:", note.note_id)
                print("Заголовок:", note.title)
                print("Текст заметки:", note.body)
                print("Дата создания:", note.created_at)
                print("Дата последнего изменения:", note.updated_at)
                print()

    def list_notes(self):
        print("Вывожу заметки в формате JSON:")
        self.print_notes()

    def list_notes_by_date(self, date):
        json_notes = [note for note in self.notes if isinstance(note, dict)]
        csv_notes = [note for note in self.notes if isinstance(note, Note)]
    
        filtered_json_notes = [note for note in json_notes if note['created_at'].startswith(date.strftime("%d-%m-%Y"))]
        filtered_csv_notes = [note for note in csv_notes if note.created_at.startswith(date.strftime("%d-%m-%Y"))]
    
        if not filtered_json_notes and not filtered_csv_notes:
            print("Заметок за указанную дату не найдено.")
        else:
            print("Заметки из JSON формата:")
        for note in filtered_json_notes:
            print("Номер заметки:", note['note_id'])
            print("Заголовок:", note['title'])
            print("Текст заметки:", note['body'])
            print("Дата создания:", note['created_at'])
            print("Дата последнего изменения:", note['updated_at'])
            print()
        
        print("Заметки из CSV формата:")
        for note in filtered_csv_notes:
            print("Номер заметки:", note.note_id)
            print("Заголовок:", note.title)
            print("Текст заметки:", note.body)
            print("Дата создания:", note.created_at)
            print("Дата последнего изменения:", note.updated_at)
            print()


    def add_note(self, title, body):
        note_id = len(self.notes) + 1
        new_note = Note(note_id, title, body)
        self.notes.append(new_note)
        self.save_notes()
        print("Заметка успешно добавлена.")

    def edit_note(self, note_id, title, body):
        for note in self.notes:
            if note.note_id == note_id:
                note.title = title
                note.body = body
                note.updated_at =  datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.save_notes()
                print("Заметка успешно отредактирована.")
                return
        print("Заметка не найдена.")

    def delete_note(self, note_id):
        for note in self.notes:
            if str(note.note_id) == str(note_id):  # Преобразуем note_id в строку перед сравнением
                self.notes.remove(note)
                self.save_notes()
                print("Заметка успешно удалена.")
                return
    print("Заметка не найдена.")


    def list_note_by_id(self, note_id, file_format):
        notes_to_search = self.notes if file_format == "json" else self.notes  # Заменяем json_notes на self.notes
        for note in notes_to_search:
            if note.note_id == note_id:
                print("Найденная заметка:")
                print("Номер заметки:", note.note_id)
                print("Заголовок:", note.title)
                print("Текст заметки:", note.body)
                print("Дата создания:", note.created_at)
                print("Дата последнего изменения:", note.updated_at)
            return
        print("Заметка с указанным номером не найдена.")


def get_date_from_input():
    while True:
        date_str = input("Введите дату в формате ДД-ММ-ГГГГ: ")
        try:
            date = datetime.strptime(date_str, "%d-%m-%Y")
            return date
        except ValueError:
            print("Ошибка: Неправильный формат даты. Пожалуйста, введите дату в формате ДД-ММ-ГГГГ.")

def main():
    json_manager = NoteManager("notes.json")
    csv_manager = NoteManager("notes.csv")
    
    while True:
            print("\nМеню:")
            print("\n1. Вывести все заметки")
            print("2. Добавить новую заметку")
            print("3. Редактировать заметку")
            print("4. Удалить заметку")
            print("5. Вывести заметки за определенную дату")
            print("6. Вывести заметку по номеру")
            print("7. Выход")

            choice = input("\nВведите ваш выбор: ")

            if choice == "1":
                print("Вывожу заметки в формате JSON:")
                json_manager.print_notes()
                print("Вывожу заметки в формате CSV:")
                csv_manager.print_notes()
            elif choice == "2":
                format_choice = input("Выберите формат файла для новой заметки:\n1. JSON\n2. CSV\nВведите номер: ")
                if format_choice == "1":
                    title = input("Введите заголовок для заметки: ")
                    body = input("Введите текст: ")
                    json_manager.add_note(title, body)
                elif format_choice == "2":
                    title = input("Введите заголовок для заметки: ")
                    body = input("Введите текст: ")
                    csv_manager.add_note(title, body)
                else:
                    print("Неправильный выбор формата. Пожалуйста, выберите 1 или 2.")
                
            elif choice == "3":
                format_choice = input("Выберите формат файла для редактирования заметки:\n1. JSON\n2. CSV\nВведите номер: ")
                if format_choice == "1":
                    note_manager = json_manager
                elif format_choice == "2":
                    note_manager = csv_manager
                else:
                    print("Неправильный выбор формата. Пожалуйста, выберите 1 или 2.")
                    continue
            
                note_id = int(input("Введите номер заметки для редактирования: "))
                title = input("Введите новый заголовок для заметки: ")
                body = input("Введите новый текст для заметки: ")
            
                if note_manager:
                    note_manager.edit_note(note_id, title, body)
                else:
                    print("Сначала выберите формат файла для хранения заметок.")
                                  
            elif choice == "4":
                while True:
                    format_choice = input("Выберите формат файла для удаления заметки:\n1. JSON\n2. CSV\nВведите номер: ")
                    if format_choice == "1":
                        note_id = int(input("Введите номер заметки для удаления: "))
                        json_manager.delete_note(note_id)
                        break  # Выход из цикла после успешного удаления заметки
                    elif format_choice == "2":
                        note_id = int(input("Введите номер заметки для удаления: "))
                        csv_manager.delete_note(note_id)
                        break  # Выход из цикла после успешного удаления заметки
                    else:
                        print("Неправильный выбор формата. Пожалуйста, выберите 1 или 2.")



                    
            elif choice == "5":
                date = get_date_from_input()
                print("Вывожу заметки за указанную дату:")
                json_manager.list_notes_by_date(date)
                csv_manager.list_notes_by_date(date)
                
            elif choice == "6":
                if json_manager.notes or csv_manager.notes:
                    note_id = int(input("Введите номер заметки для просмотра: "))
                    format_choice = input("Выберите формат файла для вывода заметки по номеру:\n1. JSON\n2. CSV\nВведите номер: ")
                    if format_choice == "1":
                        json_manager.list_note_by_id(note_id, "json")
                    elif format_choice == "2":
                        csv_manager.list_note_by_id(note_id, "csv")
                    else:
                        print("Неправильный выбор формата. Пожалуйста, выберите 1 или 2.")
                else:
                    print("Нет сохраненных заметок для просмотра.")
                    
            elif choice == "7":
                print("Завершение программы.")
                break
            else:
                print("Неверный выбор. Пожалуйста, попробуйте еще раз.")

if __name__ == "__main__":
    main()


    