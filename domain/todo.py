from core.ddd import AggregateRoot, DomainEvent, UniqueDomainEntityId
from enum import Enum
from datetime import datetime
from typing import List
from core.guard import Guard, Types


class ToDoCreatedEvent(DomainEvent):
    uuid: UniqueDomainEntityId
    description: str
    created_at: datetime

    def __init__(self, uuid: UniqueDomainEntityId, description: str, created_at: datetime):
        self.uuid = uuid
        self.description = description
        self.created_at = created_at


class ToDoMarkedAsDoneEvent(DomainEvent):
    to_do_uuid: UniqueDomainEntityId
    done_at: datetime

    def __init__(self, to_do_uuid: UniqueDomainEntityId, done_at: datetime):
        self.to_do_uuid = to_do_uuid
        self.done_at = done_at


class ToDoStatus(Enum):
    Done = "done"
    Pending = "pending"


class ToDo(AggregateRoot):
    uuid: UniqueDomainEntityId
    status: ToDoStatus
    description: str
    done_at: datetime
    created_at: datetime

    @staticmethod
    def load_from_history(events: List[DomainEvent]):
        to_do = ToDo()
        for event in events:
            to_do.apply(event)

        return to_do

    @staticmethod
    def create(description: str):
        Guard.is_type(description, Types.Str)
        event = ToDoCreatedEvent(UniqueDomainEntityId(), description, datetime.now())
        to_do = ToDo()
        to_do.apply(event)

        return to_do

    def mark_as_done(self):
        event = ToDoMarkedAsDoneEvent(self.uuid, datetime.now())
        self.apply(event)

    def apply_to_do_created_event(self, event: ToDoCreatedEvent):
        self.uuid = event.uuid
        self.description = event.description
        self.status = ToDoStatus.Pending
        self.created_at = event.created_at

    def apply_to_do_marked_as_done_event(self, event: ToDoMarkedAsDoneEvent):
        self.status = ToDoStatus.Done
        self.done_at = event.done_at
