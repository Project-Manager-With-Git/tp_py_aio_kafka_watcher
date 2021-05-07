from aiokafka.structs import ConsumerRecord
from pyloggerhelper import log


async def handdler(msg: ConsumerRecord) -> None:
    log.info("get msg", msg=msg)
