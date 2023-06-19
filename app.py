import asyncio
from aiohttp import ClientSession, ClientConnectionError
from datetime import datetime, timedelta
from prettytable import PrettyTable


def get_currency_info(data, currency):
    print(f"\nCurrency: {currency}")
    table = PrettyTable()
    table.field_names = ["Date", "Sale", "Purchase"]
    for day in data:
        currency_data = list(
            filter(lambda x: x['currency'] == currency, day['exchangeRate']))[0]
        table.add_row([day['date'], currency_data['saleRate'],
                      currency_data['purchaseRate']])

    print(table)


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


async def fetch_currency(session, date):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
    try:
        async with session.get(url) as response:
            if response.status == 200:
                result = await response.json()
                return result
            else:
                print(f"Error status: {response.status} for {url}")
    except ClientConnectionError as err:
        print(f'Connection error: {url}', str(err))


async def fetch_currencies(session, dates):
    tasks = []
    for date in dates:
        task = asyncio.create_task(fetch_currency(session, date))
        tasks.append(task)
    data = await asyncio.gather(*tasks)
    return data


def parse_instructions(command):
    args = command.split(" ")
    if len(args) < 3:
        for i in range(0, 3-len(args)):
            args.append(None)
    if args[1]:
        args[1] = args[1].upper()
    if args[2]:
         args[2] = int(args[2])
    return args


async def main():
    while True:
        async with ClientSession() as session:
            instructions = input("Enter your command >>> ")
            command, currency, period = parse_instructions(instructions)
           
            if currency and currency not in ['USD','EUR','CHF','GBP','PLN']:
                print(f"Currency '{currency}' is not exchangable in PrivatBank")
                continue
            if command == "exchange":
                if not currency and not period or not period:
                    print("Please enter all arguments: 'exchange <currency> <period(days)>'")
                if period and period > 10:
                    print("You can get rates for last 10 days maximum")
                    continue
                if command and currency and period:
                    dates = get_dates_list(period)
                    print("...Fetching data")
                    data = await fetch_currencies(session, dates)
                    get_currency_info(data, currency)
            if command == "close":
                print("See you Later")
                break
            if command not in ["exchange", "close"]:
                print("Please enter a correct command: exchange | close")


if __name__ == "__main__":
    asyncio.run(main())
