import time


def retry(func, attempts=3, wait=1):
    """Call func, and if it fails try again a couple more times."""
    for i in range(attempts):
        try:
            return func()
        except Exception as e:
            if i == attempts - 1:
                raise
            print(f"attempt {i + 1} failed: {e}, retrying in {wait}s")
            time.sleep(wait)
            wait = wait * 2
