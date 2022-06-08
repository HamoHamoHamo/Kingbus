from django.db import connection
# from django.utils.log import getLogger
from logging import getLogger

logger = getLogger(__name__)

# class QueryCountDebugMiddleware(object):
#     """
#     This middleware will log the number of queries run
#     and the total time taken for each request (with a
#     status code of 200). It does not currently support
#     multi-db setups.
#     """
#     def __init__(self, name):
#         self.name = name

#     def __call__(self, request):
#         self.process_response(request)

    
#     def process_response(self, request):
#         # if response.status_code == 200:
#         # print(request)
#         total_time = 0
#         # print(query)

#         # for query in connection.queries:
#         #     query['time'] = query.get('time')
#         #     if query['time'] is None:
#         #         # django-debug-toolbar monkeypatches the connection
#         #         # cursor wrapper and adds extra information in each
#         #         # item in connection.queries. The query time is stored
#         #         # under the key "duration" rather than "time" and is
#         #         # in milliseconds, not seconds.
#         #         query['time'] = query.get('duration', 0) / 1000
#         #     total_time += float(query['time'])

#         logger.debug('%s queries run, total %s seconds' % (len(connection.queries), total_time))