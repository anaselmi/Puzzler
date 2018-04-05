import uuid


# Entities store components, and pass events to components
# Idea: action order is a dictionary where the key is the action and the value is the sorted list of components
class Entity:
    class_id = "EN_"

    def __init__(self, manager, components, name=None):
        if name is None:
            name = str(uuid.uuid4())
        self.id = Entity.class_id + name
        self.manager = manager
        self.components = components
        self.register_components()

    def add_component(self, component):
        self.components.append(component)

    def remove_component(self, component):
        self.components.remove(component)

    def register_components(self):
        for component in self.components:
            component.owner = self.id

    # Orders components by which parses event first to ensure logical data flow
    def prioritize_components(self, action):
        action_order = []
        for component in self.components:
            priority = component.accepts(action)
            if priority is not None:
                action_order.append([component, priority])
        action_order = [x[0] for x in sorted(action_order, key=lambda x: x[1])]
        return action_order

    def parse_event(self, event):
        action = None
        while event.has_actions():
            if action != event.get_action():
                action = event.get_action()
                action_order = self.prioritize_components(action)
            if not action_order:
                event.remove_action(self.id, action)
                continue
            # Smaller priority number implies higher priority
            for component in action_order:
                # If a component returns None, then it has added a new event to the front
                if component.parse(event) is None:
                    break


class Event:
    class_id = "EV_"

    def __init__(self, actions, tags):
        self.id = Event.class_id + str(uuid.uuid4())
        self.actions = actions
        self.tags = tags

    @staticmethod
    def create_action(request_id, action):
        return [request_id, action]

    def add_action_b(self, request_id, action):
        new_action = self.create_action(request_id, action)
        self.actions.append(new_action)

    def add_action_f(self, request_id, action):
        new_action = self.create_action(request_id, action)
        self.actions.insert(0, new_action)

    def remove_action(self, request_id, action):
        if request_id[0:3] == Entity.class_id and request_id != action[0]:
            return None # TODO LOG ERROR HERE
        # HOW AM I GOING TO LOG ERRORS???
        self.actions.remove(action)
        return ...

    def get_action(self):
        if self.has_actions():
            return self.actions[0]

    def has_actions(self):
        if not self.actions:
            return False
        return True


class Component:
    class_id = "CO_"

    def __init(self, valid_actions, tags):
        self.id = Component.class_id + str(uuid.uuid4())
        self.valid_actions = valid_actions
        self.tags = tags

    def accepts(self, action):
        # Checks if the action is in the list of valid actions
        return any([x[0] == action for x in self.valid_actions])

    def parse(self, event):
        raise NotImplementedError
