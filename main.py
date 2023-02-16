from time import sleep
from typing import Dict

import requests as requests

from src.config import Config
from src.download import get_post, check_result


def get_csrftoken(session: requests.Session) -> str:
    response = session.get(
        'https://umschool.net/predbannik/massload/export-purchases/', headers={'user-agent': 'umschool_app'})

    if response.status_code == 200:
        return response.text.split('name="csrfmiddlewaretoken" value="')[1].split('">')[0]
    else:
        sleep(1)
        return get_csrftoken(session)


def get_link(session, csrftoken, config, time, types):
    numb_request_ = get_post(session=session, csrftoken=csrftoken, config=config, time=time, types=types)
    link_ = check_result(session=session, numb_request=numb_request_)
    if link_ is None:
        return get_link(session, csrftoken, config, time, types)
    else:
        return link_


def download(time: Dict[str, str], types: str):
    csrftoken = get_csrftoken(session := requests.Session())
    config = Config()

    result_login = session.post('https://umschool.net/predbannik/login/?next=/predbannik/massload/export-purchases/',
                                headers={'user-agent': 'umschool_app',
                                         'referer': 'https://umschool.net/predbannik/login/' +
                                                    '?next=/predbannik/massload/export-purchases/'},
                                data={
                                    "csrfmiddlewaretoken": csrftoken,
                                    "username": config.ADMIN_LOGIN,
                                    "password": config.ADMIN_PASSWORD,
                                    "next": '/predbannik/massload/export-purchases/'})

    if 'Пожалуйста, введите корректные имя пользователя и пароль учётной записи.' in result_login.text:
        raise Exception("Ошибка авторизации")

    csrftoken = result_login.text.split('name="csrfmiddlewaretoken" value="')[1].split('">')[0]

    link = get_link(session=session, csrftoken=csrftoken, config=config, time=time, types=types)

    filename = f"{time['start']}-{time['stop']}.csv"
    r = requests.get(link, allow_redirects=True)
    with open(f"uploaded_files/{types}/{filename}", 'wb') as file:
        file.write(r.content)
