# sitting_detector
circuitpython sitting detector using the feather s2 and capacitive touch

Runs on the [FeatherS2](https://feathers2.io/)
Requires the following [circuitpython libraries](https://circuitpython.org/libraries) (available in the bundle):
- adafruit_requests
- adafruit_minimqtt
- adafruit_dotstar

This code uses the feathers2 library that comes pre-installed on the feathers2 to turn on its LDO2. You could probably
remove that to work on other boards with capacitive touch capabilities.
