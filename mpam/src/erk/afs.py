from __future__ import annotations

from _collections import deque
from threading import Thread, RLock
from typing import Final, Optional

from erk.basic import Callback


class _AFS_Thread(Thread):
    """
    The thread used by :class:`AsyncFunctionSerializer`.
    """
    serializer: Final[AsyncFunctionSerializer]  #: The associated :class:`AsyncFunctionSerializer`
    before_task: Final[Optional[Callback]]      #: A callback called before every task
    after_task: Final[Optional[Callback]]       #: A callback called after every task
    on_empty_queue: Final[Optional[Callback]]   #: A callback called after the last task
    queue: Final[deque[Callback]]               #: The queue of callbacks.

    def __init__(self,
                 serializer: AsyncFunctionSerializer,
                 first_callback: Callback,
                 *,
                 name: Optional[str]=None,
                 daemon: bool=False,
                 before_task: Optional[Callback]=None,
                 after_task: Optional[Callback]=None,
                 on_empty_queue: Optional[Callback]=None
                 ) -> None:
        """
        Initialize the thread

        Args:
            serializer: the associated :class:`AsyncFunctionSerializer`
            first_callback: the first callback to process
            name: an optional name of the thread
        Keyword Args:
            daemon: whether or not the thread is a daemon
            before_task: A callback to call before every task
            after_task: A callback to call after every task
            on_empty_queue: A callback to call after the last task
        """
        super().__init__(name=name, daemon=daemon)
        self.serializer = serializer
        self.before_task = before_task
        self.after_task = after_task
        self.on_empty_queue = on_empty_queue
        self.queue = deque[Callback]((first_callback,))

    def run(self) -> None:
        """
        Process the callbacks in the :attr:`queue`.  Before each, call
        :attr:`before_task`. After each, call :attr:`after_task`.  When the
        queue is empty, call :attr:`on_empty` and remove ourself from our
        :attr:`serializer`

        Note:
            :attr:`on_empty` will be called with :attr:`serializer`'s lock
            locked.
        """
        queue = self.queue
        before_task = self.before_task
        after_task = self.after_task
        # logger.debug(f'queue len:{len(queue)}|before_task:{before_task}|after_task:{after_task}')
        with self.serializer.lock:
            func: Callback = queue.popleft()
        while True:
            if before_task is not None:
                before_task()
            # logger.debug(f'func:{func.__qualname__}')
            func()
            if after_task is not None:
                after_task()
            with self.serializer.lock:
                if len(queue) == 0:
                    # There's nothing left to do, and since we hold the lock, nothing will be added,
                    # so we can just get rid of ourself.
                    self.serializer.thread = None
                    on_empty = self.on_empty_queue
                    if on_empty is not None:
                        on_empty()
                    return
                else:
                    func = queue.popleft()

    def enqueue(self, fn: Callback) -> None:
        """
        Add an item to the :attr:`queue`

        Note:
            This method assumes that :attr:`serializer`'s
            :attr:`~AsyncFunctionSeraializer.lock` is locked.

        Args:
            fn: the callback function
        """
        # This is only called by the serializer while its lock is locked.
        self.queue.append(fn)


class AsyncFunctionSerializer:
    """
    Calls functions in a background thread.  Functions are added by means of
    :func:`enqueue` and are called sequentially.

    The :class:`AsyncFunctionSerializer` can specify actions to be performed
    around the enqueued functions:

    * :attr:`before_task`: called before each function

    * :attr:`after_task`: called after each function

    * :attr:`on_nonempty_queue`: called when the queue goes from being empty to
      being nonempty

    * :attr:`on_empty_queue`: called when the queue goes from being nonempty to
      being empty

    Note that it is legal for these actions to call :func:`enqueue`.

    The background thread is only created when the queue becomes non-empty, and
    it goes away when the queue becomes empty.

    By default, the background thread is not a daemon thread, and so the process
    will not die as long as there are items in the queue.  This can be altered
    by specifying ``daemon=True`` when the :class:`AsyncFunctionSerializer` is
    initialized.
    """

    thread: Optional[_AFS_Thread] = None        #: The background :class`.Thread`
    lock: Final[RLock]                          #: A local lock

    thread_name: Final[Optional[str]]           #: The name of the :class:`.Thread`
    daemon_thread: Final[bool]                  #: Is the :class:`.Thread` a daemon?
    before_task: Final[Optional[Callback]]      #: An optional callback called before each function
    after_task: Final[Optional[Callback]]       #: An optional callback called after each function
    on_empty_queue: Final[Optional[Callback]]   #: An optional callback called when queue becomes empty
    on_nonempty_queue: Final[Optional[Callback]] #: An optional callback called when queue becomes nonempty

    def __init__(self, *,
                 thread_name: Optional[str]=None,
                 daemon_thread: bool=False,
                 before_task: Optional[Callback]=None,
                 after_task: Optional[Callback]=None,
                 on_empty_queue: Optional[Callback]=None,
                 on_nonempty_queue: Optional[Callback]=None
                 ) -> None:
        """
        Initialize the object.

        Keyword Args:
            thread_name: the name of the thread
            daemon_thread: is the thread a daemon?
            before_task: an optional callback called before each function
            after_task: an optional callback called after each function
            on_empty_queue: an optional callback called when the queue becomes empty
            on_nonempty_queue: an optional callback called when the queue becomes nonempty
        """
        self.lock = RLock()
        self.thread_name = thread_name
        self.daemon_thread = daemon_thread
        self.before_task = before_task
        self.after_task = after_task
        self.on_empty_queue = on_empty_queue
        self.on_nonempty_queue = on_nonempty_queue

    def enqueue(self, fn: Callback) -> None:
        """
        Enqueue a function to be called in the background thread.

        Args:
            fn: the function to be enqueued.
        """
        with self.lock:
            thread = self.thread
            if thread is None:
                thread = _AFS_Thread(self, fn,
                                     name=self.thread_name,
                                     daemon=self.daemon_thread,
                                     before_task=self.before_task,
                                     after_task=self.after_task,
                                     on_empty_queue = self.on_empty_queue)
                self.thread = thread
                if self.on_nonempty_queue is not None:
                    self.on_nonempty_queue()
                thread.start()
            else:
                thread.enqueue(fn)
