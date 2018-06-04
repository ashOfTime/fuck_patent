from proxy import ProxyPool
from setting import api,redis_host,redis_port,min_ip



proxypool = ProxyPool(redis_host, redis_port)
proxypool.mother(api, min_ip)

