# Temperature
=============
Demonstration of a web service client and server.

The client directory contains a single python file that communicates with a [Flask](http://flask.pocoo.org/) based (or other) web service running on the localhost, port 5000.

The web service exposes the following endpoints:

 * /convert/fahrenheit/
 * /convert/celsius/
 * /convert/kelvin/
 * /convert/rankine/


Each of the endpoints receives a tempertaure, and returns a JSON object of that temperature 
converted into the other three temperature scales.

A sample invocation and response follows:

curl http://localhost:5000/convert/fahrenheit/212/

```{"kelvin": 373.15000000000003, "rankine": 671.6700000000001, "celsius": 100.0}```
