import threading, time, os

class HeartbeatMonitor:
    def __init__(self, timeout=60, check_interval=5):
        self.__check_interval = check_interval
        self.__last_heartbeat = time.time()
        self.__timeout = timeout
        self.__thread = threading.Thread(target=self.__watchdog)
        self.__thread.daemon = True
        self.__thread.start()

    def tick(self):
        self.__last_heartbeat = time.time()

    def __watchdog(self):
        while True:
            time.sleep(self.__check_interval)
            if time.time() - self.__last_heartbeat > self.__timeout:
                print("Heartbeat timeout. Exiting container.")
                os._exit(1)  # force container crash
