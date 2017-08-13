from threading import Thread
from time import sleep

from chadt.component_status import ComponentStatus


class ChadtComponent:
    
    def __init__(self):
        self.status = ComponentStatus.STOPPED

    def start(self, thread_target):
        if self.status == ComponentStatus.STOPPED:
            self.status = ComponentStatus.RUNNING
            Thread(target = self.get_run_func(thread_target)).start()
        elif self.status == ComponentStatus.STOPPING:
            raise RuntimeError("Component is stopping, cannot restart yet.")

    def get_run_func(self, target_func):
        def f():
            while self.status == ComponentStatus.RUNNING:
                target_func()
                sleep(1)
            self.status = ComponentStatus.STOPPED
        return f

    def stop(self):
        if self.status == ComponentStatus.RUNNING:
            self.status = ComponentStatus.STOPPING

    def shutdown(self, connection = None):
        if self.status == ComponentStatus.RUNNING:
            self.stop()
        if connection is not None:
            connection.close()
