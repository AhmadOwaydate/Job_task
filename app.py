# Manage http requests
import requests
# Manage logging functions
import logging

# Import flask dependencies
from flask import Flask, request,  render_template

# Importing middleware functions
from middleware.check_if_in_mkad import check_if_in_mkad
from middleware.get_distance import get_distance_to_mscow_ring
from middleware.get_cordinates import get_cordinates
# ................
app = Flask(__name__)


# Set the log level and specify the .log file
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# ....


@app.route("/pageOne", methods=['POST', 'GET'])
# This fuction is executed in case a http request reached this route
def index():
    try:
        # Run in case  of post request
        if request.method == "POST":
            address = request.form['address']
            # sending an http request to Yandex Geocoder API  url using inputted address
            response = requests.get(
                url="https://geocode-maps.yandex.ru/1.x/?"
                + "apikey=c97769fc-875c-4678-8139-08b6e7400a8e"
                + "&format=json"
                + "&geocode="
                + address)
            # if there is a response
            if response.ok:
                # decoding response
                response = response.json()

                coordinates = get_cordinates(response)
                # if there is no coordinates to return inform the user
                # that the address does'nt exist
                if coordinates == []:
                    return render_template("index.html",
                                           greeting=f"the {address} doesnt exist.")

                # Check if the coordinates exist in the database
                if check_if_in_mkad(coordinates[0], coordinates[1]):
                    # Add info to log file as debug
                    logging.debug(f"{address} already in the MKAD data")
                    return render_template("index.html",
                                           greeting=f"{address} already in the MKAD data try another")

                else:
                    # Calling a function to do as it's name implies
                    distance = get_distance_to_mscow_ring(
                        coordinates[0], coordinates[1])
                    logging.debug(
                        f"the distance between {address} and "
                        + f"mosco ring is {distance} miles")
                    # Render index.html page with args greeting as a specified value
                    return render_template("index.html",
                                           greeting=f"the distance between {address} and"
                                           + f" mosco ring is {distance} miles")
            else:
                # Run if there is no response from the server
                return render_template("index.html",
                                       greeting="There was no response from the server")
        # Run in case of GET request
        else:
            # Render from_test.html page from templates folder
            return render_template("form_test.html")
    # catch requests errors and execute the code
    except requests.exceptions.RequestException as e:
        return render_template("index.html",
                               greeting="Sorry cant reach the server right now")


if __name__ == "__main__":
    # Launch the Flask server
    app.run(port=5000, host="0.0.0.0")
