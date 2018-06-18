from datetime import datetime
def test():

    draw_datetime = datetime.strptime('20180612', '%Y%m%d')
    draw_date = draw_datetime.date()
    print(draw_date.year)
    print(draw_date.month)
    print(draw_date.week)

if __name__ == '__main__':
    test()