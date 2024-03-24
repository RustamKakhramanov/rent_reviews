import json
import redis


class Redis:
    connection = redis.Redis(
        host='localhost', port=6379, charset="utf-8", db=0)

    @staticmethod
    def query() -> redis.Redis:
        return Redis.connection

    def get(self, key) -> redis.Redis:
        data = self.query().get(key)

        if (data != 'null' or data != None):
            try:
                return json.loads(data)
            except Exception as e:
                return data
        
        return None

    def set(self, key, data, to_json=False) -> bool:
        if (to_json):
            try:
                for_write = json.dumps(data).encode('utf-8')
            except ValueError as e:
                return False
        else:
            for_write = data

        return self.query().set(key, for_write)
    
    def delete(self, key):
        self.query().delete(key)
