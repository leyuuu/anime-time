import requests
import json
import time
import os
import sys
import subprocess
import abc
from lxml import etree
from rich import print
from typing import overload,Dict, List

class Aria2Downloader():
    def __init__(self):
        ...

    def generate_input_file(self, targets: List[str]):
        targets = '\n'.join(targets)
        open("dlist.txt", "w+").write(targets)



class RSSReader():
    max_item_size = 5
    def __init__(self,config):
        self.config = config
    def export_download_link(self) -> List[str]:
        rss_list = self.config["source"]
        for rssitem in rss_list:
            rss_text = requests.get(rssitem["link"]).text
            selector = etree.fromstring(rss_text)
            for one in selector.xpath("//rss/channel/item/link/text()")[:self.max_item_size]:
                yield one


class ConfigLogger():
    log_size = 100
    def __init__(self,config, config_file):
        self.config = config
        self.__config_file = config_file
    def filter(self, links) -> List[str]:
        history = config["log"]
        return list(filter(lambda x: x not in history, links))

    def log(self, links: List[str]) -> bool:
        log = links + config["log"]
        config["log"] = log[:self.log_size]
        config_file.seek(0)
        config_file.truncate()
        config_file.write(json.dumps(config, indent=4))
        return True

config_file = open("config.json", "r+")
config = json.load(config_file)

if __name__ == "__main__":
    downloader = Aria2Downloader()
    rss = RSSReader(config)
    logger = ConfigLogger(config, config_file)
    links = list(rss.export_download_link())
    links = logger.filter(links)
    print(":tada:",f"{len(links)} file need to download")
    if len(links) == 0:
        print("No thing to download, program exit.")
        exit(1)
    downloader.generate_input_file(links)
    logger.log(links)

