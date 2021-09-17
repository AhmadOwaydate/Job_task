
import json


def get_cordinates(var):
    """get coordinates from the json file"""
    var2 = var["response"]

    var3 = var2["GeoObjectCollection"]

    var4 = var3["featureMember"]
    if var4 == []:
        # the address
        return []
    var5 = var4[1]["GeoObject"]["Point"]["pos"]
    var6 = json.dumps(var5)
    # remove the paranthesis added due to dumps method
    var6 = var6[1:-1]
    cord = var6.split(" ")
    x1 = float(cord[0])
    y1 = float(cord[1])
    return [x1, y1]
