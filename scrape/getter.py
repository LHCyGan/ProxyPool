from storages.redisStorage import RedisClient
from getproxy import Crawler
from confing import POOL_UPPER_THRESHOLD

class Getter:
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()
        
    def is_over_threshold(self):
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
        
    def run(self):
        print("爬取开始。。。。。。。。。。。")
        if not self.is_over_threshold:
            proxies = self.crawler.get_proxies()
            for proxy in proxies:
                self.redis.add(proxy)