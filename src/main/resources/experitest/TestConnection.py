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
api_endpoint = "/reporter/api/projects"
url = configuration.url + "%s" % api_endpoint

# Username and password based on UI input
usrPass = configuration.username + ":" + configuration.password

headers = {
    'Content-Type' : "application/json",
    'Authorization' : 'Basic %s' % base64.b64encode(usrPass)
}

# send GET  request to /reporter/api/projects endpoint
r = requests.get(url, headers=headers, verify=False)

# logger.error(r.content)
# logger.error(r.json())
# logger.error(r.iter_content())
# logger.error(r.reason)
# logger.error(r.status_code)
# logger.error(r.message)
# logger.error(r.data)
# logger.error(r.text)

# check for good response
if r.status_code != 200:
    raise Exception(
        "Error retrieving authorization token from Experitest Server. Please check username and password."
        # . Reason: %s" % r.status
    )
else:
    logger.error('Experitest return object: %s' % r.text)