#!/usr/bin/python
# -*- coding: utf-8 -*-

import handlers
from misc import dp
from aiogram import executor
from database.function import DataBaseFunc

if __name__ == '__main__':
    # DataBaseFunc.drop_all()
    DataBaseFunc.add_main_admin()
    executor.start_polling(dp)
    