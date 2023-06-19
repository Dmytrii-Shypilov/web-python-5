import asyncio
from aiohttp import ClientSession
from datetime import datetime, timedelta
import pprint 


def get_currency_info(data, currency):
    for day in data:
        currency_data = list(filter(lambda x: x['currency'] == currency, day['exchangeRate']))[0]
        print(f"Date: {day['date']}, Sale: {currency_data['saleRate']} UAH, Purchase: {currency_data['purchaseRate']} UAH")


def format_date(date):
    formatted_date = str(date.date()).split("-")
    formatted_date.reverse()
    result = (".").join(formatted_date)
    return result


def get_dates_list(period):
    period = int(period)
    dates_list = []
    today = datetime.now()
    dates_list.append(format_date(today))
    if period > 0 and period <= 10:
        for day in range(1, period):
            date = format_date(today - timedelta(day))
            dates_list.append(date)
    return dates_list


async def fetch_currencies(session, dates):
    data = []
    for date in dates:
        url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
        async with session.get(url) as response:
            result = await response.json()
            data.append(result)
    return data

def parse_instructions(command):
    args = command.split(" ")
    return args


async def main():
    async with ClientSession() as session:
        instructions = input("Enter your command >>> ")
        command, currency, period = parse_instructions(instructions)
        if command == "exchange":
            dates = get_dates_list(period)
            print("...Fetching data")
            data = await fetch_currencies(session, dates)
            get_currency_info(data, currency)
       


if __name__ == "__main__":
    asyncio.run(main())
   
