import esper


# Not sure whether or not this object should facilitate inter-processor communication
class ProcessorManager(esper.World):

    def process(self, *args):
        # THIS REALLY NEEDS TO BE FIXED ONCE IT'S WORKING
        if self._dead_entities:
            for entity in self._dead_entities:
                self.delete_entity(entity, immediate=True)
            self._dead_entities.clear()

        action = args[0]

        for processor in self._processors:
            processor.process(*args)
        return action
