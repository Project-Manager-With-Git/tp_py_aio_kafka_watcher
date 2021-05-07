from typing import Dict, Any, Union
from pyloggerhelper import log
from pyproxypattern import Proxy
from aiokafka import AIOKafkaConsumer as KafkaConsumer


class KafkaWatcher(Proxy):
    @classmethod
    def create(clz, *topics: str, **configs: Any) -> "KafkaWatcher":
        """初始化创建一个监听对象.
        参数参考<https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html>
        """
        c = KafkaConsumer(*topics, **configs)
        p = clz(c)
        return p

    def _instance_check(self, instance: Any) -> bool:
        return isinstance(instance, KafkaConsumer)