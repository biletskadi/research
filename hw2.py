import mapbox
import json

geocoder = mapbox.Geocoder(access_token='sk.eyJ1IjoiZGlhbmthbG9sNCIsImEiOiJjazhzdjE4c3QwMnlwM2Rud2EwZzg1b29iIn0.OqtyNqmiJI5q6UbWQC6oCQ')
response = geocoder.forward('Paris, France')
with open('text.json', 'w', encoding='UTF-8') as f:
    json.dump(response.json(), f)

from mapbox import Directions
resp = Directions('mapbox.driving').directions([origin, destination])
driving_routes = resp.geojson()
first_route = driving_routes['features'][0]