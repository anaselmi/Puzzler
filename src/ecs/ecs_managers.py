# TODO: Figure out how requesting information works, then implement it
class EntityManager:

    def __init__(self, window):
        self.window = window
        self.entities = []
        self.events = []

    def register_entity(self, entity):
        entity_id = entity.id
        entity_format = (entity_id, entity)
        self.entities.append(entity_format)

    def send(self, event, entity):
        pass

    def to_object(self, entity_id):
        pass


# Do I need this?
class ComponentManager:
    pass


class ECSManager:
    pass
