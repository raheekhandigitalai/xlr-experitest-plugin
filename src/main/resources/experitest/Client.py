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
# import urllib
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
        espressoTestRunId = getJSONValueFromResponseContent('Test Run Id', response.content)
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
        xcuiTestRunId = getJSONValueFromResponseContent('Test Run Id', response.content)
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

    testRunStatus = getJSONValueFromResponseContent('Test Run State', response.content)

    while testRunStatus != "Finished" and "Running":
        time.sleep(20)
        response = requests.request("GET", url, headers=headers, verify=False)
        testRunStatus = getJSONValueFromResponseContent('Test Run State', response.content)

    if response.status_code != 200:
        raise Exception("Error executing Test Run Status API for Espresso. Please check input parameters.")
    else:
        totalNumberOfTests = getJSONValueFromResponseContent('Total number of tests', response.content)
        passedCount = getJSONValueFromResponseContent('Number of passed tests', response.content)
        failedCount = getJSONValueFromResponseContent('Number of failed tests', response.content)
        skippedCount = getJSONValueFromResponseContent('Number of skipped tests', response.content)
        ignoredCount = getJSONValueFromResponseContent('Number of ignored tests', response.content)
        reporterLinkUrl = getJSONValueFromResponseContent('Link to Reporter', response.content)

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

def createTestView(serverParams, testViewName, username, password):
    # setup the request url
    api_endpoint = "/reporter/api/testView"
    url = serverParams.get('url') + "%s" % api_endpoint

    payload = json.dumps(
        {
            'name': testViewName,
            'byKey': 'date',
            'groupByKey1': 'device.os',
            'groupByKey2': 'device.version',
            'showInDashboard': False,
            'viewBy': 'data'
        }
    )

    usrPass = username + ":" + password

    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'deflate',
        'Authorization': 'Basic %s' % base64.b64encode(usrPass)
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    if response.status_code != 200:
        raise Exception("Error creating a Test View. Please check input parameters.")
    else:
        testViewId = getTestViewId(response.content)
        return response.text, testViewId

def getTestViewResults(serverParams, testViewId, jenkinsBuildNumber, username, password):
    # setup the request url
    logger.error('before the api end point is being called')
    api_endpoint = "/reporter/api/testView/%s/summary" % testViewId
    filter_api_endpoint = api_endpoint + "?filter={\"Jenkins_Build_Number\":\"%s\"}" % jenkinsBuildNumber

    url = serverParams.get('url') + "%s" % filter_api_endpoint

    logger.error('url value is: %s ' % url)

    usrPass = username + ":" + password

    headers = {
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Accept-Encoding': 'deflate',
        'Authorization': 'Basic %s' % base64.b64encode(usrPass)
    }

    logger.error('before call')
    response = requests.request("GET", url, headers=headers, verify=False)
    logger.error('after call')

    if response.status_code != 200:
        logger.error(response.status_code)
        raise Exception("Error executing Test Run Status API for Espresso. Please check input parameters.")
    else:
        logger.error(response.text)
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

# This gets the given 'value' based on the response content which is structured as referenced here: https://docs.experitest.com/display/TE/Manage+Test+Run+with+the+API#ManageTestRunwiththeAPI-StatusoftheAPIRun
def getJSONValueFromResponseContent(value, responseContent):
    data = json.loads(responseContent)

    for key in data:
        if key == "data":
            for subKey in data['data']:
                if subKey == "%s" % value:
                    value = data['data']['%s' % value]
                    break
            break

    return value

# Untested - Exploratory phase
def getTestViewId(responseContent):
    testViewId = ""
    data = json.loads(responseContent)

    for key in data:
        if key == "id":
            testViewId = data['id']
        break

    return testViewId