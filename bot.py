#!/usr/bin/python
# -*- coding: utf-8 -*-

import handlers
from misc import dp
from aiogram import executor

from database.function import DataBaseFunc

if __name__ == '__main__':
    DataBaseFunc.drop_all()
    DataBaseFunc.generate_course()
    DataBaseFunc.add_my_contact()
    DataBaseFunc.add_main_admin()
    # DataBaseFunc.add_admin_eduard()
    # DataBaseFunc.add_second_test_acc()
    DataBaseFunc.add_course_in_me()
    executor.start_polling(dp)
