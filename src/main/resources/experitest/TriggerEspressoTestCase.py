#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import requests
import org.slf4j.LoggerFactory as LoggerFactory
import base64
import json
#
logger = LoggerFactory.getLogger("Experitest")
#
# # New Experitest logic
# # setup the request url
# api_endpoint = "/api/v1/test-run/execute-test-run-async"
# url = server.get('url') + "%s" % api_endpoint
#
# logger.error(url)
#
# usrPass = server.get('username') + ":" + server.get('password')
#
# headers = {
#     'Content-Type' : "application/json",
#     'Authorization' : 'Basic %s' % base64.b64encode(usrPass)
# }
#
# logger.error("Header Object loaded correctly with input parameters.")
# logger.error(json.dumps(headers))
#
# if deviceQueries == 'android':
#     deviceQuery = '@os=\'android\''
# else:
#     deviceQuery = '@os=\'ios\''
#
# payload = {
#     'executionType': 'espresso',
#     'runningType': runningType,
#     'deviceQueries': deviceQuery
# }
#
# logger.error("Payload Object loaded correctly with input parameters.")
# logger.error(json.dumps(payload))
#
# files = [
#     ('app', open(app,'rb')),
#     ('testApp', open(testApp,'rb'))
# ]
#
# #logger.error("Files Object loaded correctly with input parameters.")
# # logger.error(files)
#
# # send POST request to /api/v1/test-run/execute-test-run-async endpoint
# r = requests.post(url, headers=headers, data=payload, files=files, verify=False)
#
# # check for good response
# if r.status_code != 200:
#     raise Exception(
#         "Error executing Espresso Test Case. Please check input parameters."
#     )
#     # logger.error(r.errorDump())
# else:
#     output = r.text

# url = "https://uscloud.experitest.com/api/v1/test-run/execute-test-run-async"

# New Experitest logic
# setup the request url
api_endpoint = "/api/v1/test-run/execute-test-run-async"
url = server.get('url') + "%s" % api_endpoint

if deviceQueries == 'android':
    deviceQuery = '@os=\'android\''
else:
    deviceQuery = '@os=\'ios\''

payload = {
    'executionType': 'espresso',
    'runningType': runningType,
    'deviceQueries': deviceQuery
}

# Referencing .apk files for Application (app) and Unit Tests (testApp)
files = [
    ('app', open(app,'rb')),
    ('testApp', open(testApp,'rb'))
]

usrPass = username + ":" + password

headers = {
    'Authorization' : 'Basic %s' % base64.b64encode(usrPass)
}

logger.error("Header Object loaded correctly with input parameters.")
logger.error(json.dumps(headers))

logger.error("Payload Object loaded correctly with input parameters.")
logger.error(json.dumps(payload))

response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

if response.status_code != 200:
    raise Exception("Error executing Espresso Test Case. Please check input parameters.")
else:
    output = response.text