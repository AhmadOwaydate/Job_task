
from mkad_coordinates import mkad_km


def check_if_in_mkad(x1, y1):
    """"check if the entered coordinates are in the MKAD table"""
    for i in mkad_km:
        if i[1] == x1 and i[2] == y1:
          # it's already in the mkad data and it has index {i[0]}
            return True
    # These coordinates are not in the database
    return False
