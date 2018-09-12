## Broker settings.
broker_url = 'pyamqp://guest:guest@localhost:5672/test'

# # List of modules to import when the Celery worker starts.
# imports = ('celeries.tasks',)

## Using the database to store task state and results.
result_backend = 'redis://localhost:6379'

# task_annotations = {'tasks.add': {'rate_limit': '10/s'}}
#
#
# # using serializer name
# accept_content = ['json']

# # or the actual content-type (MIME)
# accept_content = ['application/json']

'''
reply_to:	f29a341a-2d44-3400-b6e2-8b67428c0a81
correlation_id:	a5a897d4-ed78-403e-8234-66f43d6e4300
delivery_mode:	2
headers:	
argsrepr:	(2, 3)
eta:	undefined
expires:	undefined
group:	undefined
id:	a5a897d4-ed78-403e-8234-66f43d6e4300
kwargsrepr:	{}
lang:	py
origin:	gen30197@H.local
parent_id:	undefined
retries:	0
root_id:	a5a897d4-ed78-403e-8234-66f43d6e4300
shadow:	undefined
task:	celeries.tasks.add
timelimit:	undefined
undefined
content_encoding:	utf-8
content_type:	application/json
'''
