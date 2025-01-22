# Bitget Trading Bot

Bot de trading automatizado que ejecuta operaciones en Bitget basado en señales recibidas a través de un canal de Telegram.

## Características

- Integración con la API de Bitget para trading de futuros
- Conexión con Telegram para recibir señales de trading
- Manejo automático de posiciones (apertura y cierre)
- Gestión de riesgo basada en porcentaje del balance
- Soporte para apalancamiento configurable

## Requisitos Previos

- Python 3.10+
- Cuenta en Bitget
- Cuenta de Telegram
- API Key de Bitget con permisos de trading

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/rmblockcode/telegram_signals_bot_bitget.git
cd telegram_signals_bot_bitget
```

2. Crear y activar entorno virtual:
```bash
# En Windows
python -m venv venv
.\venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Variables de Entorno

El proyecto utiliza python-dotenv para manejar las variables de entorno. Crea un archivo `.env` en la raíz del proyecto con el siguiente formato:

```bash
# Telegram credentials
TELEGRAM_API_ID=<tu-api-id>
TELEGRAM_API_HASH=<tu-api-hash>
TELEGRAM_PHONE_NUMER=<tu-numero-telefono>
TELEGRAM_CHANNEL_ID=<id-del-canal>

# Bitget API credentials
BG_API_KEY=<tu-api-key>
BG_SECRET_KEY=<tu-secret-key>
BG_PASSPHRASE=<tu-passphrase>

# Trading parameters
RISK_PERCENT=20  # Porcentaje de riesgo por operación (default: 20)
LEVERAGE=20      # Apalancamiento a utilizar (default: 20)
SL_PERCENT=0.75  # Porcentaje de distancia para el SL
```

Las variables se cargarán automáticamente al ejecutar el script.

## Configuración

En el archivo `main.py` puedes ajustar los siguientes parámetros:

- `risk_percent`: Porcentaje del balance a arriesgar en cada operación
- `leverage`: Apalancamiento a utilizar
- `use_risk_percent`: Habilitar/deshabilitar el uso de porcentaje de riesgo

## Uso

1. Asegúrate de tener las variables de entorno configuradas.

2. Ejecutar el bot:
```bash
python main.py
```

## Formato de Señales

El bot espera señales en el siguiente formato:
```
SEÑAL EXCLUSIVA PARA EL EXCHANGE:
🏦 BITGET 🏦
 long
🪙 Symbol: SOLUSDT.P 🪙
🚀 Posicion: long 🚀
💵 Precio: 282.787 💵
⏰ Temporalidad: 3 MIN⏰
```

Para cerrar posiciones:
```
SEÑAL EXCLUSIVA PARA EL EXCHANGE:
🏦 BITGET 🏦
 Trail Exit long
🪙 Symbol: SOLUSDT.P 🪙
🚀 Posicion: flat 🚀
💵 Precio: 283.300 💵
⏰ Temporalidad: 3 MIN⏰
```

## Características de Seguridad

- Manejo de errores para operaciones fallidas
- Validación de parámetros antes de ejecutar órdenes
- Uso de variables de entorno para credenciales sensibles

## Demostración

### Video de YouTube (TODO)
[![Demo en YouTube](https://img.youtube.com/vi/ID_DEL_VIDEO/0.jpg)](https://www.youtube.com/watch?v=ID_DEL_VIDEO)


## Advertencia

El trading de criptomonedas con apalancamiento conlleva un alto riesgo. Este bot es una herramienta experimental y no garantiza ganancias. Úsalo bajo tu propio riesgo.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## Licencia

[MIT License](LICENSE)
