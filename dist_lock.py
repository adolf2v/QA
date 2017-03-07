import pymongo
from threading import Thread
import threading
import redis
from redis_netlock import dist_lock
client=pymongo.MongoClient(host="127.0.0.1",port=27017)
tdb=client['kyspider']
post=tdb['test']
post.find_and_modify(query={"_id":1},update={"$inc":{"_id":1}},upsert=True)

r=redis.Redis(connection_pool=redis.BlockingConnectionPool(max_connections=15, host='172.16.1.21', port=6379))

def goumai(i):
    with dist_lock('test',r):
        num=post.find_one({"_id":2})
        m=num.get('num')
        print m
        post.update({"_id":2},{"$set":{"num":m+i}})

if __name__ == "__main__":
    a=[]
    for x in xrange(6):
        a.append(Thread(target=goumai,args=(5,)))
    print a
    for item in a:
        item.start()
    for item in a:
        item.join()
