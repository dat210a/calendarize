class ShardTestingClass:
    def __init__(self, app):
        self.__app = app
#        self.__id = len(app.config['shards']) + 1

#        self.__app.config['shards'].append(self)
#        print('Class with id {} created.'.format(self.__id))

    def work(self):
        print('{} working...'.format(self.__id))

    def __enter__(self):
        return self

#    def __exit__(self, exc_type, exc_val, exc_tb):
#       self.__app.config['shards'].remove(self)