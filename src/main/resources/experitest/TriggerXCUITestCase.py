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

logger = LoggerFactory.getLogger("Experitest")

# New Experitest logic
# setup the request url
#api_endpoint = "/api/v1/test-run/execute-test-run-async"
api_endpoint = "/reporter/api/projects"
url = server.get('url') + "%s" % api_endpoint

#logger.error(url)

usrPass = server.get('username') + ":" + server.get('password')

headers = {
    'Content-Type' : "application/json",
    'Authorization' : 'Basic %s' % base64.b64encode(usrPass)
}

#logger.error("Header Object loaded correctly with input parameters.")
# logger.error(headers)

# payload = {
#     'executionType': 'espresso',
#     'runningType': runningType,
#     # 'app': app,
#     # 'testApp': testApp,
#     'deviceQueries': deviceQueries
# }

#logger.error("Payload Object loaded correctly with input parameters.")
# logger.error(payload)

# files = [
#     ('app', open(app,'rb')),
#     ('testApp', open(testApp,'rb'))
# ]

#logger.error("Files Object loaded correctly with input parameters.")
# logger.error(files)

# send POST request to /api/v1/test-run/execute-test-run-async endpoint
#r = requests.post(url, headers=headers, data=payload, files=files, verify=False)
r = requests.get(url, headers=headers, verify=False)

# logger.error(url)
# logger.error(r.request.body)
# logger.error(r.request.headers)

# logger.error(r.errorDump())
# logger.error(rawData["data"]);

# check for good response
if r.status_code != 200:
    raise Exception(
        "Error executing Espresso Test Case. Please check input parameters."
    )
else:
    output = r.text

# import requests
# url = "https://uscloud.experitest.com/api/v1/test-run/execute-test-run-async"
# payload = {'executionType': 'espresso',
#            'runningType': 'fastFeedback',
#            'deviceQueries': '@os=\'android\''}
# files = [
#     ('app', open('/C:/Users/Rahee/Desktop/Clients/medidata/Archive/app-local-debug.apk','rb')),
#     ('testApp', open('/C:/Users/Rahee/Desktop/Clients/medidata/Archive/app-local-debug-androidTest.apk','rb'))
# ]
# headers = {
#     'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJ4cC51Ijo3MzU0NDMsInhwLnAiOjE2NjA5MDMsInhwLm0iOjE1Nzg2MDM5NTA1MTUsImV4cCI6MTkxMDc5NDYyOCwiaXNzIjoiY29tLmV4cGVyaXRlc3QifQ.CMJSREYHuaHYC3GTDGYO6VN7Osf0Rnq6oX_LHNZjtl4',
#     'Cookie': 'XSRF-TOKEN=2a329ebd-d9b3-42e9-b0db-109552a712bc; JSESSIONID=32DC33D46F72D4B5DF361CD48DC27F5A'
# }
# response = requests.request("POST", url, headers=headers, data = payload, files = files)
# print(response.text.encode('utf8'))
