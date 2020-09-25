#!/usr/bin/python
# -*- coding: utf-8 -*-

# import os
# os.remove('database//database.db')

from database.function import DataBaseFunc
from aiogram import executor
from misc import dp
import handlers


if __name__ == '__main__':
    DataBaseFunc.initial_course_in_db()
    # DataBaseFunc.add_main_admin()
    executor.start_polling(dp)