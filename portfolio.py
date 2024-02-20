from tinkoff.invest import Client, InstrumentIdType, OperationState
from datetime import *
from decimal import Decimal
from time import sleep

TOKEN = "your_token"
id = "your_id"


def MoneyType(value):
    result = f"{getattr(value, 'units')},{abs(Decimal(getattr(value, 'nano')//10000))}"
    return result

def ExpectedYieldType(value):
    result = f"{getattr(value, 'units')},{Decimal(getattr(value, 'nano')//10000)}"
    return result

def QuotationType(value):
    result = f"{getattr(value, 'units')},"
    return result

def DateTimeType(value):
    result = value.strftime("%d.%m.%Y %H:%M")
    return result


def MainInfo():
    with Client(TOKEN) as client:
        response = client.operations.get_portfolio(account_id=id)
        result_main = {
            "total_amount_shares": MoneyType(getattr(response, "total_amount_shares")),
            "total_amount_bonds": MoneyType(getattr(response, "total_amount_bonds")),
            "total_amount_etf": MoneyType(getattr(response, "total_amount_etf")),
            "total_amount_currencies": MoneyType(
                getattr(response, "total_amount_currencies")
            ),
            "expected_yield": ExpectedYieldType(getattr(response, "expected_yield")),
            "total_amount_portfolio": MoneyType(
                getattr(response, "total_amount_portfolio")
            ),
        }
    return result_main


def PortfolioInfo():
    with Client(TOKEN) as client:
        response = client.operations.get_portfolio(account_id=id)
        positions = getattr(response, "positions")

        result_shares = []
        result_bonds = []
        result_etf = []

        for position in positions:
            instrument_type = getattr(position, "instrument_type")
            figi = getattr(position, "figi")
            if instrument_type == "share":
                share = client.instruments.share_by(
                    id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi
                )
                info_share = getattr(share, "instrument")
                result_shares.append(
                    [
                        figi,
                        getattr(info_share, "ticker"),
                        getattr(info_share, "name"),
                        QuotationType(getattr(position, "quantity")),
                        MoneyType(getattr(position, "average_position_price")),
                        QuotationType(getattr(position, "expected_yield")),
                        MoneyType(getattr(position, "current_price")),
                        getattr(info_share, "sector"),
                    ]
                )

            elif instrument_type == "bond":
                bond = client.instruments.bond_by(
                    id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi
                )
                info_bond = getattr(bond, "instrument")
                result_bonds.append(
                    [
                        figi,
                        getattr(info_bond, "ticker"),
                        getattr(info_bond, "name"),
                        QuotationType(getattr(position, "quantity")),
                        MoneyType(getattr(position, "average_position_price")),
                        QuotationType(getattr(position, "expected_yield")),
                        MoneyType(getattr(position, "current_price")),
                        getattr(info_bond, "sector"),
                    ]
                )

            elif instrument_type == "etf":
                etf = client.instruments.etf_by(
                    id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi
                )
                info_etf = getattr(etf, "instrument")
                result_etf.append(
                    [
                        figi,
                        getattr(info_etf, "ticker"),
                        getattr(info_etf, "name"),
                        QuotationType(getattr(position, "quantity")),
                        MoneyType(getattr(position, "average_position_price")),
                        QuotationType(getattr(position, "expected_yield")),
                        MoneyType(getattr(position, "current_price")),
                        getattr(info_etf, "sector"),
                    ]
                )

        return result_shares, result_bonds, result_etf


def Operation_state(state):
    if state == OperationState.OPERATION_STATE_UNSPECIFIED:
        return "Статус операции не определён"
    elif state == OperationState.OPERATION_STATE_EXECUTED:
        return "Исполнена"
    elif state == OperationState.OPERATION_STATE_CANCELED:
        return "Отменена"
    elif state == OperationState.OPERATION_STATE_PROGRESS:
        return "Исполняется"


def OperationsInfo():
    with Client(TOKEN) as client:
        response = client.operations.get_operations(
            account_id=id, from_=datetime(2023, 8, 1), to=datetime.now()
        )
        operations = getattr(response, "operations")
        result_operations = []
        for operation in operations:
            figi = getattr(operation, "figi")
            if len(figi) > 0:
                instrument_type = getattr(operation, "instrument_type")
                name = ""
                if instrument_type == "share":
                    share = client.instruments.share_by(
                        id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi
                    )
                    name = getattr(getattr(share, "instrument"), "name")
                elif instrument_type == "bond":
                    bond = client.instruments.bond_by(
                        id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi
                    )
                    name = getattr(getattr(bond, "instrument"), "name")
                elif instrument_type == "etf":
                    etf = client.instruments.etf_by(
                        id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi
                    )
                    name = getattr(getattr(etf, "instrument"), "name")

                result_operations.append(
                    [
                        figi,
                        getattr(operation, "type"),
                        Operation_state(getattr(operation, "state")),
                        name,
                        DateTimeType(getattr(operation, "date")),
                        MoneyType(getattr(operation, "price")),
                        getattr(operation, "quantity"),
                        MoneyType(getattr(operation, "payment")),
                        getattr(operation, "instrument_type"),
                    ]
                )
            else:
                result_operations.append(
                    [
                        "",
                        getattr(operation, "type"),
                        Operation_state(getattr(operation, "state")),
                        '',
                        DateTimeType(getattr(operation, "date")),
                        MoneyType(getattr(operation, "price")),
                        getattr(operation, "quantity"),
                        MoneyType(getattr(operation, "payment")),
                        getattr(operation, "instrument_type"),
                    ]
                )
                sleep(1)

        return result_operations
