from website import *
from dotenv import load_dotenv
load_dotenv()

import threading, os

app = create_app()


if __name__ == '__main__':
    app.run("0.0.0.0", 3273, True)

