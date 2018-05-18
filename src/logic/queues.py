class EventQueue:
    def __init__(self, world):
        self.world = world
        self.queue = []

    # Pushing adds a new event, but does not delete the old one
    def push(self, event):
        self.world.dispatch(event)

    # Replacing adds a new event, which destroys the old one if successful
    def replace(self, event):
        self.world.dispatch(event)

    # Determines whether an event is negated/replaced, also adds required information
    def pre_event(self, event):
        pass

    # Modifies/alters an event right before it happens
    def modify_event(self, event):
        pass

    # Applies modified event to targets
    def apply_event(self, event):
        pass

    # Post event adds new events to the queue as a direct result of the event
    def post_event(self, event):
        pass

    def furthest_dependant_root(self, event):
        if event.dependant:
            return self.furthest_dependant_root(event.root)
        return event


class TurnQueue:
    def __init__(self, world):
        self.world = world
        self.turns = 0

    def next_turn(self):
        self.world.get_component()