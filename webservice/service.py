# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop
import json

class BaseHandler(tornado.web.RequestHandler):
	def set_default_headers(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Access-Control-Allow-Credentials', 'true')
		self.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
		self.set_header('Access-Control-Allow-Headers','Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')

class ConvertKelvinHandler(BaseHandler):
    def get(self,temperature):
        temperature = float(temperature)
        F = float(((9.0/5.0)*(temperature-273.15))+32.0)
        C = float(temperature-273.15)
        R = float(temperature*1.8)

        self.write(json.dumps({"fahrenheit":F,"celsius":C,"rankine":R}))

class ConvertFahrenheitHandler(BaseHandler):
    def get(self,temperature):
        temperature = float(temperature)
        K = float(((temperature-32.0)*(5.0/9.0))+273.15)
        C = float((temperature-32.0)*(5.0/9.0))
        R = float(temperature+459.67)

        self.write(json.dumps({"kelvin":K,"celsius":C,"rankine":R}))

class ConvertRankineHandler(BaseHandler):
    def get(self,temperature):
        temperature = float(temperature)
        F = float(temperature-459.67)
        C = float((temperature/1.8)-273.15)
        K = float(temperature/1.8)

        self.write(json.dumps({"fahrenheit":F,"celsius":C,"kelvin":K}))

class ConvertCelsiusHandler(BaseHandler):
    def get(self,temperature):
        temperature = float(temperature)
        F = float((temperature*(9.0/5.0))+32)
        K = float(temperature+273.15)
        R = float((temperature*1.8)+491.67)

        self.write(json.dumps({"fahrenheit":F,"kelvin":K,"rankine":R}))

def make_app():
    return tornado.web.Application([
        (r"/convert/kelvin/(-?\d+\.?\d+?)/",       ConvertKelvinHandler),
        (r"/convert/fahrenheit/(-?\d+\.?\d+?)/",   ConvertFahrenheitHandler),
        (r"/convert/rankine/(-?\d+\.?\d+?)/",      ConvertRankineHandler),
        (r"/convert/celsius/(-?\d+\.?\d+?)/",      ConvertCelsiusHandler)
    ])

if __name__ == '__main__':
	app = make_app()
	app.listen(5000)
	tornado.ioloop.IOLoop.current().start()