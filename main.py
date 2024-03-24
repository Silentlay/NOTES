import json
import os
import csv
from datetime import datetime, timedelta, timezone


class Note:
    def __init__(self, note_id, title, body, created_at=None, updated_at=None):
        self.note_id = note_id
        self.title = title
        self.body = body
        self.created_at = created_at if created_at else self.get_current_time()
        self.updated_at = updated_at if updated_at else self.get_current_time()

    def get_current_time(self):
        return datetime.now()

        
    def __repr__(self):
        created_at_str = self.created_at.strftime("%d-%m-%Y %H:%M:%S")
        updated_at_str = self.updated_at.strftime("%d-%m-%Y %H:%M:%S")
        return f"Номер заметки: {self.note_id}\nЗаголовок: {self.title}\nТекст: {self.body}\nСоздана в: {created_at_str}\nОбновлена в: {updated_at_str}"



class NoteManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.notes = []
        self.load_notes()

        
    def load_notes(self):
        if not os.path.exists(self.file_path):
            return

        if self.file_path.endswith('.json'):
            with open(self.file_path, "r", encoding="utf-8") as file:
                notes_data = json.load(file)
                if not notes_data:
                    return
                self.notes = [Note(note_data['note_id'], note_data['title'], note_data['body'],
                                created_at=datetime.strptime(note_data['created_at'], "%d-%m-%Y %H:%M:%S"),
                                updated_at=datetime.strptime(note_data['updated_at'], "%d-%m-%Y %H:%M:%S"))
                          for note_data in notes_data]
        elif self.file_path.endswith('.csv'):
            with open(self.file_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=';')
                next(reader) 
                for row in reader:
                    note_id = int(row[0])
                    title = row[1]
                    body = row[2]
                    created_at = datetime.strptime(row[3], "%d-%m-%Y %H:%M:%S")
                    updated_at = datetime.strptime(row[4], "%d-%m-%Y %H:%M:%S")
                    self.notes.append(Note(note_id, title, body, created_at, updated_at))
        else:
            raise ValueError("Неподдерживаемый формат файла")

        
    def save_notes(self):
        if self.file_path.endswith('.json'):
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([{
                    'note_id': note.note_id,
                    'title': note.title,
                    'body': note.body,
                    'created_at': note.created_at.strftime("%d-%m-%Y %H:%M:%S"),  # Преобразование в нужный формат
                    'updated_at': note.updated_at.strftime("%d-%m-%Y %H:%M:%S")  # Преобразование в нужный формат
                } for note in self.notes], file, ensure_ascii=False, default=str)
        elif self.file_path.endswith('.csv'):
            with open(self.file_path, "w", encoding="utf-8", newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(["Номер заметки", "Заголовок", "Текст", "Дата создания", "Дата последнего изменения"])
                for note in self.notes:
                    writer.writerow([note.note_id, note.title, note.body,
                                note.created_at.strftime("%d-%m-%Y %H:%M:%S"),  # Преобразование в нужный формат
                                note.updated_at.strftime("%d-%m-%Y %H:%M:%S")])  # Преобразование в нужный формат
        else:
            raise ValueError("Неподдерживаемый формат файла")



    def print_notes(self):
        if not self.notes:
            print("!!! Нет ни одной заметки.")
        else:
            for note in self.notes:
                print(note)
                print()

    def add_note(self, title, body):
        max_note_id = max([note.note_id for note in self.notes], default=0)
        new_note_id = max_note_id + 1
        moscow_timezone = timezone(timedelta(hours=3))
        current_time = datetime.now(moscow_timezone)
        new_note = Note(new_note_id, title, body, created_at=current_time, updated_at=current_time)
        self.notes.append(new_note)
        self.save_notes()
        print("\nЗаметка успешно добавлена.")

    def edit_note(self, note_id, title, body):
        for note in self.notes:
            if note.note_id == note_id:
                note.title = title
                note.body = body
                note.updated_at = datetime.now(timezone(timedelta(hours=3)))
                self.save_notes()
                print("\nЗаметка успешно отредактирована.")
                return
        print("Заметка не найдена.")

    def delete_note_by_id(self, note_id):
        for note in self.notes:
            if note.note_id == note_id:
                self.notes.remove(note)
                self.save_notes()
                print("\nЗаметка успешно удалена.")
                return True
        print("Заметка не найдена.")
        return False

        
    def list_notes_by_date(self, date):
        notes_on_date = [note for note in self.notes if note.created_at.date() == date.date()]
        if notes_on_date:
            print()
            for note in notes_on_date:
                print(note)
        else:
            print("Нет заметок за указанную дату.")
    
   
    def list_note_by_id(self, note_id, file_format):
        notes_to_search = self.notes if file_format == "json" else self.notes
        notes_found = [note for note in notes_to_search if note.note_id == note_id]
        if notes_found:
            print(f"Найденная заметка в формате {file_format}:")
            for note in notes_found:
                print(note)
        else:
            if file_format == "json":
                print("Нет заметки в формате JSON с указанным номером.")
            elif file_format == "csv":
                print("Нет заметки в формате CSV с указанным номером.")



def get_date_from_input():
    while True:
        date_str = input("\nВведите дату в формате ДД-ММ-ГГГГ: ")
        try:
            date = datetime.strptime(date_str, "%d-%m-%Y")
            return date
        except ValueError:
            print("\n!!! Вы ввели неправильный формат даты. Пожалуйста, введите дату в формате ДД-ММ-ГГГГ.")


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
            print("\nВывожу заметки в формате JSON:\n")
            json_manager.print_notes()
            print("\nВывожу заметки в формате CSV:\n")
            csv_manager.print_notes()
        elif choice == "2":
            while True:
                format_choice = input("\nВыберите формат файла для новой заметки:\n1. JSON\n2. CSV\n\nВведите номер 1 - JSON или 2 - CSV (или 0 для выхода в меню): ")
                if format_choice == "1":
                    title = input("\nВведите заголовок для заметки: ")
                    body = input("Введите текст: ")
                    json_manager.add_note(title, body)
                    break
                elif format_choice == "2":
                    title = input("\nВведите заголовок для заметки: ")
                    body = input("Введите текст: ")
                    csv_manager.add_note(title, body)
                    break
                elif format_choice == "0":
                    print("Выход в меню.")
                    break
                else:
                    print("\n!!! Неправильный выбор формата. Пожалуйста, выберите 1 или 2.")
                    continue  # Возвращаемся к запросу выбора формата заметки


        elif choice == "3":
            while True:
                format_choice = input("\nВыберите формат файла для редактирования заметки:\n1. JSON\n2. CSV\n\nВведите номер 1 - JSON или 2 - CSV (или 0 для выхода в меню): ")

                if format_choice == "1":
                    note_manager = json_manager
                elif format_choice == "2":
                    note_manager = csv_manager
                elif format_choice == "0":
                    print("Выход в меню.")
                    break
                else:
                    print("\n!!! Неправильный выбор формата. Пожалуйста, выберите 1 или 2 (или 0 для выхода в меню)")
                    continue

                if format_choice == "0":
                    print("Выход в меню.")
                    break

                if not note_manager.notes:
                    print("Нет сохраненных заметок для редактирования.")
                    break

                while True:
                    print("\nЗаметки в выбранном формате:\n")
                    note_manager.print_notes()

                    try:
                        note_id = int(input("\nВведите номер заметки для редактирования или введите 0 для выхода: "))
                    except ValueError:
                        print("Ошибка: Введите корректный номер заметки (целое число).")
                        continue

                    if note_id == 0:
                        print("Выход из редактирования.")
                        break

                    note_to_edit = None
                    for note in note_manager.notes:
                        if note.note_id == note_id:
                            note_to_edit = note
                            break

                    if note_to_edit:
                        print("\nВыбранная заметка для редактирования:\n")
                        print(note_to_edit)
                        title = input("\nВведите новый заголовок для заметки: ")
                        body = input("Введите новый текст для заметки: ")
                        note_manager.edit_note(note_id, title, body)
                        break

                if format_choice == "0":
                    print("Выход в меню.")
                break

        elif choice == "4":
            format_choice = input("\nВыберите формат файла для удаления заметки:\n1. JSON\n2. CSV\n\nВведите номер 1 или 2: ")
            while format_choice not in ["1", "2"]:
                print("\n!!! Неправильный выбор формата. Пожалуйста, выберите 1 или 2.")
                format_choice = input("\nВыберите формат файла для удаления заметки:\n1. JSON\n2. CSV\n\nВведите номер 1 или 2: ")

            if format_choice == "1":
                note_manager = json_manager
                print("\nВывожу файл в формате JSON:\n")
                note_manager.print_notes()
            elif format_choice == "2":
                note_manager = csv_manager
                print("\nВывожу файл в формате CSV:\n")
                note_manager.print_notes()

            if not note_manager.notes:
                #print("Нет ни одной заметки.")
                continue  # Возвращаемся в главное меню

            while True:
                try:
                    note_id = int(input("\nВведите номер заметки для удаления: "))
                    if any(note.note_id == note_id for note in note_manager.notes):
                        break
                    else:
                        print("\n!!! Нет заметки с таким номером.")
                except ValueError:
                    print("\nВведите корректный номер заметки (целое число).")

            note_manager.delete_note_by_id(note_id)

        elif choice == "5":
            date = get_date_from_input()
            print("\nВывожу заметки за указанную дату:\n")
            json_manager.list_notes_by_date(date)
            csv_manager.list_notes_by_date(date)

        elif choice == "6":
            if json_manager.notes or csv_manager.notes:
                while True:
                    note_id_input = input("Введите номер заметки для просмотра (или введите 0 для выхода): ").strip()
                    if note_id_input == "0":
                        print("Выход в меню.")
                        break
                    try:
                        note_id = int(note_id_input)
                        if note_id <= 0:
                            print("Ошибка: Введите положительный номер заметки.")
                            continue
                    except ValueError:
                        print("Ошибка: Введите корректный номер заметки (целое число).")
                        continue

                    format_choice = input("Выберите формат файла для вывода заметки по номеру:\n1. JSON\n2. CSV\nВведите номер: ")
                    if format_choice == "1":
                        json_manager.list_note_by_id(note_id, "json")
                    elif format_choice == "2":
                        csv_manager.list_note_by_id(note_id, "csv")
                    else:
                        print("Неправильный выбор формата. Пожалуйста, выберите 1 или 2.")
            else:
                print("Нет сохраненных заметок для просмотра.")
                continue

        elif choice == "7":
            print("Завершение программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")


if __name__ == "__main__":
    main()

