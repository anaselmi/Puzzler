import uuid
from abc import *


# Entities store components, and pass events to components
class Entity:

    def __init__(self, manager, *args):
        self.manager = manager
        self.components = []
        self.id = "EN_" + str(uuid.uuid4())
        for component in args:
            # Makes sure only components are accepted into the components list.
            if isinstance(component, ComponentABC):
                component.owner = self.id
                self.components.append(component)


    # Allow for updating components
    def add_component(self, component):
        if component not in self.components and isinstance(component, ComponentABC):
            component.owner = self.id
            self.components += component

    def remove_component(self, component):
        if component in self.components and isinstance(component, ComponentABC):
            self.components.remove(component)

    def parse_event(self, event):
        for component in self.components:
            if component.accept(event):
                component.parse(event)

    def sort_components(self):
        self.components = sorted(self.components)


# Components hold tags, accepted events, and logic for each event
# Components can subscribe and have the ability to subscribe to other events
# TODO: Ordering components and sorting, subscribing
class ComponentABC(ABC):

    def __init__(self, priority=50, **kwargs):
        self.priority = priority
        self.id = "CO_" + str(uuid.uuid4())

        self.allowed_events = list(self.allowed_events())

        self.allowed_tags = self.allowed_tags()
        for tag, value in kwargs.items():
            default_value = self.allowed_tags.get(tag)
            if value is None:
                if default_value is None:
                    raise AssertionError
                setattr(self, tag, default_value)
            else:
                setattr(self, tag, value)

    @abstractmethod
    def allowed_events(self):
        pass

    @abstractmethod
    def default_tags(self):
        pass

    def accept(self, event):
        event_type = event.type
        if event_type in self.allowed_events:
            return True
        return False

    @abstractmethod
    def parse(self, event):
        pass


class EventABC(ABC):

    def __init__(self, manager, creator_id, **kwargs):
        self.manager = manager
        self.id = "EV_" + str(uuid.uuid4())
        self.creator_id = creator_id
        self.message = []
        self.tags = {}
        for key, value in kwargs.items():
            self.tags[key] = value

    def __call__(self):
        return self.runtime()

    @abstractmethod
    def runtime(self):
        pass
