

class BaseRepository:
    def to_list(self, sql):
        return [item for item in sql]