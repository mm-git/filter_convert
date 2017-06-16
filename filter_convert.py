import numpy as np
import json

grid = np.fromfile("altfilter.bin", dtype='uint8')
area = {
    "NE": "",
    "NW": "",
    "SE": "",
    "SW": ""
}


def exist(lng, lat, x, y):
    grid_x = (lng + 180) * 3 + x
    grid_y = (lat + 90) * 3 + y

    byte = grid_x / 8
    bit = 1 << (grid_x % 8)
    return grid[grid_y * 135 + byte] & bit != 0


def base64(value):
    b64 = ""
    while value != 0:
        bit6 = value & 0x3f
        value >>= 6
        encode = chr(bit6 + 0x3f)
        b64 += encode
    while len(b64)<4:
        b64 += "="
    return b64


def add_area(lng, lat, grid_pattern):
    if lng<0:
        if lat<0:
            lng = -lng
            lat = -lat
            a = "SW"
        else:
            lng = -lng
            a = "NW"
    else:
        if lat<0:
            lat = - lat
            a = "SE"
        else:
            a = "NE"
    lng_lat_b64 = base64((lat<<17) + (lng<<9) + grid_pattern)
    coordinate =  lng_lat_b64
    area[a] += coordinate

for lat in xrange(0, 180):
    print(lat)
    for lng in xrange(0, 360):
        grid_pattern = 0
        for y in xrange(0,3):
            for x in xrange(0,3):
                if exist(lng-180, lat-90, x, y):
                    bit = 1 << (y*3+x)
                    grid_pattern |= bit
        if grid_pattern > 0:
            add_area(lng-180, lat-90, grid_pattern)


output = open("altfilter.json", "w")
area_json = json.dumps(area)
output.write(area_json)
output.close()
