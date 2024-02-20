# Подключаем библиотеки
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import view_main
import view_portfolio
import view_operation
from datetime import *

CREDENTIALS_FILE = (
    ".\credentials.json"  # Имя файла с закрытым ключом, вы должны подставить свое
)

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
)

httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
service = apiclient.discovery.build(
    "sheets", "v4", http=httpAuth
)  # Выбираем работу с таблицами и 4 версию API

# Создание таблицы
"""
spreadsheet = service.spreadsheets().create(body = {
    'properties': {'title': 'Портфель Tinkoff', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Main',
                               'gridProperties': {'rowCount': 200, 'columnCount': 30}}}]
}).execute()
"""

spreadsheetId = ("")  # сохраняем идентификатор файла

"""
driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'your mail'},  # Открываем доступ на редактирование
    fields = 'id'
).execute()
"""

data_full = (
    view_main.get_view_main() + view_portfolio.get_view_portfolio() + view_operation.get_view_operations()
)
results = (
    service.spreadsheets()
    .values()
    .batchUpdate(
        spreadsheetId=spreadsheetId,
        body={
            "valueInputOption": "USER_ENTERED",  # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": data_full,
        },
    )
    .execute()
)

print("https://docs.google.com/spreadsheets/d/" + spreadsheetId)
