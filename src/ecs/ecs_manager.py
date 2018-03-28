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

    def reset_components(self):
        for component in self.components:
            component.done = False

    # TODO
    def parse_event(self, event):
        for component in self.components:
            if component.accept(event):
                component.parse(event)
            else:
                component.done = True

    # TODO
    def request(self, request_id, event):
        if request_id == self.id:
            self.parse_event(event)
        elif request_id is None:
            self.manager.parse_request(self.id, event)


# Components hold tags, accepted events, and logic for each event
# TODO eventually: Ordering components and sorting, subscribing
class Component(ABC):

    def __init__(self, allowed_events, owner, priority=50, done=False, **kwargs):
        assert(isinstance(allowed_events, list))
        allowed_events += ["update"]
        self.allowed_events = list(chain(allowed_events, allowed_events))

        self.owner = owner
        self.manager = self.owner.manager

        self.priority = priority
        self.done = done

        self.id = "CO_" + str(uuid.uuid4())

        self.tags = {"active": True}
        for tag, value in kwargs.items():
            self.tags[tag] = value

    # TODO
    def accept(self, event):
        event_type = event.type
        if event_type in self.allowed_events:
            return True
        return False

    @abstractmethod
    def parse(self, event):
        pass


class Event(ABC):

    def __init__(self, moments, **kwargs):
        self.id = "EV_" + str(uuid.uuid4())

        self.moments = moments

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

    # TODO: Figure out
    def add_moment(self, moment, front=True):
        pass

    def remove_moment(self, moment, front=True):
        pass

    def current_moment(self):
        pass

    def add_event_type(self, id, event_type, front=True):
        pass

    def remove_event_type(self):
        pass


# TODO: EntityManager needs to be able to parse requests, possible entity in ECSM that parses requests
# TODO: Idea, component saves event, transforms current event into request with needed targets, and resumes original
class ECSManager:
    def __init__(self, window):
        self.window = window
        self.entities = []
        self.events = []

        self.id = "EV_" + str(uuid.uuid4())

    # Formats our registry of entities so we have easy access to the entity and its ID
    # TODO eventually: possibly used a named tuple
    def register_entity(self, entity):
        entity_id = entity.id
        entity_format = (entity_id, entity)
        self.entities.append(entity_format)

    def dispatch_event(self, event):
        target_id = event.current_target
        target = self.id_to_object(target_id)
        target.parse_event(event)

    # TODO: for example if an entity is requesting whether or not a tile is passable send coordinates to parse_request
    def parse_request(self, request):
        pass

    # Allows us to access the object from within IDs without actually referencing the object itself
    # TODO eventually: possibly used a named tuple
    def id_to_object(self, entity_id):
        for entity_format in self.entities:
            if entity_id == entity_format[0]:
                return entity_format[1]
        return None
