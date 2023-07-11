from __future__ import annotations

from queue import Queue, Empty
from threading import Thread
import time
import random
from typing import Callable, TypeVar, Any, Generic, Final, Optional
from quantities.dimensions import Time
from quantities.SI import seconds
from quantities.timestamp import Timestamp, time_now, time_since
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')

class Worker(Thread, Generic[T]):
    queue: Queue[T]
    worker_pool: WorkerPool[T]
    last_started_task_tick: int
    should_terminate: bool
    task_handler: Callable[[T], Any]
    idle: bool

    def __init__(self, queue: Queue[T], worker_pool: WorkerPool[T]) -> None:
        super().__init__()
        self.queue = queue
        self.worker_pool = worker_pool
        self.last_started_task_tick = self.worker_pool.tick
        self.should_terminate = False
        self.task_handler = worker_pool.task_handler
        self.idle = True
        logger.info(f"Started {self}")

    def run(self) -> None:
        task_handler = self.task_handler
        queue = self.queue
        pool = self.worker_pool
        timeout = pool.worker_polling_interval.as_number(seconds)
        while not self.should_terminate:
            try:
                task = queue.get(timeout=timeout)
                self.idle = False
                self.last_started_task_tick = pool.tick
                task_handler(task)
                self.idle = True
                queue.task_done()
            except Empty:
                pass
            
    def request_shutdown(self) -> None:
        self.should_terminate = True
        logger.info(f"Shutting down {self}")


class WorkerPool(Generic[T]):
    tick: int
    monitor_polling_interval: Final[Time]
    worker_polling_interval: Final[Time]
    monitor_thread: Final[Thread]
    task_handler: Callable[[T], Any]
    min_workers: Final[int]
    max_workers: Final[Optional[int]]
    max_up_to_date_workers: Final[Optional[int]]
    min_worker_lifetime: Final[Time]
    min_worker_creation_interval: Final[Time]
    running: bool = True

    def __init__(self, *,
                 task_handler: Callable[[T], Any],
                 min_workers: int = 1,
                 max_workers: Optional[int] = None, 
                 monitor_polling_interval: Time,
                 worker_polling_interval: Time, 
                 max_up_to_date_workers: Optional[int] = None,
                 min_worker_lifetime: Time = Time.ZERO,
                 min_worker_creation_interval: Time = Time.ZERO, 
                 ) -> None:
        self.queue: Final[Queue[T]] = Queue()
        self.monitor_polling_interval = monitor_polling_interval
        self.worker_polling_interval = worker_polling_interval
        self.tick = 0
        self.task_handler = task_handler
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.max_up_to_date_workers = max_up_to_date_workers
        self.min_worker_lifetime = min_worker_lifetime
        self.min_worker_creation_interval = min_worker_creation_interval
        self.workers: Final[list[Worker[T]]] = [Worker(self.queue, self) for _ in range(min_workers)]

        self.monitor_thread = Thread(target=self.monitor)
        self.monitor_thread.setDaemon(True)

    def start(self) -> None:
        for worker in self.workers:
            worker.start()

        self.monitor_thread.start()
        
    def shutdown(self) -> None:
        self.running = False
        for worker in self.workers:
            worker.request_shutdown()

    def add_task(self, task: T) -> None:
        self.queue.put(task)

    def monitor(self) -> None:
        timeout = self.monitor_polling_interval.as_number(seconds)
        max_up_to_date = self.max_up_to_date_workers
        last_removed: Timestamp = time_now()
        last_added: Timestamp = time_now()
        min_worker_lifetime = self.min_worker_lifetime
        min_worker_creation_interval = self.min_worker_creation_interval
        workers = self.workers
        min_workers = self.min_workers
        max_workers = self.max_workers
        
        while self.running:
            time.sleep(timeout)

            # up_to_date_workers are those that are idle or got their most recent task since the last time we looked.
            current_tick = self.tick
            def up_to_date(worker: Worker[T]) -> bool:
                return worker.idle or worker.last_started_task_tick == current_tick
            up_to_date_workers = [worker for worker in workers if up_to_date(worker)]
            n_workers = len(workers)
            n_up_to_date = len(up_to_date_workers)
            
            self.tick += 1
            
            if (n_workers > min_workers
                    and max_up_to_date is not None 
                    and n_up_to_date > max_up_to_date
                    and time_since(last_removed) > min_worker_lifetime):
                worker_to_terminate = random.choice(up_to_date_workers)
                worker_to_terminate.request_shutdown()
                workers.remove(worker_to_terminate)
                last_removed = time_now()
            elif (n_up_to_date == 0 
                  and max_workers is not None 
                  and n_workers < max_workers
                  and time_since(last_added) > min_worker_creation_interval):
                new_worker = Worker(self.queue, self)
                self.workers.append(new_worker)
                new_worker.start()
                last_added = time_now()
