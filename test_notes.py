from notes_app import add_note, get_note, delete_note, update_note, list_notes
import os


def test_all_functions():
    """Тестирование всех функций приложения"""
    print("=== ТЕСТИРОВАНИЕ ФУНКЦИЙ ЗАМЕТОК ===")

    # Тест 1: Добавление заметок
    print("\n1. Добавление заметок:")
    id1 = add_note("Покупки", "Купить молоко, хлеб, яйца")
    id2 = add_note("Встреча", "Встреча с командой в 15:00")
    id3 = add_note("Идеи", "Разработать новый проект")

    # Тест 2: Просмотр списка заметок
    print("\n2. Список всех заметок:")
    list_notes()

    # Тест 3: Просмотр конкретной заметки
    print(f"\n3. Просмотр заметки ID={id2}:")
    get_note(id2)

    # Тест 4: Обновление заметки
    print(f"\n4. Обновление заметки ID={id1}:")
    update_note(id1, title="Список покупок", text="Молоко, хлеб, яйца, масло")
    get_note(id1)

    # Тест 5: Удаление заметки
    print(f"\n5. Удаление заметки ID={id3}:")
    delete_note(id3)

    # Тест 6: Просмотр оставшихся заметок
    print("\n6. Оставшиеся заметки:")
    list_notes()

    print("\n=== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ===")


if __name__ == "__main__":
    # Удаляем тестовые файлы, если они существуют
    if os.path.exists('notes.json'):
        os.remove('notes.json')
    if os.path.exists('notes.log'):
        os.remove('notes.log')

    test_all_functions()