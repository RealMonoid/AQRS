import os
import signal
import sys
from contextlib import suppress
from subprocess import Popen, TimeoutExpired
from threading import Thread

import psutil


def capability(memory_mode: str) -> str | None:
    if memory_mode != "observed_rss":
        return "A strict memory cap is unavailable in this build."
    if sys.platform == "win32":
        try:
            WindowsJob().close()
        except (ImportError, OSError) as error:
            return f"Windows Job Object unavailable ({type(error).__name__})."
    elif sys.platform != "linux":
        return "Worker containment is supported only on Windows and Linux."
    return None


class WindowsJob:
    def __init__(self) -> None:
        import win32job

        self.api = win32job
        from pywintypes import error as WindowsError

        try:
            self.handle = win32job.CreateJobObject(None, "")
        except WindowsError as error:
            raise OSError("Could not create a Windows Job Object.") from error
        try:
            limits = win32job.QueryInformationJobObject(
                self.handle, win32job.JobObjectExtendedLimitInformation
            )
            limits["BasicLimitInformation"]["LimitFlags"] = (
                win32job.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            )
            win32job.SetInformationJobObject(
                self.handle, win32job.JobObjectExtendedLimitInformation, limits
            )
        except WindowsError as error:
            self.close()
            raise OSError("Could not configure a Windows Job Object.") from error

    def attach(self, pid: int) -> None:
        import win32api
        import win32con

        access = win32con.PROCESS_SET_QUOTA | win32con.PROCESS_TERMINATE
        from pywintypes import error as WindowsError

        try:
            process = win32api.OpenProcess(access, False, pid)
            try:
                self.api.AssignProcessToJobObject(self.handle, process)
            finally:
                process.Close()
        except WindowsError as error:
            raise OSError("Could not attach worker to a Windows Job Object.") from error

    def close(self) -> None:
        self.handle.Close()


def stop_tree(process: Popen, job: WindowsJob | None) -> None:
    with suppress(BrokenPipeError):
        process.stdin.close()
    if job is not None:
        job.close()
        try:
            process.wait(timeout=2)
        except TimeoutExpired:
            process.kill()
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        process.wait(timeout=5)
    except TimeoutExpired as error:
        raise OSError(
            "Worker did not exit after containment was terminated."
        ) from error


def arm_parent_loss_guard(stdin_fd: int) -> None:
    if sys.platform == "linux":
        Thread(target=_kill_group_on_parent_loss, args=(stdin_fd,), daemon=True).start()


def _kill_group_on_parent_loss(stdin_fd: int) -> None:
    # The supervisor owns the write end for the full worker lifetime.
    os.read(stdin_fd, 1)
    os.killpg(os.getpgrp(), signal.SIGKILL)


def tree_usage(pid: int) -> tuple[float, float]:
    root = psutil.Process(pid)
    rss = 0
    cpu_seconds = 0.0
    for process in [root, *root.children(recursive=True)]:
        try:
            rss += process.memory_info().rss
        except psutil.NoSuchProcess:
            continue
        with suppress(psutil.Error):
            times = process.cpu_times()
            cpu_seconds += times.user + times.system
    return rss / 1024**2, cpu_seconds
