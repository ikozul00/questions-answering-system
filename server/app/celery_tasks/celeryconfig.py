

# RabbitMQ settings
broker_url = 'amqp://ivana:***@localhost:5672/celery_vhost'
                           
broker_transport_options = {'confirm_publish': True}                 
broker_heartbeat = 0
broker_pool_limit = None
broker_connection_timeout = 20
broker_connection_retry = True
broker_connection_max_retries = 100

ignore_result = False
