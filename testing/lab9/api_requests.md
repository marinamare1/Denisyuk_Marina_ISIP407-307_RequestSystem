Коллекция API-запросов

1. GET /health
Запрос: GET http://localhost:8000/health
Ответ: 200 OK
{"status": "ok"}

2. GET /requests
Запрос: GET http://localhost:8000/requests
Ответ: 200 OK
[{...}, {...}]

3. GET /requests/1
Запрос: GET http://localhost:8000/requests/1
Ответ: 200 OK
{"id": 1, "request_number": "REQ-2026-001", ...}

4. GET /requests/999
Запрос: GET http://localhost:8000/requests/999
Ответ: 404 Not Found
{"detail": "Заявка с id 999 не найдена"}

5. POST /requests
Запрос: POST http://localhost:8000/requests
{"topic": "API тест", "description": "Проверка", "category_id": 1,
 "priority": "Средний", "requester_id": 4}
Ответ: 201 Created
{"id": 13, "message": "Заявка создана"}

6. POST /requests (ошибка)
Запрос: POST http://localhost:8000/requests
{} (пустое тело)
Ответ: 422 Unprocessable Entity
{"detail": [{"type": "json_invalid", ...}]}

7. PATCH /requests/1
Запрос: PATCH http://localhost:8000/requests/1
{"topic": "Обновлённая тема"}
Ответ: 200 OK
{"id": 1, "topic": "Обновлённая тема", ...}

8. PATCH /requests/1/status
Запрос: PATCH http://localhost:8000/requests/1/status
{"status_id": 2}
Ответ: 200 OK
{"id": 1, "status_id": 2, "message": "Статус изменён"}

9. PATCH /requests/1/status (ошибка)
Запрос: PATCH http://localhost:8000/requests/1/status
{"status_id": 4}
Ответ: 400 Bad Request
{"detail": "Переход из статуса «В работе» в «Закрыта» запрещён"}

10. DELETE /requests/10
Запрос: DELETE http://localhost:8000/requests/10
Ответ: 400 Bad Request
{"detail": "Нельзя удалить заявку в статусе «В работе» без подтверждения"}

11. GET /users
Запрос: GET http://localhost:8000/users
Ответ: 200 OK
[{...}, {...}]

12. GET /statuses
Запрос: GET http://localhost:8000/statuses
Ответ: 200 OK
[{"id": 1, "name": "Новая"}, ...]

13. GET /categories
Запрос: GET http://localhost:8000/categories
Ответ: 200 OK
[{"id": 1, "name": "ПО и системы"}, ...]