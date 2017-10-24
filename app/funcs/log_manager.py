import logging


def setup_logger(concern):
    try:
        lg = logging.getLogger(concern)
        handler = logging.FileHandler(filename='{}.log'.format(concern), encoding='utf-8', mode='a')
        fmt = logging.Formatter('[%(asctime)s]:%(module)s:%(levelname)s: %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(fmt)
        lg.addHandler(handler)
        return lg
    except PermissionError as e:
        print('{}\n'
              'WARNING: Logging not enabled.\n'
              'If you get this error, change your IDE working directory.\n'
              'The application will still work, but nothing will be logged.'.format(e))
        # In PyCharm, go to Run>Edit Configuration to set the working directory to the calendarize folder.


def teardown(logger):
    handlers = logger.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        logger.removeHandler(hdlr)


def request_data(req):
    res = '{} requested by {}'.format(req.url, req.remote_addr)
    return res


def log_basic(request):
    # This handles logging of basic data that should be logged for all requests
    try:
        logging.info(request_data(request))
    except Exception as e:
        print(e)

