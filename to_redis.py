import redis
 
r = redis.Redis(host='192.168.42.132', port=6379)
r.set('aaaaaaaaaaa', 'Bar')
print(r.get('foo'))