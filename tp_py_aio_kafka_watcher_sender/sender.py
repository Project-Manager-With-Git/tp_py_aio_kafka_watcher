from typing import Dict, Any, Union
from pyloggerhelper import log
from pyproxypattern import Proxy
from kafka import KafkaProducer


class KafkaSender(Proxy):
    @classmethod
    def create(clz, **configs: Any) -> "KafkaSender":
        """初始化创建一个监听对象.
        参数参考<https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html>
        """
        c = KafkaProducer(**configs)
        p = clz(c)
        return p

    def _instance_check(self, instance: Any) -> bool:
        return isinstance(instance, KafkaProducer)