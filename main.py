import logging

from src.fonts import Courier12
from src.consts import SIZE, TITLE, FPS
from src.engine import Engine

log_level = logging.DEBUG
logging.basicConfig(level=log_level,
                    datefmt='%I:%M:%S%p',
                    format='%(asctime)s  %(name)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

logger.info("Program started.")
engine = Engine(SIZE, Courier12, TITLE, FPS)
logger.debug("Engine created.")
engine.create_play_state()
engine.loop()
logger.info("Program ended.")
