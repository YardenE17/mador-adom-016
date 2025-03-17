
def main(host, port, username, password, logger):
    """
    Plugin's main function. Receives arguments as named parameters via kwargs.
    """
    logger.info(f"Starting demo plugin as {username}")
    return f"This is a demo plug in"

def func():
    ...