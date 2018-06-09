import urllib.request
import json  
from io import StringIO
import csv
from datetime import datetime

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
    return result['Draws']

def update_result_file():
    missing_results = get_result(1046, 1060)
    missing_results.reverse()
    with open('resource/test.csv', 'a', newline='') as csvfile:
        result_file = csv.writer(csvfile, delimiter=',')
        for result in missing_results:
            draw_date = datetime.strptime(result['DrawDate'], '%Y-%m-%dT%H:%M:%S')
            result_file.writerow([result['DrawNumber'], draw_date.strftime('%Y%m%d')]+result['PrimaryNumbers']+result['SecondaryNumbers'])
    csvfile.close()

def update_ozlotto_latest_result():
    missing_results = []
    part_results = get_result(1046, 1095)
    missing_results.extend(part_results)
    part_results = get_result(1096, 1145)
    missing_results.extend(part_results)
    part_results = get_result(1146, 1195)
    missing_results.extend(part_results)
    part_results = get_result(1196, 1245)
    missing_results.extend(part_results)
    part_results = get_result(1246, 1269)
    missing_results.extend(part_results)

    missing_results.sort(key = lambda result: result['DrawNumber'])
    print(len(missing_results))
    with open('resource/Ozlotto-latest.csv', 'a', newline='') as csvfile:
        result_file = csv.writer(csvfile, delimiter=',')
        for result in missing_results:
            draw_date = datetime.strptime(result['DrawDate'], '%Y-%m-%dT%H:%M:%S')
            result_file.writerow([result['DrawNumber'], draw_date.strftime('%Y%m%d')]+result['PrimaryNumbers']+result['SecondaryNumbers'])
    csvfile.close()   

if __name__ == '__main__':
    update_ozlotto_latest_result()