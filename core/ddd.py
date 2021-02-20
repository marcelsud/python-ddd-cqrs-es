import re as regex
from abc import ABC
from typing import List
from uuid import uuid4, UUID


class DomainEvent(ABC):
    pass


class UniqueDomainEntityId:
    uuid: UUID

    def __init__(self, uuid: UUID = None):
        if uuid is None:
            uuid = uuid4()

        self.uuid = uuid

    def to_primitive(self) -> str:
        return str(self.uuid)


class AggregateRoot(ABC):
    uuid: UniqueDomainEntityId
    pending_events = []

    def get_call_key(self):
        pass

    @staticmethod
    def load_from_history(events: List[DomainEvent]):
        pass

    def apply(self, event: DomainEvent):
        self.pending_events.append(event)
        method_name = regex.sub(r'(?<!^)(?=[A-Z])', '_', type(event).__name__).lower()
        getattr(self, f'apply_{method_name}')(event)

    def flush_events(self):
        events = self.pending_events.copy()
        self.pending_events.clear()

        return events

    def validate(self) -> bool:
        pass
