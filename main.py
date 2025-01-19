import os
from telethon import TelegramClient, events
from datetime import datetime

import bitget.v2.mix.order_api as max_order_api
import bitget.v2.mix.account_api as max_account_api
import bitget.v2.mix.market_api as max_market_api
import bitget.bitget_api as baseApi

# Replace with your credentials
api_id = os.environ.get('TELEGRAM_API_ID')
api_hash = os.environ.get('TELEGRAM_API_HASH')
phone_number = os.environ.get('TELEGRAM_PHONE_NUMER')

# channel_id = -1002239931115
channel_id = int(os.environ.get('TELEGRAM_CHANNEL_ID'))

# Bitget API credentials
api_key = os.environ.get('BG_API_KEY')
secret_key = os.environ.get('BG_SECRET_KEY')
passphrase = os.environ.get('BG_PASSPHRASE')

# Risk parameter in percentage (e.g., 1% of the account balance)
risk_percent = 20
leverage = "20"

# Thread ID del topic específico que quieres monitorear
thread_id = None  # Reemplaza None con el ID del thread que quieres monitorear

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

max_order_api = max_order_api.OrderApi(api_key, secret_key, passphrase)
account_api = max_account_api.AccountApi(api_key, secret_key, passphrase)
market_api = max_market_api.MarketApi(api_key, secret_key, passphrase)


async def main(): 
    # Start the Telegram client session
    await client.start(phone_number)

    # Listen for new messages in the specified group
    @client.on(events.NewMessage(chats=channel_id))
    async def handler(event):
        print('\n------------------------------------')
        print(f'New Message at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        message = event.message.message
        print(message)
        lines = message.splitlines()

        print(lines[0])

        if len(lines) > 1:
            side = lines[2].strip()
            symbol = lines[3].split(": ")[1].split(" ")[0].lower()
            symbol = symbol[:-2] if symbol.endswith(".p") else symbol
            print(side)
            print(symbol)

            try:
                if 'Exit' in side:
                    params = {}
                    params["symbol"] = symbol
                    params["productType"] = "USDT-FUTURES"

                    response = max_order_api.closePositions(params)

                else:
                    # Let set leverage
                    params = {}
                    params["symbol"] = symbol
                    params["productType"] = "USDT-FUTURES"
                    params["marginCoin"] = "USDT"
                    params["leverage"] = leverage

                    response = account_api.setLeverage(params)

                    params = {}
                    params["symbol"] = symbol
                    params["productType"] = "USDT-FUTURES"
                    params["marginCoin"] = "USDT"
            
                    response = account_api.account(params)

                    balance = float(response.get("data").get("crossedMaxAvailable"))

                    # Getting market price
                    params = {}
                    params["symbol"] = symbol
                    params["productType"] = "USDT-FUTURES"
                    response = market_api.market_price(params)

                    # print(response)
                    mark_price = float(response.get("data")[0].get("markPrice"))

                    position_size = ((balance * risk_percent / 100) / mark_price) * float(leverage)

                    params = {}

                    if side == "long":
                        params["side"] = "buy"
                    else:
                        params["side"] = "sell"

                    print('position_size', position_size)
                    params["symbol"] = symbol
                    params["productType"] = "USDT-FUTURES"
                    params["marginMode"] = "crossed"
                    params["marginCoin"] = "USDT"
                    params["orderType"] = "market"
                    params["tradeSide"] = "open"
                    # params["price"] = "27012"
                    params["size"] = position_size
                    print(params)
                    response = max_order_api.placeOrder(params)
                    print(response)

            except Exception as e:
                print("error:" + e.message)

    print("Listening for messages...")
    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
