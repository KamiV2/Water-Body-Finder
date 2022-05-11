from PIL import Image
import requests
import io

def generate_map(location,zoom, dim):
    dimstr = str(dim*10)
    map_parameters = {
        "apiKey":"-Bg4gLOVWSV0cC0ZUSi4swAktgiMXfpzgr7eRCErgsI",
        "c":location, #pulls latlong from location
        "h":dimstr, #image height
        "w":dimstr, #image width
        "t":"1", #terrain mode (sal)
        "z":zoom, #zoom level
        "nodot":"1", #hides dot in location
        "nocp":"1" #removes text
    }

    maprequest = requests.get('https://image.maps.ls.hereapi.com/mia/1.6/mapview', params = map_parameters)
    image_data = maprequest.content # byte values of the image
    image = Image.open(io.BytesIO(image_data))
    filename = "map_Europe.png"
    im1 = image.save(filename, format=None)
    return filename

generate_map("60, 60", "3", 100)





