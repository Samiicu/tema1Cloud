import cgi
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests



class RestHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        pagina_web = open("firstpage.html", "r")
        jsonD = json.dumps(pagina_web.read())
        self.wfile.write(json.loads(jsonD).encode())

        if self.path.find("myip") != -1:
            url = "http://bot.whatismyipaddress.com/"
            response = requests.get(url=url)
            text_to_html="<br><br>Ip-ul meu este:<br>"+response.content.decode()
            self.wfile.write(text_to_html.encode())

        if self.path.find("mygeolocation") != -1:
            url = "http://bot.whatismyipaddress.com/"
            response = requests.get(url=url)
            # print(response.content.decode())
            param = {"ip": response.content.decode()}
            url = "https://ipvigilante.com/"
            response = requests.get(url=url, params=param)
            resp = {}
            resp = json.loads(response.content)
            print(resp["data"]["city_name"])
            print(resp["data"]["latitude"])
            print(resp["data"]["longitude"])
            text_to_html = "<br><br>Oras:" + resp["data"]["city_name"] + "<br>Geolocalizare:<br>" + resp["data"][
                "latitude"] + ", " + resp["data"]["longitude"] + "<br>"
            self.wfile.write(text_to_html.encode())
            # pagina_web = open("secondpage.html", "r")
            # jsonD = json.dumps(pagina_web.read())
            # self.wfile.write(json.loads(jsonD).encode())

        if self.path.find("mycountry") != -1:
            url = "http://bot.whatismyipaddress.com/"
            response = requests.get(url=url)

            url = "https://api.ip2country.info/ip?" + response.content.decode()



            # self.wfile.write(requests.get(url="https://api.ip2country.info/").content)



            response = requests.get(url=url)
            res = {}
            res = json.loads(response.content)
            text = "<br><br>" + "Tara:<br>" + res["countryName"] + "<br>" + "Country code:<br>" + res[
                "countryCode"] + "<br>"
            print(text)
            self.wfile.write(text.encode())

        if self.path.find("mymeetups") != -1:

            #
            url0 = "http://bot.whatismyipaddress.com/"
            response = requests.get(url=url0)
            url1 = "https://api.ip2country.info/ip?" + response.content.decode()
            response = requests.get(url=url1)
            first_response = {}
            first_response = json.loads(response.content)
            #

            #
            url2 = "https://ipvigilante.com/"
            param = {"format":"json","IP": response.content.decode()}
            response = requests.get(url=url2, params=param)
            second_response = {}
            second_response = json.loads(response.content)
            url = "https://api.meetup.com/2/cities"
            params = {
                "country": str(first_response["countryCode"]).lower(),
                "offset": "0",
                "format": "json",
                "lon": str(second_response["data"]["longitude"]),
                "photo-host": "public",
                "page": "10",
                "radius": "50",
                "lat": str(second_response["data"]["latitude"]),
                "order": "size",
                "desc": "false",
                "sig_id": "275434266",
                "sig": "c88544333071682d9302be3ae07129465ee67064"
            }
            response = requests.get(url=url, params=params)

            last_response = {}
            last_response = json.loads(response.content)
            self.wfile.write(response.content)
            print(last_response.values())
            # self.wfile.write(json.dumps(last_response).encode())
            text=""
            for i in last_response["results"]:
                print(i["zip"])
                text+="<br><br>Zip:"+i["zip"]+"<br>Distanta:"+str(i["distance"])+" km"+"<br> Oras:"+i["city"]+"<br>Numar de mebmri:"+str(i["member_count"])
            self.wfile.write(text.encode())

        return


httpd = HTTPServer(('0.0.0.0', 8000), RestHTTPRequestHandler)
while True:
    httpd.handle_request()
