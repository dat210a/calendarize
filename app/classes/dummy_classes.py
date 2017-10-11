class ShardTestingClass:
    def __init__(self, app):
        self.__app = app
        self.__id = len(app.config['shards']) + 1

        self.__app.config['shards'].append(self)
        print('Class with id {} created.'.format(self.__id))
