# Bitget Trading Bot

Bot de trading automatizado que ejecuta operaciones en Bitget basado en señales recibidas a través de un canal de Telegram.

## Características

- Integración con la API de Bitget para trading de futuros
- Conexión con Telegram para recibir señales de trading
- Manejo automático de posiciones (apertura y cierre)
- Gestión de riesgo basada en porcentaje del balance
- Soporte para apalancamiento configurable

## Requisitos Previos

- Python 3.7+
- Cuenta en Bitget
- Cuenta de Telegram
- API Key de Bitget con permisos de trading

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd Bitget
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
Crear un archivo `.env` con las siguientes variables:
```env
# Telegram Credentials
export TELEGRAM_API_ID=<tu-api-id>
export TELEGRAM_API_HASH=<tu-api-hash>
export TELEGRAM_PHONE_NUMER=<tu-numero-telefono>
export TELEGRAM_CHANNEL_ID=<id-del-canal>

# Bitget API Credentials
export BG_API_KEY=<tu-api-key>
export BG_SECRET_KEY=<tu-secret-key>
export BG_PASSPHRASE=<tu-passphrase>
```

## Configuración

En el archivo `main.py` puedes ajustar los siguientes parámetros:

- `risk_percent`: Porcentaje del balance a arriesgar en cada operación
- `leverage`: Apalancamiento a utilizar
- `use_risk_percent`: Habilitar/deshabilitar el uso de porcentaje de riesgo

## Uso

1. Asegúrate de tener las variables de entorno configuradas:
```bash
source .env
```

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

## Advertencia

El trading de criptomonedas con apalancamiento conlleva un alto riesgo. Este bot es una herramienta experimental y no garantiza ganancias. Úsalo bajo tu propio riesgo.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## Licencia

[MIT License](LICENSE)