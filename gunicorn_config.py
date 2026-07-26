workers = 4
worker_class = "uvicorn_worker.GunicornUVicornWorker"

keepalive = 5

max_requests = 2000
max_requests_jitter = 200

timeout = 120
graceful_timeout  = 30

accesslog = "-"
errorlog = "-"
loglevel = "info"

access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" '
    '%(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
)
