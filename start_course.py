import datetime

from main import download

if __name__ == '__main__':
    date = datetime.datetime.now()
    # Настроить в зависимость от настроек cron-а
    start_data = (date - datetime.timedelta(hours=1)).strftime('%d.%m.%Y %H')
    stop_data = date.strftime('%d.%m.%Y %H')
    download({
        "start": f"{start_data}:00",
        "stop": f"{stop_data}:00"
    }, 'course')
