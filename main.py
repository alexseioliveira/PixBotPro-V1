import logging
import requests
import json
import sqlite3
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = '7894687678:AAGrp4b_zY44BcC1ldOpCwxRi4me3Zikfa4'

# Função de pagamento simulada
async def receber_pagamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    valor = update.message.text.split("r")[-1].replace("_", ".")
    try:
        resposta = requests.post("https://api.exemplo.com/pagamento", data={'valor': valor})
        data = resposta.json()

        if data.get('status') == 'success':
            qr_code_link = data['pix']['qrcode_url']
            await update.message.reply_text(f"Realize o pagamento via Pix no link:\n{qr_code_link}\n\nApós o pagamento, confirme aqui.")
        else:
            await update.message.reply_text("Erro ao gerar cobrança. Tente novamente.")
    except Exception as e:
        await update.message.reply_text("Erro. Tente novamente.")

# Inicia o bot
from telegram.ext import ApplicationBuilder, CommandHandler
import asyncio

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("comprar", comprar))
    app.add_handler(CommandHandler("pagar", receber_pagamento))
    app.add_handler(CommandHandler("valor9_99", receber_pagamento))
    app.add_handler(CommandHandler("valor19_99", receber_pagamento))
    app.add_handler(CommandHandler("valor29_99", receber_pagamento))
    app.add_handler(CommandHandler("valor49_99", receber_pagamento))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == '__main__':
    main()


# Funções complementares
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bem-vindo! Use os comandos para iniciar o pagamento.")

async def comprar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Escolha o valor: /valor9_99 /valor19_99 /valor29_99 /valor49_99")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
