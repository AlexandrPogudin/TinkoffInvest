import portfolio
from datetime import *

def get_view_portfolio():
    print("view_portfolio start: ", datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    result_shares, result_bonds, result_etf = portfolio.PortfolioInfo()

    data_portfolio = [
        {
            # Акции
            "range": "Shares!A4:H100",
            "majorDimension": "ROWS",
            "values": result_shares,
        },
        {
            # Облигации
            "range": "Bonds!A4:H100",
            "majorDimension": "ROWS",
            "values": result_bonds,
        },
        {
            # Фонды
            "range": "ETF!A4:H100",
            "majorDimension": "ROWS",
            "values": result_etf,
        },
    ]

    print("view_portfolio finish: ", datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    return data_portfolio
