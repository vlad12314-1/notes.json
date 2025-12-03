import json
import os
import uuid
from datetime import datetime
from functools import wraps

# Файлы для хранения данных
NOTES_FILE = 'notes.json'
LOG_FILE = 'notes.log'


def save_log(func):
    """Декоратор для логирования действий с заметками"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Получаем ID заметки из аргументов
        note_id = None
        for arg in args:
            if isinstance(arg, (int, str)) and str(arg).isdigit():
                note_id = arg
                break
        if not note_id and 'id' in kwargs:
            note_id = kwargs['id']

        # Выполняем функцию
        result = func(*args, **kwargs)

        # Логируем действие
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        action = func.__name__

        with open(LOG_FILE, 'a', encoding='utf-8') as log_file:
            log_file.write(f"{timestamp} | Действие: {action} | ID заметки: {note_id}\n")

        return result

    return wrapper


def load_notes():
    """Загружает заметки из файла"""
    if not os.path.exists(NOTES_FILE):
        return []

    try:
        with open(NOTES_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_notes(notes):
    """Сохраняет заметки в файл"""
    with open(NOTES_FILE, 'w', encoding='utf-8') as file:
        json.dump(notes, file, ensure_ascii=False, indent=2)


def add_note(title, text):
    """Добавляет новую заметку"""
    notes = load_notes()

    # Генерируем ID
    if notes:
        note_id = max(note['id'] for note in notes) + 1
    else:
        note_id = 1

    # Создаем новую заметку
    new_note = {
        'id': note_id,
        'title': title,
        'text': text,
        'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'updated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    notes.append(new_note)
    save_notes(notes)
    print(f"Заметка '{title}' успешно добавлена (ID: {note_id})")
    return note_id


@save_log
def get_note(id):
    """Получает заметку по ID"""
    notes = load_notes()

    for note in notes:
        if note['id'] == id:
            print(f"\nЗаметка найдена:")
            print(f"ID: {note['id']}")
            print(f"Заголовок: {note['title']}")
            print(f"Текст: {note['text']}")
            print(f"Создана: {note['created_date']}")
            print(f"Обновлена: {note['updated_date']}")
            return note

    print(f"Заметка с ID {id} не найдена")
    return None


@save_log
def delete_note(id):
    """Удаляет заметку по ID"""
    notes = load_notes()

    for i, note in enumerate(notes):
        if note['id'] == id:
            deleted_title = notes.pop(i)['title']
            save_notes(notes)
            print(f"Заметка '{deleted_title}' (ID: {id}) успешно удалена")
            return True

    print(f"Заметка с ID {id} не найдена")
    return False


def update_note(id, title=None, text=None):
    """Обновляет заметку (дополнительная функция)"""
    notes = load_notes()

    for note in notes:
        if note['id'] == id:
            if title:
                note['title'] = title
            if text:
                note['text'] = text
            note['updated_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_notes(notes)
            print(f"Заметка с ID {id} успешно обновлена")
            return True

    print(f"Заметка с ID {id} не найдена")
    return False


def list_notes():
    """Выводит список всех заметок"""
    notes = load_notes()

    if not notes:
        print("Нет сохраненных заметок")
        return

    print(f"\nВсего заметок: {len(notes)}")
    print("-" * 40)
    for note in notes:
        print(f"ID: {note['id']} | {note['title']} | {note['created_date']}")


def show_log():
    """Показывает лог действий"""
    if not os.path.exists(LOG_FILE):
        print("Лог файл пуст")
        return

    with open(LOG_FILE, 'r', encoding='utf-8') as log_file:
        logs = log_file.read()
        if logs:
            print("\n=== Лог действий ===")
            print(logs)
        else:
            print("Лог файл пуст")


def main():
    """Основная функция приложения"""
    while True:
        print("\n" + "=" * 40)
        print("МЕНЮ УПРАВЛЕНИЯ ЗАМЕТКАМИ")
        print("=" * 40)
        print("1. Добавить заметку")
        print("2. Просмотреть заметку")
        print("3. Удалить заметку")
        print("4. Обновить заметку")
        print("5. Список всех заметок")
        print("6. Показать лог действий")
        print("7. Выход")

        choice = input("\nВыберите действие (1-7): ")

        if choice == '1':
            print("\n--- Добавление новой заметки ---")
            title = input("Введите заголовок заметки: ")
            text = input("Введите текст заметки: ")
            if title and text:
                add_note(title, text)
            else:
                print("Заголовок и текст не могут быть пустыми!")

        elif choice == '2':
            print("\n--- Просмотр заметки ---")
            try:
                note_id = int(input("Введите ID заметки: "))
                get_note(note_id)
            except ValueError:
                print("Ошибка: ID должен быть числом")

        elif choice == '3':
            print("\n--- Удаление заметки ---")
            try:
                note_id = int(input("Введите ID заметки для удаления: "))
                delete_note(note_id)
            except ValueError:
                print("Ошибка: ID должен быть числом")

        elif choice == '4':
            print("\n--- Обновление заметки ---")
            try:
                note_id = int(input("Введите ID заметки для обновления: "))
                title = input("Введите новый заголовок (оставьте пустым, чтобы не менять): ")
                text = input("Введите новый текст (оставьте пустым, чтобы не менять): ")
                if title or text:
                    update_note(note_id, title if title else None, text if text else None)
                else:
                    print("Не указано ни одного поля для обновления")
            except ValueError:
                print("Ошибка: ID должен быть числом")

        elif choice == '5':
            list_notes()

        elif choice == '6':
            show_log()

        elif choice == '7':
            print("Выход из программы...")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()