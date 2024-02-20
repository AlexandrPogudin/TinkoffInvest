import portfolio
from datetime import *

def get_view_operations():
    print("view_operations start: ", datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    result_operations = portfolio.OperationsInfo()

    data_operations = [
        {
            # Операции
            "range": "Operations!A4:I500",
            "majorDimension": "ROWS",
            "values": result_operations,
        },
    ]

    print("view_operations finish: ", datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    return data_operations
