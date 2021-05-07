import os
import time
import asyncio
from pathlib import Path
from typing import Dict, Union
from schema_entry import EntryPoint
from pyloggerhelper import log
# from watchdog.observers.polling import PollingObserver as Observer # 如果在docker中部署可以用PollingObserver
from watcher import KafkaWatcher
from handdler import handdler


class Application(EntryPoint):
    _name = "tp_py_aio_kafka_watcher_watcher"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": [
            "app_version",
            "app_name",
            "log_level",
            "watch_kafka_topics",
            "watch_kafka_urls",
            "watch_kafka_group_id",
            "watch_kafka_auto_offset_reset"
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
            "watch_kafka_topics": {
                "type": "array",
                "title": "t",
                "description": "监听的topic列表",
                "items": {
                    "type": "string",
                }
            },
            "watch_kafka_urls": {
                "type": "array",
                "title": "u",
                "description": "监听的kafka集群地址",
                "items": {
                    "type": "string",
                }
            },
            "watch_kafka_group_id": {
                "type": "string",
                "title": "g",
                "description": "监听的kafka集群的消费者群组id"
            },
            "watch_kafka_auto_offset_reset": {
                "type": "string",
                "title": "a",
                "description": "监听的kafka集群中数据的起始位置",
                "enum": ["earliest", "latest"],
                "default": "latest"
            },
            "watch_kafka_options": {
                "type": "array",
                "title": "o",
                "description": "监听的kafka的配置项,使用<key>::<value>的形式",
                "items": {
                    "type": "string",
                }
            },
            "use_uvloop": {
                "type": "boolean",
                "description": "是否使用uvloop作为事件循环",
                "default": False
            }
        }
    }

    async def watch(self) -> None:
        watch_kafka_topics = self.config["watch_kafka_topics"]
        watch_kafka_urls = self.config["watch_kafka_urls"]
        watch_kafka_group_id = self.config["watch_kafka_group_id"]
        watch_kafka_auto_offset_reset = self.config["watch_kafka_auto_offset_reset"]
        watch_kafka_options: Dict[str, Union[str, int, bool]] = {}
        _watch_kafka_options = self.config.get("watch_kafka_options")
        if _watch_kafka_options:
            for kvs in _watch_kafka_options:
                ks, vs = kvs.split("::")
                if vs.isdigit():
                    v = int(vs)
                elif vs.lower() == "true":
                    v = True
                elif vs.lower() == "false":
                    v = False
                else:
                    v = vs
                watch_kafka_options[ks] = v
        try:
            async with KafkaWatcher.create(
                *watch_kafka_topics,
                bootstrap_servers=watch_kafka_urls,
                group_id=watch_kafka_group_id,
                auto_offset_reset=watch_kafka_auto_offset_reset,
                **watch_kafka_options
            ) as watcher:
                async for msg in watcher:
                    await handdler(msg)
        except Exception as e:
            log.error("kafka watcher get error", err=type(e), err_msg=str(e), exc_info=True, stack_info=True)

    def _do_main(self) -> None:
        log.initialize_for_app(
            app_name=self.config.get("app_name"),
            log_level=self.config.get("log_level")
        )
        log.info("获取任务配置", config=self.config)

        if self.config.get("use_uvloop"):
            import uvloop
            uvloop.install()
            log.warn('using UVLoop')
        try:
            asyncio.run(self.watch())
        except (KeyboardInterrupt, SystemExit):
            log.info('kafka watcher stoped')
