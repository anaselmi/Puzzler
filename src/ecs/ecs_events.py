from ecs_base_classes import EventABC


class MoveEvent(EventABC):

    def runtime(self):
        active = self.tags.get("active")
        if not active:
            return None

        target = self.tags.get("target")
        dx = self.tags.get("dx")
        dy = self.tags.get("dy")
        if target and dx and dy:
            target_object = self.manager.to_object(target)
            self.manager.send(self, target_object)




# TODO: Add a render event