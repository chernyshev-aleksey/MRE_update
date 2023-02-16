import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.ADMIN_LOGIN = os.getenv('ADMIN_LOGIN')
        self.ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
        self.MG_SETTING = os.getenv('MG_SETTING')
        self.COURSE_SETTING = os.getenv('COURSE_SETTING')
