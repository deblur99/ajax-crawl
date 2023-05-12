import pytz
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def get_soup_from_URL(URL: str):
    res = requests.get(URL)
    return BeautifulSoup(res.text, 'html.parser')


def find_events(soup: BeautifulSoup):
    timezone = pytz.timezone('Asia/Seoul')
    now = datetime.now(timezone)
    semester = -1

    semester1_list = [3, 4, 5, 6, 7, 8]
    semester2_list = [9, 10, 11, 12, 1, 2]

    if now.month in semester1_list:
        semester = 1
    elif now.month in semester2_list:
        semester = 2

    results = soup.select('div.row-fluid > div.span8')[1:]
    rows = {}

    for idx, result in enumerate(results):
        row = []
        items = result.select('div.desc > ul > li')

        for item in items:
            items = {}
            items['date'] = item.find('span').text.replace(' ', '').split('~')

            date_str = ''

            for date in items['date']:
                date = date.split('.')
                month, day = int(date[1]), int(date[2])
                if len(date_str) > 0:
                    date_str += '\n~ ' + f'{month}월 {day}일'
                else:
                    date_str = f'{month}월 {day}일'

            items['date'] = date_str
            items['content'] = item.find('a').text.lstrip(' ').rstrip(' ')

            row.append(items)

        match semester:
            case 1:
                rows[semester1_list[idx]] = row

            case 2:
                rows[semester2_list[idx]] = row

    return rows


# https://www.dankook.ac.kr/web/kor/-2014-?p_p_id=Event_WAR_eventportlet
# &p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2
# &p_p_col_pos=1&p_p_col_count=3&_Event_WAR_eventportlet_action=view
#
# https://www.dankook.ac.kr/web/kor/-2014-?p_p_id=Event_WAR_eventportlet
# &p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2
# &p_p_col_pos=1&p_p_col_count=3&_Event_WAR_eventportlet_action=view

def main():
    URL = "https://www.dankook.ac.kr/web/kor/-2014-?p_p_id=Event_WAR_eventportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-2&p_p_col_pos=1&p_p_col_count=3&_Event_WAR_eventportlet_action=view"
    soup = get_soup_from_URL(URL)
    find_events(soup)


main()
