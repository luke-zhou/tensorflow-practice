import urllib.request
import json  
from io import StringIO

def get_result(min_draw, max_draw):
    post_body = {'MinDrawNo': min_draw, 'MaxDrawNo': max_draw, 'Product': "OzLotto", 'CompanyFilter': ["Tattersalls"]}

    api_url = "https://api.thelott.com/sales/vmax/web/data/lotto/results/search/drawrange"
    req = urllib.request.Request(api_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    json_data = json.dumps(post_body)
    json_data_bytes = json_data.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(json_data_bytes))
    print(json_data_bytes)
    response = urllib.request.urlopen(req, json_data_bytes)
    result = json.load(StringIO(response.read().decode("utf-8")))
    print(len(result['Draws']))

    for draw in result['Draws']:
        print(draw)

if __name__ == '__main__':
    get_result(1199, 1200)