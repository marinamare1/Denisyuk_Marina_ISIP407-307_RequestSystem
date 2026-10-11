from src.repository import request as request_repository
from src.domain.models import Request

class ValidationError(Exception):
    """Ошибка валидации данных."""
    pass

class BusinessError(Exception):
    """Ошибка бизнес-правил."""
    pass


# Допустимые переходы статусов
STATUS_TRANSITIONS = {
    1: [2],
    2: [3],
    3: [4],
    4: [],
}

STATUS_NAMES = {
    1: "Новая",
    2: "В работе",
    3: "Выполнена",
    4: "Закрыта",
}

def _validate_new_request(topic, description, category_id, priority):
    """Проверка данных при создании заявки."""
    if not topic or not topic.strip():
        raise ValidationError("Укажите тему заявки")
    if not description or not description.strip():
        raise ValidationError("Укажите описание заявки")
    if not category_id:
        raise ValidationError("Выберите категорию")
    if not priority:
        raise ValidationError("Выберите приоритет")

def _generate_number():
    """Сгенерировать новый уникальный номер заявки."""
    last = request_repository.get_last_number()
    if not last:
        return "REQ-2026-001"
    try:
        num = int(last.split("-")[-1])
    except (ValueError, IndexError):
        num = 0
    return f"REQ-2026-{num + 1:03d}"

def create_request(topic, description, category_id, priority,
                   requester_id, assignee_id=None):
    """Создать новую заявку с валидацией и генерацией номера."""
    _validate_new_request(topic, description, category_id, priority)

    number = _generate_number()

    request = Request(
        id=0,
        request_number=number,
        topic=topic.strip(),
        description=description.strip(),
        priority=priority,
        created_at="",
        category_id=category_id,
        status_id=1,  # Новая
        requester_id=requester_id,
        assignee_id=assignee_id,
    )

    new_id = request_repository.create(request)
    return new_id

def get_all_requests():
    """Получить все заявки."""
    return request_repository.get_all()

def get_request(request_id):
    """Получить заявку по id. Если не найдена — ошибка."""
    request = request_repository.get_by_id(request_id)
    if not request:
        raise BusinessError(f"Заявка с id {request_id} не найдена")
    return request

def search_requests(query):
    """Поиск заявок."""
    if not query or not query.strip():
        return request_repository.get_all()
    return request_repository.search(query.strip())

def filter_requests(status_id=None, category_id=None):
    """Фильтрация заявок."""
    return request_repository.filter_by(status_id, category_id)

def change_status(request_id, new_status_id):
    """Сменить статус заявки по цепочке."""
    request = get_request(request_id)
    current = request.status_id

    if new_status_id not in STATUS_TRANSITIONS.get(current, []):
        current_name = STATUS_NAMES.get(current, current)
        new_name = STATUS_NAMES.get(new_status_id, new_status_id)
        raise BusinessError(
            f"Переход из статуса «{current_name}» "
            f"в «{new_name}» запрещён"
        )

    request_repository.update(request_id, status_id=new_status_id)

def assign_executor(request_id, assignee_id):
    """Назначить исполнителя на заявку."""
    request = get_request(request_id)

    if request.status_id == 4:
        raise BusinessError(
            "Нельзя назначить исполнителя на закрытую заявку"
        )

    request_repository.update(request_id, assignee_id=assignee_id)

def edit_request(request_id, topic=None, description=None,
                 category_id=None, priority=None):
    """Редактировать заявку. Запрещено для статуса «Закрыта»."""
    request = get_request(request_id)

    if request.status_id == 4:
        raise BusinessError("Нельзя редактировать закрытую заявку")

    if topic is not None and not topic.strip():
        raise ValidationError("Тема не может быть пустой")
    if description is not None and not description.strip():
        raise ValidationError("Описание не может быть пустым")

    request_repository.update(
        request_id,
        topic=topic,
        description=description,
        category_id=category_id,
        priority=priority,
    )

def delete_request(request_id):
    """Удалить заявку. Опасное действие — требует подтверждения."""
    request = get_request(request_id)

    if request.status_id == 2:
        raise BusinessError(
            "Нельзя удалить заявку в статусе «В работе» "
            "без подтверждения"
        )

    request_repository.delete(request_id)