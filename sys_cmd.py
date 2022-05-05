import logging
import subprocess

logger = logging.getLogger(__name__)


def sys_command_executor(cmd, timeout, capture_output):
    """
    Why use PIPE: to read err msg from stdout && stderr
    """
    logger.info("util.sys_command_executor", extra={
        "cmd": cmd,
        "timeout": timeout,
        "capture_output": capture_output
    })
    stdout = subprocess.DEVNULL
    stderr = subprocess.DEVNULL
    if capture_output:
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
    res = subprocess.run(cmd, stdout=stdout, stderr=stderr, timeout=timeout, shell=True)
    res.stdout = res.stdout.decode('utf-8') if res.stdout else ''
    res.stderr = res.stderr.decode('utf-8') if res.stderr else ''
    return res.returncode, res.stdout, res.stderr
