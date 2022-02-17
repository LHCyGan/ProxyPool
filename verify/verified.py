import time
from storages.redisStorage import RedisClient
import asyncio
import aiohttp
from urllib.parse import urljoin

from confing import *

class TEST:
    def __init__(self) -> None:
        self.redis = RedisClient()
        
    
    async def test_single_proxy(self, proxy):
        """测试单个代理"""
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = urljoin('http://', proxy)
                print('testing', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, time_out=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.max(proxy)
                        print('proxy is ok : ', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('proxy is no : ', proxy)
                        
            except(aiohttp.ClientError, aiohttp.ClientConnectionError, AttributeError, TimeoutError):
                self.redis.decrease(proxy)
                print('proxy request failure : ', proxy)

    def run(self):
        print('run............')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i:i+BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print('testing error : ', e)