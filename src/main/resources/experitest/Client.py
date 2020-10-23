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
import time
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

def getTestRunStatusAndResultForUnitTests(serverParams, testRunId, username, password):
    # setup the request url
    api_endpoint = "/api/v1/test-run/%s/status" % testRunId
    url = serverParams.get('url') + "%s" % api_endpoint

    usrPass = username + ":" + password

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Accept': 'application/json;charset=UTF-8',
        'Accept-Encoding': 'deflate',
        'Authorization': 'Basic %s' % base64.b64encode(usrPass)
    }

    response = requests.request("GET", url, headers=headers, verify=False)

    testRunStatus = getTestRunStatus(response.content)

    while testRunStatus != "Finished" and "Running":
        time.sleep(20)
        response = requests.request("GET", url, headers=headers, verify=False)
        testRunStatus = getTestRunStatus(response.content)

    if response.status_code != 200:
        raise Exception("Error executing Test Run Status API for Espresso. Please check input parameters.")
    else:
        totalNumberOfTests = getTotalNumberOfTests(response.content)
        passedCount = passed(response.content)
        failedCount = failed(response.content)
        skippedCount = skipped(response.content)
        ignoredCount = ignored(response.content)
        reporterLinkUrl = reporterLink(response.content)
        return testRunStatus, totalNumberOfTests, passedCount, failedCount, skippedCount, ignoredCount, reporterLinkUrl

def uploadBuildToSeeTestCloud(serverParams, filePath, uniqueName, projectName, username, password):
    # setup the request url
    api_endpoint = "/api/v1/applications/new"
    url = serverParams.get('url') + "%s" % api_endpoint

    payload = {
        'camera': True,
        'touchId': True,
        'uniqueName': uniqueName,
    }

    files = [
        ('file', open(filePath,'rb'))
    ]

    usrPass = username + ":" + password

    headers = {
        'Authorization': 'Basic %s' % base64.b64encode(usrPass),
        'projectName': projectName
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)

    if response.status_code != 200:
        raise Exception("Error executing Test Run Status API for XCUITest. Please check input parameters.")
    else:
        return response.text

# Untested - Exploratory phase
def createTestView(serverParams, testViewName, username, password):
    # setup the request url
    api_endpoint = "/reporter/api/testView"
    url = serverParams.get('url') + "%s" % api_endpoint

    logger.error(url)

    payload = {
        'name': testViewName,
        'byKey': 'date',
        'groupByKey1': 'device.os',
        'groupByKey2': 'device.version',
        'showInDashboard': False,
        'viewBy': 'data'
    }

    usrPass = username + ":" + password

    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'deflate',
        'Connection': 'keep-alive',
        'Authorization': 'Basic %s' % base64.b64encode(usrPass)
    }

    logger.error("Before the call")
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    logger.error("After the call")

    if response.status_code != 200:
        raise Exception("Error creating a Test View. Please check input parameters.")
    else:
        testViewId = getTestViewId(response.content)
        return response.text, testViewId

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

def getTestRunStatus(responseContent):
    testRunStatus = ""
    data = json.loads(responseContent)

    for key in data:
        if key == "data":
            for subKey in data['data']:
                if subKey == "Test Run State":
                    testRunStatus = data['data']['Test Run State']
                    break
            break

    return testRunStatus

def getTotalNumberOfTests(responseContent):
    totalNumberOfTests = ""
    data = json.loads(responseContent)

    for key in data:
        if key == "data":
            for subKey in data['data']:
                if subKey == "Total number of tests":
                    totalNumberOfTests = data['data']['Total number of tests']
                    break
            break

    return totalNumberOfTests

def passed(responseContent):
    passedCount = ""
    data = json.loads(responseContent)

    for key in data:
        if key == "data":
            for subKey in data['data']:
                if subKey == "Number of passed tests":
                    passedCount = data['data']['Number of passed tests']
                    break
            break

    return passedCount

def failed(responseContent):
    failedCount = ""
    data = json.loads(responseContent)

    for key in data:
        if key == "data":
            for subKey in data['data']:
                if subKey == "Number of failed tests":
                    failedCount = data['data']['Number of failed tests']
                    break
            break

    return failedCount

def skipped(responseContent):
    skippedCount = ""
    data = json.loads(responseContent)

    for key in data:
        if key == "data":
            for subKey in data['data']:
                if subKey == "Number of skipped tests":
                    skippedCount = data['data']['Number of skipped tests']
                    break
            break

    return skippedCount

def ignored(responseContent):
    ignoredCount = ""
    data = json.loads(responseContent)

    for key in data:
        if key == "data":
            for subKey in data['data']:
                if subKey == "Number of ignored tests":
                    ignoredCount = data['data']['Number of ignored tests']
                    break
            break

    return ignoredCount

def reporterLink(responseContent):
    reporterLinkUrl = ""
    data = json.loads(responseContent)

    for key in data:
        if key == "data":
            for subKey in data['data']:
                if subKey == "Link to Reporter":
                    reporterLinkUrl = data['data']['Link to Reporter']
                    break
            break

    return reporterLinkUrl

# Untested - Exploratory phase
def getTestViewId(responseContent):
    testViewId = ""
    data = json.loads(responseContent)

    for key in data:
        if key == "id":
            testViewId = data['id']
        break

    return testViewId
