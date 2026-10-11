import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.service import request as request_service
from src.repository import request as request_repository

def print_menu():
    print("\n" + "=" * 50)
    print("  СИСТЕМА УЧЁТА ЗАЯВОК")
    print("=" * 50)
    print("1. Показать все заявки")
    print("2. Показать заявку по id")
    print("3. Создать заявку")
    print("4. Редактировать заявку")
    print("5. Сменить статус")
    print("6. Назначить исполнителя")
    print("7. Поиск заявок")
    print("8. Фильтр по статусу")
    print("9. Удалить заявку")
    print("0. Выход")
    print("=" * 50)

def print_request(r):
    print(f"\n  ID: {r.id}")
    print(f"  Номер: {r.request_number}")
    print(f"  Тема: {r.topic}")
    print(f"  Описание: {r.description}")
    print(f"  Приоритет: {r.priority}")
    print(f"  Категория ID: {r.category_id}")
    print(f"  Статус ID: {r.status_id}")
    print(f"  Заявитель ID: {r.requester_id}")
    print(f"  Исполнитель ID: {r.assignee_id}")

def action_list():
    print("\n--- ВСЕ ЗАЯВКИ ---")
    requests = request_service.get_all_requests()
    if not requests:
        print("  Заявок нет")
        return
    for r in requests:
        print(f"  [{r.id}] {r.request_number} — {r.topic} "
              f"(статус: {r.status_id})")

def action_get():
    try:
        request_id = int(input("Введите id заявки: "))
        r = request_service.get_request(request_id)
        print_request(r)
    except ValueError:
        print("  Ошибка: id должен быть числом")
    except request_service.BusinessError as e:
        print(f"  Ошибка: {e}")

def action_create():
    try:
        topic = input("Тема: ")
        description = input("Описание: ")
        category_id = int(input("Категория (id): "))
        priority = input("Приоритет (Высокий/Средний/Низкий): ")
        requester_id = int(input("Заявитель (id): "))

        new_id = request_service.create_request(
            topic=topic,
            description=description,
            category_id=category_id,
            priority=priority,
            requester_id=requester_id,
        )
        print(f"  Заявка создана с id = {new_id}")
    except ValueError:
        print("  Ошибка: неверный формат числа")
    except request_service.ValidationError as e:
        print(f"  Ошибка валидации: {e}")

def action_edit():
    try:
        request_id = int(input("id заявки для редактирования: "))
        topic = input("Новая тема (Enter — не менять): ")
        description = input("Новое описание (Enter — не менять): ")

        request_service.edit_request(
            request_id=request_id,
            topic=topic if topic else None,
            description=description if description else None,
        )
        print("  Заявка обновлена")
    except ValueError:
        print("  Ошибка: неверный id")
    except (request_service.BusinessError,
            request_service.ValidationError) as e:
        print(f"  Ошибка: {e}")

def action_change_status():
    try:
        request_id = int(input("id заявки: "))
        print("  Статусы: 1 — Новая, 2 — В работе, "
              "3 — Выполнена, 4 — Закрыта")
        new_status = int(input("Новый статус (id): "))

        request_service.change_status(request_id, new_status)
        print("  Статус изменён")
    except ValueError:
        print("  Ошибка: неверный формат")
    except request_service.BusinessError as e:
        print(f"  Ошибка: {e}")

def action_assign():
    try:
        request_id = int(input("id заявки: "))
        assignee_id = int(input("id исполнителя: "))
        request_service.assign_executor(request_id, assignee_id)
        print("  Исполнитель назначен")
    except ValueError:
        print("  Ошибка: неверный формат")
    except request_service.BusinessError as e:
        print(f"  Ошибка: {e}")

def action_search():
    query = input("Поисковый запрос: ")
    results = request_service.search_requests(query)
    if not results:
        print("  Ничего не найдено")
        return
    print(f"\n  Найдено: {len(results)}")
    for r in results:
        print(f"  [{r.id}] {r.request_number} — {r.topic}")

def action_filter():
    try:
        status_id = int(input("Статус id (1–4): "))
        results = request_service.filter_requests(status_id=status_id)
        if not results:
            print("  Нет заявок с таким статусом")
            return
        print(f"\n  Найдено: {len(results)}")
        for r in results:
            print(f"  [{r.id}] {r.request_number} — {r.topic}")
    except ValueError:
        print("  Ошибка: неверный формат")

def action_delete():
    try:
        request_id = int(input("id заявки для удаления: "))
        confirm = input(
            f"Удалить заявку {request_id}? (да/нет): "
        )
        if confirm.lower() != "да":
            print("  Удаление отменено")
            return
        request_service.delete_request(request_id)
        print("  Заявка удалена")
    except ValueError:
        print("  Ошибка: неверный id")
    except request_service.BusinessError as e:
        print(f"  Ошибка: {e}")

def main():
    actions = {
        "1": action_list,
        "2": action_get,
        "3": action_create,
        "4": action_edit,
        "5": action_change_status,
        "6": action_assign,
        "7": action_search,
        "8": action_filter,
        "9": action_delete,
    }

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("Выход.")
            break

        action = actions.get(choice)
        if action:
            try:
                action()
            except Exception as e:
                print(f"  Непредвиденная ошибка: {e}")
        else:
            print("  Неверный пункт меню")

if __name__ == "__main__":
    main()