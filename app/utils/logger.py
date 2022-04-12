import logging

from app.common.config import conf


logging.basicConfig(
    filename="./controller.log",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="[%(levelname)s]\t%(asctime)s.%(msecs)03d    %(message)s"
)

logger = logging.getLogger("controller")

c = conf()
if c.DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
