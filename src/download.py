from time import sleep

from bs4 import BeautifulSoup

from src.config import Config


def get_post(session, csrftoken, config: Config, time, types: str, second: bool = False) -> None | str:

    data = dict(csrfmiddlewaretoken=csrftoken, service_type='mg', month='', course_type='', class_type='', is_valid='',
                rate_plan='', is_manual='', export_type='', status='', pack='', pack_settings='all', utm_source='',
                utm_campaign='', utm_medium='', utm_content='', date_from=time['start'], date_due=time['stop'],
                export_mode='default', product_date_from='', product_date_due='', purchase_period='')

    if types == 'mastergroup':
        data['types'] = config.MG_SETTING
        data['service_type'] = 'mg'
    else:
        data['types'] = config.COURSE_SETTING
        data['service_type'] = 'course'

    result_request = session.post(
        'https://umschool.net/predbannik/massload/export-purchases/',
        headers={
            'referer': 'https://umschool.net/predbannik/massload/export-purchases/',
            'user-agent': 'umschool_app',
        },
        data=data)

    if 'Упс... Что-то пошло не так' in result_request.text:
        if second:
            raise Exception('Ошибка в data запроса')
        else:
            return get_post(session=session, csrftoken=csrftoken, config=config, time=time, types=types)

    soup = BeautifulSoup(result_request.text, 'html.parser')
    return soup.find('tbody').find('tr').find('td').string


def check_result(session, numb_request, numb_page: int = 1, number_of_repetitions: int = 0) -> str:
    result_request_get = session.get(f'https://umschool.net/predbannik/massload/export-purchases/?page={numb_page}',
                                     headers={
                                         'referer': 'https://umschool.net/predbannik/massload/export-purchases/',
                                         'user-agent': 'umschool_app',
                                     })

    soup1 = BeautifulSoup(result_request_get.text, 'html.parser')
    raw_request_sheet = soup1.find('tbody').find_all('tr')

    request_sheet = []
    for raw_request in raw_request_sheet:
        result = {'number': str(raw_request).split('<td>')[1].split('</td>')[0],
                  'name': str(raw_request).split('<br/><b>')[1].split('</b><br/>')[0]}
        try:
            res = str(raw_request).split('href="')[1].split('">')[0]
        except IndexError:
            res = None
        result['link'] = res
        request_sheet.append(result)

    for results in request_sheet:
        if numb_request == results['number']:
            if results['link'] is not None:
                return results['link']
            else:
                sleep(60)
                number_of_repetitions += 1
                if number_of_repetitions >= 120:
                    raise Exception('За 2 часа не удалось скачать файл')
                else:
                    return check_result(session, numb_request, numb_page, number_of_repetitions)
    return check_result(session, numb_request, numb_page + 1, number_of_repetitions)
