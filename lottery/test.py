from datetime import datetime


def test():
    draw_data = [[1261, 20180417, 43, 20, 7, 27, 36, 11, 23, 18, 26],
                 [1262, 20180424, 7, 45, 39, 4, 16, 27, 29, 40, 24],
                 [1263, 20180501, 15, 11, 9, 19, 27, 8, 36, 5, 29],
                 [1264, 20180508, 41, 45, 27, 31, 29, 9, 43, 16, 6],
                 [1265, 20180515, 41, 3, 12, 13, 6, 40, 29, 4, 39],
                 [1266, 20180522, 2, 13, 39, 45, 19, 12, 31, 24, 41],
                 [1267, 20180529, 13, 21, 44, 1, 8, 12, 9, 38, 10],
                 [1268, 20180605, 11, 30, 45, 18, 33, 37, 23, 6, 3],
                 [1269, 20180612, 22, 2, 31, 38, 12, 7, 45, 11, 29],
                 [1270, 20180619, 20, 18, 26, 35, 10, 22, 16, 25, 34]]
    predict_feature = {
        'draw_number': [1271],
        'date': [20180625],
    }
    draw_datetime = datetime.strptime(
        str(predict_feature['date'][0]), '%Y%m%d')
    draw_date = draw_datetime.date()
    predict_feature['date-year'] = [draw_date.year]
    predict_feature['date-month'] = [draw_date.month]
    predict_feature['date-day'] = [draw_date.day]
    for i in range(0, len(draw_data)):
        for j in range(1, 8):
            predict_feature['num'+str(j)+'-'+str(10-i)] = [draw_data[i][j+1]]
        for j in range(1, 3):
            predict_feature['sup'+str(j)+'-'+str(10-i)] = [draw_data[i][j+8]]

    print(predict_feature)


if __name__ == '__main__':
    test()
