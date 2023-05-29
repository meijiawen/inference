import queue
import time

from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
from apscheduler.schedulers.blocking import BlockingScheduler

from server import transfer_server
from task import Task
from logger import logger


class CancelContext:

    def __init__(self):
        self.killed_task = []

    def cancel(self, task_id):
        self.killed_task.append(task_id)

    def cancelled(self, task_id):
        return task_id in self.killed_task


class Agent:

    def __init__(self, concurrent: int) -> None:
        self.num = 0
        self.concurrent = concurrent

        self.submit_task = queue.Queue(maxsize=concurrent)
        self.finished_task = queue.Queue()
        self.process_task = {}


        self.thread_pool_executor = ThreadPoolExecutor(max_workers=concurrent)
        self.future_list = []

        self.exit = False

        self.concel_context = CancelContext()

        self.ping_ok = True

    def exit(self, flag: bool):
        self.exit = flag

    def ping(self):
        self.ping_ok = transfer_server.ping()

    def fetch_task(self):
        """
            从server端获取可执行的任务
        """
        if self.ping_ok and self.num <= self.concurrent:
            try:
                task = transfer_server.getTask()
                if task is not None:
                    self.num = self.num + 1
                    self.submit_task.put(task)
            except Exception as ex:
                logger.error("fetch task error", ex)

    def sync_task(self):
        try:
            task = self.finished_task.get()
            ok = transfer_server.syncTask(task)

            # 如果同步失败,则需要重新同步
            if not ok:
                self.finished_task.put(task)
        except Exception as ex:
            logger.error("sync task error", ex)

    def run_task(self, task: Task):
        task.run()
        self.finished_task.put(task)
        self.num = self.num - 1

    def handle_task(self):
        task = self.submit_task.get()
        if self.concel_context.cancelled(task.task_id):
            logger.info(f"task is cancelled: %s", task.task_id)
            return

        self.process_task[task.task_id] = task
        self.thread_pool_executor.submit(self.run_task, task)
        # self.run_task(task)

    def pre_ping(self):
        """
            在agent启动前对server进行探活,如果失败不会进行后续的操作
        """
        ping_ok = transfer_server.ping()
        while not ping_ok:
            ping_ok = transfer_server.ping()
            time.sleep(2)

        self.ping_ok = ping_ok

    def run(self):
        """
            启动定时任务进行心跳发送,任务获取和任务执行
        """
        
        self.pre_ping()

        scheduler = BlockingScheduler()
        scheduler.add_job(self.ping, "interval", seconds=10)
        scheduler.add_job(self.fetch_task, "interval", seconds=10)

        # Thread(target=self.ping).start()
        # Thread(target=self.fetch_task).start()
        Thread(target=self.handle_task).start()
        Thread(target=self.sync_task).start()

        scheduler.start()


        while not self.exit:
            time.sleep(5)


    def cancel_task(self, task_id: str):
        task = self.process_task.get(task_id)
        if task:
            task.cancel()
            del self.process_task[task_id]
