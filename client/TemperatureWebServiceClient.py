#!/usr/bin/python
'''
    Filename:
        TemperatureWebServiceClient.py

    Description:
        Client of the temperature conversion web service on localhost
'''
import csv
import json
from contextlib import closing
from httplib import CannotSendRequest, HTTPConnection
from _socket import error
from urllib import quote
from urllib2 import URLError

def getConnection():
    '''
    Connect to the temperature conversion web service on the localhost, port 5000
    @return: An HTTP connection object for use in communciation with the web service
    '''
    return HTTPConnection('localhost', 5000)

def webserviceResult(conn, wsEndpoint, temperature):
    '''
    Handle the communication with the webservice by specifying the endpoint, and
    reading the web service response
    @param conn: An HTTP connection object to the web service endpoint
    @param wsEndpoint: The web service endpoint the user chooses to execute
    @param temperature: The temperature to pass to the web service for conversion
    @return: Response from the web service as a json object on success, Exception
    on error
    '''
    try:
        conn.putrequest('GET', '%s%s/' % (wsEndpoint, quote(temperature)))
        conn.endheaders()
        resp = conn.getresponse()
        if resp.status == 200:
            data = resp.read()
            return data
        else:
            raise URLError('Invocation of web service failed')
    except (error, CannotSendRequest, URLError) as wsError:
        raise wsError

def endpoint(temperatureScale):
    '''
    Determine which web service endpoint the user's input is, for conversion
    to the other three temperature scales
    @param temperatureScale: string representation of the temperature scale of
    the user input.
    @return: The web service endpoint that will perform the temperature conversion
    '''
    if temperatureScale.upper()[0] == 'K':
        return '/convert/kelvin/'
    elif temperatureScale.upper()[0] == 'F':
        return '/convert/fahrenheit/'
    elif temperatureScale.upper()[0] == 'R':
        return '/convert/rankine/'
    elif temperatureScale.upper()[0] == 'C':
        return '/convert/celsius/'
    raise URLError('Unknown conversion scale')

def displayTemps(temperatureScale, jsonString):
    '''
    Convert the json object response from the web service to a formatted
    string.
    @param temperatureScale: string representing the scale we passed in to the
    web service. Necessary to help us determine which of the optional fields
    in the json object we need to unpack
    @param jsonString: Binary response from web service that will be
    converted to a json object 
    @return: A formatted string for display on standard output
    '''
    temps = json.loads(jsonString)
    if temperatureScale.upper()[0] == 'K':
        return '%.2f\t\t-\t\t%.2f\t\t%.2f' % (temps['fahrenheit'], temps['celsius'], 
                                                  temps['rankine'],)
    elif temperatureScale.upper()[0] == 'F':
        return '\t-\t\t%.2f\t\t%.2f\t\t%.2f' % (temps['kelvin'], temps['celsius'],
                                                  temps['rankine'])
    elif temperatureScale.upper()[0] == 'R':
        return '%.2f\t\t%.2f\t\t%.2f\t\t-' % (temps['fahrenheit'], temps['kelvin'],
                                                  temps['celsius'])
    elif temperatureScale.upper()[0] == 'C':
        return '%.2f\t\t%.2f\t\t-\t\t%.2f' % (temps['fahrenheit'], temps['kelvin'],
                                                  temps['rankine'])

def readDataFile():
    '''
    Generator that returns a tuple with the temperature scale as the first element
    and the tempearture as the second element
    '''
    try:
        with open('testfile.csv') as fPtr:
            reader = csv.reader(fPtr)
            for line in reader:
                yield line
    except IOError, ioError:
        raise ioError

def main():
    '''
    Read the test data, and trigger the web service computation that will convert
    the specified temperature and scale to the other three temperature scales.
    '''
    print 'Input\t\tFahrenheit\tKelvin\t\tCelsius\t\tRankine\r\n',
    try:
        for scale, degrees in readDataFile():
            with closing(getConnection()) as connection:
                try:
                    print "%-12s %s" % (degrees, displayTemps(scale,
                                            webserviceResult(connection,
                                                            endpoint(scale),
                                                            degrees)))
                except URLError:
                    print degrees, '\t\tX\t\tX\t\tX\t\tX'
    except IOError:
        print 'Missing or corrupt test data file'

if __name__ == '__main__':
    main()
