from core.ddd import AggregateRoot, DomainEvent, UniqueDomainEntityId
from typing import List
from core.guard import Guard, Types


class CustomerCreatedEvent(DomainEvent):
    name: str
    uuid: UniqueDomainEntityId

    def __init__(self, uuid: UniqueDomainEntityId, name: str):
        self.uuid = uuid
        self.name = name


class CustomerNameChangedEvent(DomainEvent):
    new_name: str

    def __init__(self, new_name: str):
        self.new_name = new_name


class Customer(AggregateRoot):
    uuid: UniqueDomainEntityId = None
    name: str = None

    @staticmethod
    def load_from_history(events: List[DomainEvent]):
        customer = Customer()
        for event in events:
            customer.apply(event)

        return customer

    @staticmethod
    def create(name: str):
        Guard.is_type(name, Types.Str)
        event = CustomerCreatedEvent(UniqueDomainEntityId(), name)
        customer = Customer()
        customer.apply(event)

        return customer

    def change_name(self, new_name: str):
        Guard.is_type(new_name, Types.Str)
        event = CustomerNameChangedEvent(new_name)
        self.apply(event)

    def apply_customer_created_event(self, event: CustomerCreatedEvent):
        self.uuid = event.uuid
        self.name = event.name

    def apply_customer_name_changed_event(self, event: CustomerNameChangedEvent):
        self.name = event.new_name

    def validate(self):
        Guard.is_type(self.name, Types.Str)
        return True
