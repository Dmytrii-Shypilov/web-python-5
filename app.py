import asyncio
from aiohttp import ClientSession
from datetime import datetime
import requests

def get_url(period=None):
    if not period:
        period = str(datetime.now().date()).split("-")
        period.reverse()
    api_date_format = (".").join(period)
    base_url = f'https://api.privatbank.ua/p24api/exchange_rates?date={api_date_format}'
    return base_url

def get_currency_info(data, currency=None):
    pass


async def fetch_currencies(session, period=None):
    url = get_url(period)
    async with session.get(url) as response:
        result = await response.text()
        return result
        


def parse_instructions(command):
    args = command.split(" ")
    while len(args) < 3:
        args.append(None)
    return args


async def main():
    async with ClientSession() as session:
        instructions = input("Enter your command >>> ")
        command, date, currency = parse_instructions(instructions) 
        data = await fetch_currencies(session, date)
        get_currency_info(data, currency)
        


if __name__ == "__main__":
    asyncio.run(main())