import os
from telethon import TelegramClient, events
from datetime import datetime
from dotenv import load_dotenv

import bitget.v2.mix.order_api as max_order_api
import bitget.v2.mix.account_api as max_account_api
import bitget.v2.mix.market_api as max_market_api
import bitget.bitget_api as baseApi

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone_number = os.getenv('TELEGRAM_PHONE_NUMER')
channel_id = int(os.getenv('TELEGRAM_CHANNEL_ID'))

# Bitget API credentials
api_key = os.getenv('BG_API_KEY')
secret_key = os.getenv('BG_SECRET_KEY')
passphrase = os.getenv('BG_PASSPHRASE')

# Trading parameters
risk_percent = float(os.getenv('RISK_PERCENT', 20))  # Default to 20 if not set
leverage = os.getenv('LEVERAGE', 20)  # Default to 20 if not set
sl_percent = float(os.getenv('SL_PERCENT', 0.75))

client = TelegramClient('session_name', api_id, api_hash)

max_order_api = max_order_api.OrderApi(api_key, secret_key, passphrase)
account_api = max_account_api.AccountApi(api_key, secret_key, passphrase)
market_api = max_market_api.MarketApi(api_key, secret_key, passphrase)


async def main():
    await client.start(phone_number)

    can_operate = True
    
    @client.on(events.NewMessage(chats=channel_id))
    async def handler(event):
        try:
            nonlocal can_operate

            # Verificar si el mensaje es del topic específico
            is_bot = True
            if hasattr(event.message, 'reply_to') and event.message.reply_to:
                is_bot = False
            
            if not is_bot:
                print(f"Ignorando mensaje de otro topic")
                return

            print('\n------------------------------------')
            print(f'Nuevo mensaje recibido a las {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
            message = event.message.message
            print("Contenido del mensaje:")
            print(message)
            
            lines = message.splitlines()
            
            if len(lines) > 1:
                side = lines[2].strip()
                symbol = lines[3].split(": ")[1].split(" ")[0].lower()
                symbol = symbol[:-2] if symbol.endswith(".p") else symbol
                print(f"Side: {side}")
                print(f"Symbol: {symbol}")

                try:
                    if 'Exit' in side:
                        params = {}
                        params["symbol"] = symbol
                        params["productType"] = "USDT-FUTURES"
                        print("\nCerrando posición...")
                        can_operate = True
                        response = max_order_api.closePositions(params)

                    else:

                        if can_operate:
                            position_side = "buy" if side == "long" else "sell"
                            # Configurar apalancamiento
                            params = {}
                            params["symbol"] = symbol
                            params["productType"] = "USDT-FUTURES"
                            params["marginCoin"] = "USDT"
                            params["leverage"] = leverage

                            print("\nConfigurando apalancamiento...")
                            response = account_api.setLeverage(params)
                            print("Respuesta de apalancamiento:", response)

                            # Obtener información de la cuenta
                            params = {}
                            params["symbol"] = symbol
                            params["productType"] = "USDT-FUTURES"
                            params["marginCoin"] = "USDT"
                    
                            print("\nObteniendo balance disponible...")
                            response = account_api.account(params)
                            balance = float(response.get("data").get("crossedMaxAvailable"))
                            print(f"Balance disponible: {balance} USDT")

                            # Obtener precio de mercado
                            params = {}
                            params["symbol"] = symbol
                            params["productType"] = "USDT-FUTURES"
                            
                            print("\nObteniendo precio de mercado...")
                            response = market_api.market_price(params)
                            mark_price = float(response.get("data")[0].get("markPrice"))
                            print(f"Precio de mercado: {mark_price}")

                            # Calcular tamaño de la posición
                            position_size = ((balance * risk_percent / 100) / mark_price) * float(leverage)

                            sl_distance = mark_price * (sl_percent/100)
                            
                            stop_loss_price = mark_price - sl_distance if position_side == "buy" else mark_price + sl_distance

                            print("\nObteniendo multiplier...")
                            params = {}
                            params["symbol"] = symbol
                            params["productType"] = "USDT-FUTURES"
                            response = market_api.contracts(params)
                            multiplier = float(response.get("data")[0].get("sizeMultiplier"))

                            stop_loss_price = round(stop_loss_price / multiplier) * multiplier

                            # Preparar orden
                            params = {}
                            params["side"] = position_side
                            params["symbol"] = symbol
                            params["productType"] = "USDT-FUTURES"
                            params["marginMode"] = "crossed"
                            params["marginCoin"] = "USDT"
                            params["orderType"] = "market"
                            params["tradeSide"] = "open"
                            params["size"] = position_size
                            params["presetStopLossPrice"] = str(stop_loss_price)

                            print("\nPreparando orden:")
                            print(f"Tamaño de la posición: {position_size}")
                            print("Parámetros de la orden:", params)
                            
                            response = max_order_api.placeOrder(params)
                            print("Respuesta de la orden:", response)

                            can_operate = False
                        else:
                            print('Ya hay operación abierta')

                except Exception as e:
                    print(f"\nError en la operación: {str(e)}")

        except Exception as e:
            print(f"\nError procesando el mensaje: {str(e)}")

    print("\nBot iniciado. Escuchando mensajes...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
