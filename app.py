# importing flask dependencies
from flask import Flask, request,  render_template

# library for managing http requests
import requests
# library for managing logging
import logging

# importing middleware functions
from middleware.check_if_in_mkad import check_if_in_mkad
from middleware.get_distance import get_distance_to_mscow_ring
from middleware.get_cordinates import get_cordinates
# ................
app = Flask(__name__)

#app.config['DEBUG'] = True
# setting the log level and the .log file
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# ....


@app.route("/pageOne", methods=['POST', 'GET'])
# index fuction executed in case a http request reached this route
def index():
    try:
        # in case of post request
        if request.method == "POST":
            address = request.form['address']
            # sending an http request to Yandex Geocoder API  url using inputted address
            response = requests.get(
                url="https://geocode-maps.yandex.ru/1.x/?"
                + "apikey=c97769fc-875c-4678-8139-08b6e7400a8e"
                + "&format=json" +
                "&geocode=" + address)
            # if there is a response
            if response.ok:
                # decoding response
                response = response.json()

                coordinates = get_cordinates(response)
                if coordinates == []:
                    return render_template("index.html", greeting=f"the {address} doesnt exist ")
                print(coordinates)

                if check_if_in_mkad(coordinates[0], coordinates[1]):
                    # if the coordinates exist in the database
                    # add to log file
                    logging.debug(f"{address} already in the MKAD data")
                    return render_template("index.html", greeting=f"{address} already in the MKAD data try another")
                else:
                    # calling a function to do as it's name implies
                    distance = get_distance_to_mscow_ring(
                        coordinates[0], coordinates[1])
                    logging.debug(
                        f"the distance between {address} and mosco ring is {distance}")
                    # render index.html page with args greeting as a specified value
                    return render_template("index.html", greeting=f"the distance between {address} and mosco ring is {distance}")
            else:
                # in case  there is no response from the server
                return render_template("index.html", greeting="There was ni\o response from the server")
        # in case of GET request
        else:
            # render from_test.html page from templates folder
            return render_template("form_test.html")
    except:
        # if something went wrong
        return render_template("index.html", greeting="Sorry cant reach the serverr right now")


if __name__ == "__main__":
    # Launch the Flask server
    app.run()
