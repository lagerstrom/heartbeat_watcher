#!/usr/bin/env python3

from celery import Celery
from celery.signals import heartbeat_sent
from heartbeat_watcher import HeartbeatMonitor

heartbeat_monitor = HeartbeatMonitor(timeout=60)

app = Celery("healthcheck")
app.config_from_object('celeryconfig')


@heartbeat_sent.connect
def on_heartbeat(**kwargs):
    heartbeat_monitor.tick()
    print("Heartbeat sent:", kwargs)


@app.task(
    bind=True,
    max_retries=1,
    default_retry_delay=10,
    name='healthcheck.tasks.add',
)
def blender_add(self, num_one: int, num_two: int):
    """Adds two numbers together and returns the result."""
    return num_one + num_two
