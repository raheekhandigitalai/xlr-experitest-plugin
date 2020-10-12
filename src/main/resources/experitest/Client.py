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
import json
import base64
import org.slf4j.LoggerFactory as LoggerFactory

logger = LoggerFactory.getLogger("Experitest")


def triggerEspressoTest(serverParams, deviceQueries, runningType, app, testApp, username, password):
    # setup the request url
    api_endpoint = "/api/v1/test-run/execute-test-run-async"
    url = serverParams.get('url') + "%s" % api_endpoint

    deviceQuery = setDeviceQuery(deviceQueries)

    payload = {
        'executionType': 'espresso',
        'runningType': runningType,
        'deviceQueries': deviceQuery
    }

    # Referencing .apk files for Application (app) and Unit Tests (testApp)
    files = setFileDefinitions(app, testApp)

    usrPass = username + ":" + password
    headers = {
        'Authorization': 'Basic %s' % base64.b64encode(usrPass)
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

    if response.status_code != 200:
        raise Exception("Error executing Espresso Test Case. Please check input parameters.")
    else:
        espressoTestRunId = getTestRunId(response.content)
        return response.text, espressoTestRunId


def triggerXCUITest(serverParams, deviceQueries, runningType, app, testApp, username, password):
    # setup the request url
    api_endpoint = "/api/v1/test-run/execute-test-run-async"
    url = serverParams.get('url') + "%s" % api_endpoint

    deviceQuery = setDeviceQuery(deviceQueries)

    payload = {
        'executionType': 'xcuitest',
        'runningType': runningType,
        'deviceQueries': deviceQuery
    }

    # Referencing .ipa files for Application (app) and Unit Tests (testApp)
    files = setFileDefinitions(app, testApp)

    usrPass = username + ":" + password
    headers = {
        'Authorization': 'Basic %s' % base64.b64encode(usrPass)
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

    if response.status_code != 200:
        raise Exception("Error executing XCUI Test Case. Please check input parameters.")
    else:
        xcuiTestRunId = getTestRunId(response.content)
        return response.text, xcuiTestRunId

def getTestRunStatusEspresso(serverParams, username, password):
    # setup the request url
    api_endpoint = "/api/v1/test-run/" + espressoTestRunId + "/status"
    url = serverParams.get('url') + "%s" % api_endpoint

    usrPass = username + ":" + password

    headers = {
        'Authorization': 'Basic %s' % base64.b64encode(usrPass)
    }

    response = requests.request("GET", url, headers=headers, verify=False)

    if response.status_code != 200:
        raise Exception("Error executing Test Run Status API for Espresso. Please check input parameters.")
    else:
        return response.text

def getTestRunStatusXCUITest(serverParams, username, password):
    # setup the request url
    api_endpoint = "/api/v1/test-run/" + xcuiTestRunId + "/status"
    url = serverParams.get('url') + "%s" % api_endpoint

    usrPass = username + ":" + password

    headers = {
        'Authorization': 'Basic %s' % base64.b64encode(usrPass)
    }

    response = requests.request("GET", url, headers=headers, verify=False)

    if response.status_code != 200:
        raise Exception("Error executing Test Run Status API for XCUITest. Please check input parameters.")
    else:
        return response.text

def setDeviceQuery(deviceQueries):
    if deviceQueries == 'android':
        deviceQuery = '@os=\'android\''
    else:
        deviceQuery = '@os=\'ios\''

    return deviceQuery


def setFileDefinitions(app, testApp):
    files = [
        ('app', open(app, 'rb')),
        ('testApp', open(testApp, 'rb'))
    ]

    return files


def getTestRunId(responseContent):
    testRunId = ""
    data = json.loads(responseContent)

    for key in data:
        if key == "data":
            for subKey in data['data']:
                if subKey == "Test Run Id":
                    testRunId = data['data']['Test Run Id']
                    break
            break

    return testRunId
