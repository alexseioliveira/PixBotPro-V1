import logging
import sqlite3
import time
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext

# CONFIGURAÇÕES DO BOT:
BOT_TOKEN = '7894687678:AAGrp4b_zY44BcC1ldOpCwxRi4me3Zikfa4'
PUSHINPAY_TOKEN = '34902|FqMRbMDl0hWCXmiRDvNVYRSZOioT5TR1WOoTn6Owc152f119'
GROUP_ID = -1002201363601  # ID do seu grupo

# Iniciar banco de dados SQLite
conn = sqlite3.connect('assinantes.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS assinantes (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    data_expiracao INTEGER
)
''')
conn.commit()

# Iniciar logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bem-vindo ao PixBot Pro!\nEscolha seu plano:\n\n"
                                    "7 dias - R$ 9,99\n"
                                    "30 dias - R$ 19,99\n"
                                    "90 dias - R$ 29,99\n"
                                    "Vitalício - R$ 49,99\n\n"
                                    "Digite: /comprar")

# Comando /comprar
async def comprar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Para comprar, escolha um dos planos e me envie o valor. (9.99, 19.99, 29.99 ou 49.99)")

# Receber o valor enviado
async def receber_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        valor = float(update.message.text.replace(",", "."))
        if valor not in [9.99, 19.99, 29.99, 49.99]:
            await update.message.reply_text("Valor inválido. Envie o valor correto do plano.")
            return
        
        # Cria cobrança no PushinPay
        payload = {
            "value": valor,
            "key": PUSHINPAY_TOKEN,
            "name": f"Assinatura PixBot Pro - {valor}",
            "expire": 3600  # expira em 1 hora
        }
        response = requests.post("https://api.pushinpay.com/api/v1/charge", json=payload)
        data = response.json()

        if data.get('status') == 'success':
            qr_code_link = data['pix']['qrcode_url']
            await update.message.reply_text(f"Realize o pagamento via Pix no link:\n{qr_code_link}\n\nApós o pagamento, você será liberado automaticamente.")
        else:
            await update.message.reply_text("Erro ao gerar cobrança. Tente novamente.")
    except Exception as e:
        await update.message.reply_text("Erro. Tente novamente.")

# Inicia o bot
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("comprar", comprar))
    app.add_handler(CommandHandler("9.99", receber_pagamento))
    app.add_handler(CommandHandler("19.99", receber_pagamento))
    app.add_handler(CommandHandler("29.99", receber_pagamento))
    app.add_handler(CommandHandler("49.99", receber_pagamento))
    
    app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
