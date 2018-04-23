import esper


class ProcessorManager(esper.World):

    def process(self, *args):
        """Call the process method on all Processors, in order of their priority.

        Call the *process* method on all assigned Processors, respecting their
        optional priority setting. In addition, any Entities that were marked
        for deletion since the last call to *World.process*, will be deleted
        at the start of this method call.

        :param args: Optional arguments that will be passed through to the
        *process* method of all Processors.
        """
        if self._dead_entities:
            for entity in self._dead_entities:
                self.delete_entity(entity, immediate=True)
            self._dead_entities.clear()

        for processor in self._processors:
            processor.process(*args)

    def dispatch_action(self, action):