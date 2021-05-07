import os
import time
from pathlib import Path
from typing import Dict, Union
from schema_entry import EntryPoint
from pyloggerhelper import log
# from watchdog.observers.polling import PollingObserver as Observer # 如果在docker中部署可以用PollingObserver
from sender import KafkaSender


class Application(EntryPoint):
    _name = "tp_py_aio_kafka_watcher_sender"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": [
            "app_version",
            "app_name",
            "log_level",
            "send_kafka_urls",
        ],
        "properties": {
            "app_version": {
                "type": "string",
                "title": "v",
                "description": "应用版本",
                "default": "0.0.0"
            },
            "app_name": {
                "type": "string",
                "title": "n",
                "description": "应用名",
                "default": "tp_py_aio_kafka_watcher_watcher"
            },
            "log_level": {
                "type": "string",
                "title": "l",
                "description": "log等级",
                "enum": ["DEBUG", "INFO", "WARN", "ERROR"],
                "default": "DEBUG"
            },
            "send_kafka_urls": {
                "type": "array",
                "title": "u",
                "description": "监听的kafka集群地址",
                "items": {
                    "type": "string",
                }
            },
            "send_kafka_options": {
                "type": "array",
                "title": "o",
                "description": "监听的kafka的配置项,使用<key>::<value>的形式",
                "items": {
                    "type": "string",
                }
            }
        }
    }

    def do_main(self) -> None:
        log.initialize_for_app(
            app_name=self.config.get("app_name"),
            log_level=self.config.get("log_level")
        )
        log.info("获取任务配置", config=self.config)
        send_kafka_urls = self.config["send_kafka_urls"]

        send_kafka_options: Dict[str, Union[str, int, bool]] = {}
        _send_kafka_options = self.config.get("send_kafka_options")
        if _send_kafka_options:
            for kvs in _send_kafka_options:
                ks, vs = kvs.split("::")
                if vs.isdigit():
                    v = int(vs)
                elif vs.lower() == "true":
                    v = True
                elif vs.lower() == "false":
                    v = False
                else:
                    v = vs
                send_kafka_options[ks] = v
        sender = KafkaSender.create(
            bootstrap_servers=send_kafka_urls,
            **send_kafka_options
        )
        try:
            sender.send(topic="topic1-1-1", value=b"msg1", key=b"key1", headers=[("h1", b"h1"), ("h2", b"h2")])
            log.info("send msg",topic="topic1-1-1", value=b"msg1", key=b"key1",headers=[("h1", b"h1"), ("h2", b"h2")])
        except (KeyboardInterrupt, SystemExit):
            log.info('kafka sender stoped')
        except Exception as e:
            log.error("kafka sender get error", err=type(e), err_msg=str(e), exc_info=True, stack_info=True)
        finally:
            sender.close()