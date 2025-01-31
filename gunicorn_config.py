import os

# Server socket
port = int(os.getenv("PORT", 8080))
bind = f"0.0.0.0:{port}"

# Worker processes
workers = 1
worker_class = 'gthread'
threads = 8
timeout = 0

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Startup
preload_app = True
reload = False

# Reduce startup time
worker_tmp_dir = '/dev/shm' 