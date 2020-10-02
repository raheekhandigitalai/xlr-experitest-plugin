#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import time
import json
import org.slf4j.LoggerFactory as LoggerFactory
import base64

logger = LoggerFactory.getLogger("Experitest")

uri = "/reporter/api/testView"

body = json.dumps(
    {
        "name": "RaheeTestView_1.0",
        "byKey": "date",
        "groupByKey1": "device.os",
        "groupByKey2": "device.version",
        "keys": [
            {
                "date"
            }
        ],
        "showInDashboard": False
    }
)

request = HttpRequest(instance)
response = request.post(
    uri,
    body=body,
    contentType="application/json"
)

if response.isSuccessful():
    rawData = json.loads(response.getResponse())
else:
    response.errorDump()
    raise Exception("Unable to get data from Experitest")

data = {
    "rawData": rawData["data"],
    "instance": instance["url"]
}