def init_sized_object(name, size, _logger):
    width, height = size
    _logger.debug("New %s %d units wide and %d units tall created." % (name, width, height))
