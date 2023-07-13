import time
from obswebsocket import obsws, requests
obs_client = obsws("localhost", 4455, "951753")
obs_client.connect()

# Start the recording
obs_client.call(requests.StartRecord())
time.sleep(1)
obs_client.call(requests.StopRecord())