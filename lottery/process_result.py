import json
import csv

def main():
    with open('resource/oz-latest-predict-result.json', 'r') as f:
        result = json.load(f)
    f.close

    with open('resource/oz-latest-predict-result.csv', 'w') as f:
        csv_writer = csv.writer(f, delimiter=',')
        csv_writer.writerow(['num', 'label', 'accurate'])
        for key in result:
            csv_writer.writerow([key, result[key]['label'], result[key]['accurate']])
    f.close

if __name__=='__main__':
    main()