import uuid
from abc import *
from itertools import chain


# Entities store components, and pass events to components
class Entity:

    def __init__(self, manager, *args):
        self.manager = manager
        self.components = []
        self.id = "EN_" + str(uuid.uuid4())
        for component in args:
            # Makes sure only components are accepted into the components list.
            if isinstance(component, Component):
                self.components.append(component)
        self.register_components()

    # TODO: Allow for updating components
    def add_component(self, component):
        if component not in self.components and isinstance(component, Component):
            component.owner = self.id
            self.components += component

    def remove_component(self, component):
        if component in self.components and isinstance(component, Component):
            self.components.remove(component)

    def register_components(self):
        for component in self.components:
            component.owner = self.id

    def activate_components(self):
        for component in self.components:
            component.active = True

    def parse_event(self, event):
        for component in self.components:
            if component.accept(event):
                component.parse(event)
            else:
                component.done = True

    def request(self, request_id, event):
        if request_id == self.id:
            self.parse_event(event)
        elif request_id is None:
            self.manager.parse_request(self.id, event)

    def sort_components(self):
        self.components = sorted(self.components)


# Components hold tags, accepted events, and logic for each event
# Components can subscribe and have the ability to subscribe to other events
# TODO eventually: Ordering components and sorting, subscribing
class Component(ABC):

    def __init__(self, allowed_events, owner, priority=50, parsed=False, **kwargs):
        assert(isinstance(allowed_events, list))
        allowed_events += ["update"]
        self.allowed_events = list(chain(allowed_events, allowed_events))

        self.owner = owner
        self.manager = self.owner.manager
        self.priority = priority
        self.parsed = parsed

        self.id = "CO_" + str(uuid.uuid4())

        self.tags = {"active": True}
        for tag, value in kwargs.items():
            self.tags[tag] = value

    def accept(self, event):
        event_type = event.type
        if event_type in self.allowed_events:
            return True
        return False

    def tag_ensure(self, **kwargs):
        for tag, default_value in kwargs.items():
            value = self.tags.get(tag)
            if default_value is None and value is None:
                raise KeyError("value required for tag " + tag)
            if value is None:
                self.tags[tag] = default_value

    @abstractmethod
    def parse(self, event):
        pass

    @abstractmethod
    def parse_request(self, request):
        pass


class Event(ABC):

    def __init__(self, event_types, creator_id, targets, **kwargs):
        self.id = "EV_" + str(uuid.uuid4())
        self.message = []

        self.event_types = event_types
        self.creator_id = creator_id
        self.targets = targets

        self.tags = {"active": True}
        for tag, value in kwargs.items():
            self.tags[tag] = value

    # Use to get a tag if it exists or to get a default parameter if it does not
    def get_tag(self, tag, default=None):
        value = self.tags.get(tag)
        if value:
            return value
        return default

    # Use if you want to get a tag that should be there
    def grab_tag(self, tag):
        value = self.tags.get(tag)
        if value is None:
            raise KeyError("expected tag to have a value, but there was none" + tag)

    # Use if you are not certain a tag has been added and want to add a default value
    def update_tag(self, tag, value):
        self.tags.update({tag: value})

    # Use if a tag should be there and are fine with raising an error if it hasn't been
    def change_tag(self, tag, value):
        if self.get_tag(tag) is None:
            raise KeyError("expected tag to have a value, but there was none" + tag)
        self.tags[tag] = value

    # Use if a tag hasn't been added or you want to change a tag that might be there
    def add_tag(self, tag, value):
        self.tags[tag] = value

    # Use this to remove a tag, whether or not it exists
    def remove_tag(self, tag):
        self.tags.pop(tag, None)

    def add_target(self, target):
        pass

    def remove_target(self):
        pass

    def add_type(self):
        pass

    def remove_type(self):
        pass

    def current_target(self):
        pass


# TODO: EntityManager needs to be able to parse requests
# TODO: Idea, component saves event, transforms current event into request with needed targets, and resumes original
class ECSManager:
    def __init__(self, window):
        self.window = window
        self.entities = []
        self.events = []

        self.id = "EV_" + str(uuid.uuid4())

    # Formats our registry of entities so we have easy access to the entity and its ID
    def register_entity(self, entity):
        entity_id = entity.id
        entity_format = (entity_id, entity)
        self.entities.append(entity_format)

    # TODO
    def dispatch_event(self, event):
        target_id = event.grab_tag("target")
        target = self.id_to_object(target_id)
        self.send(event, target)

    def send(self, event, target):
        target.parse_event(event)

    # TODO: for example if an entity is requesting whether or not a tile is passable send coordinates to parse_request
    def parse_request(self, request):
        pass

    # Allows us to access the object from within IDs without actually referencing the object itself
    def id_to_object(self, entity_id):
        for entity_format in self.entities:
            if entity_id == entity_format[0]:
                return entity_format[1]