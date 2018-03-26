import uuid
from abc import *


# Entities store components, and pass events to components
class Entity:

    def __init__(self, *args):
        self.components = []
        for component in args:
            # Makes sure only components are accepted into the components list.
            if isinstance(component, ComponentABC):
                self.components.append(component)
        # TODO: Ensure player has an id of "EN_Player"
        self.id = "EN_" + str(uuid.uuid4())

    def add_component(self, component):
        if component not in self.components and isinstance(component, ComponentABC):
            self.components += component

    def remove_component(self, component):
        if component in self.components and isinstance(component, ComponentABC):
            self.components.remove(component)

    def parse_event(self, event):
        for component in self.components:
            if component.accept(event.type):
                component.parse(event)

    def sort_components(self):
        self.components = sorted(self.components)


# Components hold tags, accepted events, and logic for each event
# Components can subscribe and have the ability to subscribe to other events
# How do we order components in a logical order?
# TODO: Ordering components, sorting, subscribing, event logic
# TODO: Ensure all components have some form of parameters for tags and accepted events
# TODO: Implement way for components to parse events according to a priority
class ComponentABC(ABC):

    def __init__(self, priority=50, **kwargs):
        # TODO Parse kwarg key to see if accepted, then parse value to see if accepted
        self.priority = priority

        self.allowed_events = list(self.allowed_events())

        self.allowed_tags = self.allowed_tags()
        for tag, value in kwargs.items():
            value_type = self.allowed_tags.get(tag)
            if isinstance(value, value_type) or value is None:
                setattr(self, tag, value)
            else:
                # TODO: Either raise error or print to messagewin
                pass

    @abstractmethod
    def allowed_events(self):
        pass

    @abstractmethod
    def allowed_tags(self):
        pass

    def accept(self, event_type):
        if event_type in self.allowed_events:
            return True
        return False

    @abstractmethod
    def parse(self, event):
        pass

    # TODO: Figure out how requesting information works, then implement it
    # @abstractmethod
    # def request(self):
    #     pass


# TODO
class EventABC(ABC):

    def __init__(self, creator_id, **kwargs):
        self.id = "EV_" + str(uuid.uuid4())
        self._creator_id = creator_id
        self.message = []

    def __call__(self):
        return self.runtime()

    @abstractmethod
    def runtime(self):
        pass

    @abstractmethod
    def allowed_events(self):
        pass

    @abstractmethod
    def allowed_tags(self):
        pass

