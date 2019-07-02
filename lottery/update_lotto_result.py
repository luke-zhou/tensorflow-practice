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

def get_result_p(min_draw, max_draw):
    post_body = {'MinDrawNo': min_draw, 'MaxDrawNo': max_draw, 'Product': "Powerball", 'CompanyFilter': ["Tattersalls"]}

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
    # print(len(result['Draws'][0]['PrimaryNumbers']))
    return result['Draws']

def update_result_file():
    missing_results = get_result_p(1046, 1060)
    missing_results.reverse()
    with open('resource/powerball.csv', 'a', newline='') as csvfile:
        result_file = csv.writer(csvfile, delimiter=',')
        for result in missing_results:
            draw_date = datetime.strptime(result['DrawDate'], '%Y-%m-%dT%H:%M:%S')
            result_file.writerow([result['DrawNumber'], draw_date.strftime('%Y%m%d')]+result['PrimaryNumbers']+result['SecondaryNumbers'])
    csvfile.close()

def update_ozlotto_latest_result(from_draw, to_draw):
    missing_results = get_result(from_draw, to_draw)

    missing_results.sort(key = lambda result: result['DrawNumber'])
    print(len(missing_results))
    with open('resource/Ozlotto-latest.csv', 'a', newline='') as csvfile:
        result_file = csv.writer(csvfile, delimiter=',')
        for result in missing_results:
            draw_date = datetime.strptime(result['DrawDate'], '%Y-%m-%dT%H:%M:%S')

            result_file.writerow([result['DrawNumber'], draw_date.strftime('%Y%m%d')]+result['PrimaryNumbers']+result['SecondaryNumbers'])
    csvfile.close()   

def update_powerball_latest_result():
    missing_results = []
    part_results = get_result_p(877, 895)
    missing_results.extend(part_results)
    part_results = get_result_p(896, 945)
    missing_results.extend(part_results)
    part_results = get_result_p(946, 995)
    missing_results.extend(part_results)
    part_results = get_result_p(996, 1045)
    missing_results.extend(part_results)
    part_results = get_result_p(1046, 1095)
    missing_results.extend(part_results)
    part_results = get_result_p(1096, 1145)
    missing_results.extend(part_results)
    part_results = get_result_p(1146, 1186)
    missing_results.extend(part_results)


    missing_results.sort(key = lambda result: result['DrawNumber'])
    print(len(missing_results))
    with open('resource/powerball.csv', 'a', newline='') as csvfile:
        result_file = csv.writer(csvfile, delimiter=',')
        for result in missing_results:
            draw_date = datetime.strptime(result['DrawDate'], '%Y-%m-%dT%H:%M:%S')

            if len(result['PrimaryNumbers']) == 6:
                primary_number = result['PrimaryNumbers']+['x']
            else:
                primary_number = result['PrimaryNumbers']
            result_file.writerow([result['DrawNumber'], draw_date.strftime('%Y%m%d')]+primary_number+result['SecondaryNumbers'])
    csvfile.close()   

def add_ozlotto_result(draw):
    result = get_result(draw, draw)[0]
    with open('resource/Ozlotto-latest.csv', 'a', newline='') as csvfile:
        result_file = csv.writer(csvfile, delimiter=',')
        draw_date = datetime.strptime(result['DrawDate'], '%Y-%m-%dT%H:%M:%S')

        result_file.writerow([result['DrawNumber'], draw_date.strftime('%Y%m%d')]+result['PrimaryNumbers']+result['SecondaryNumbers'])
    csvfile.close() 

if __name__ == '__main__':
    update_ozlotto_latest_result(1313, 1325)