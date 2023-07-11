from telescope_planner.client.app import App
from telescope_planner.client.service import Service

SERVER_NAME = "127.0.0.1"
SERVER_PORT = "8000"
ROOT_PATH = "../.."
SERVICE = Service(SERVER_NAME, SERVER_PORT, ROOT_PATH)
APP = App(SERVICE)

APP.run()
