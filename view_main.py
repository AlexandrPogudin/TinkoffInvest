import portfolio
from datetime import *

def get_view_main():
    print("view_main start: ", datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    maininfo = portfolio.MainInfo()

    data_main = [
        {
            # Стоимость портфеля
            "range": "Main!B4",
            "majorDimension": "ROWS",
            "values": [[maininfo["total_amount_portfolio"]]],
        },
        {
            # Доходность
            "range": "Main!E4",
            "majorDimension": "ROWS",
            "values": [["=" + maininfo["expected_yield"] + "/100"]],
        },
        {
            # Валюта
            "range": "Main!H4",
            "majorDimension": "ROWS",
            "values": [[maininfo["total_amount_currencies"]]],
        },
        {
            # Стоимость акций
            "range": "Main!B8",
            "majorDimension": "ROWS",
            "values": [[maininfo["total_amount_shares"]]],
        },
        {
            # Стоимость облигаций
            "range": "Main!E8",
            "majorDimension": "ROWS",
            "values": [[maininfo["total_amount_bonds"]]],
        },
        {
            # Стоимость фондов
            "range": "Main!H8",
            "majorDimension": "ROWS",
            "values": [[maininfo["total_amount_etf"]]],
        },
    ]

    print("view_main finish: ", datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    return data_main
