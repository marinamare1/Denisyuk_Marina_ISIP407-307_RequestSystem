from dataclasses import dataclass

@dataclass
class User:
    id: int
    full_name: str
    login: str
    email: str
    role_id: int

@dataclass
class Status:
    id: int
    name: str

@dataclass
class Category:
    id: int
    name: str

@dataclass
class Request:
    id: int
    request_number: str
    topic: str
    description: str
    priority: str
    created_at: str
    category_id: int
    status_id: int
    requester_id: int
    assignee_id: int | None

@dataclass
class Comment:
    id: int
    request_id: int
    author_id: int
    text: str
    created_at: str