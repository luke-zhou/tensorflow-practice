from datetime import datetime


def test():
    columns = ['draw_number', 'date',
               'date-year', 'date-month', 'date-day']
    for i in range(10, 0, -1):
        for j in range(1, 8):
            columns.append('num'+str(j)+'-'+str(i))
        columns.append('sup1'+'-'+str(i))
        columns.append('sup2'+'-'+str(i))
    columns.append('result')
    print(columns)


if __name__ == '__main__':
    test()
