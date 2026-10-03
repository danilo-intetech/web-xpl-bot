import os
import subprocess
import urllib.request
import urllib.parse
import json

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

NMAP_PATH = r"C:\Program Files (x86)\Nmap\nmap.exe"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Web XPL Bot funcionando!\n\n"
        "Usa /help para ver los comandos disponibles."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponibles:\n"
        "/start - Iniciar el bot\n"
        "/help - Mostrar ayuda\n"
        "/nmap <host> - Escaneo básico de un host autorizado\n"
        "/gau <dominio> - Recolectar URLs públicas\n"
        "/crt <dominio> - Buscar subdominios en certificados públicos\n"
        "/ipinfo <IP> - Consultar información pública de una IP"
    )


async def nmap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Uso: /nmap <host>\n"
            "Ejemplo: /nmap localhost"
        )
        return

    host = context.args[0]

    await update.message.reply_text(
        f"🔎 Iniciando escaneo de {host}..."
    )

    try:
        result = subprocess.run(
            [NMAP_PATH, host],
            capture_output=True,
            text=True,
            timeout=60
        )

        output = result.stdout.strip()

        if not output:
            output = result.stderr.strip()

        if len(output) > 4000:
            output = output[:4000] + "\n...[resultado truncado]"

        await update.message.reply_text(
            f"```text\n{output}\n```",
            parse_mode="Markdown"
        )

    except subprocess.TimeoutExpired:
        await update.message.reply_text(
            "⏱️ El escaneo tardó demasiado y fue cancelado."
        )

    except FileNotFoundError:
        await update.message.reply_text(
            "❌ No se encontró Nmap en la ruta configurada."
        )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Error al ejecutar Nmap: {error}"
        )


async def gau_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Uso: /gau <dominio>\n"
            "Ejemplo: /gau example.com"
        )
        return

    domain = context.args[0]

    await update.message.reply_text(
        f"🔎 Buscando URLs públicas de {domain}..."
    )

    try:
        query = urllib.parse.quote(f"domain:{domain}")
        url = f"https://urlscan.io/api/v1/search/?q={query}"

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Web-XPL-Bot/1.0"}
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        results = data.get("results", [])
        urls = []

        for item in results:
            page = item.get("page", {})
            page_url = page.get("url")

            if page_url and page_url not in urls:
                urls.append(page_url)

        if not urls:
            output = "No se encontraron URLs públicas."
        else:
            output = "\n".join(urls)

        if len(output) > 4000:
            output = output[:4000] + "\n...[resultado truncado]"

        await update.message.reply_text(
            f"```text\n{output}\n```",
            parse_mode="Markdown"
        )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Error al consultar URLScan: {error}"
        )


async def crt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Uso: /crt <dominio>\n"
            "Ejemplo: /crt example.com"
        )
        return

    domain = context.args[0].strip()

    await update.message.reply_text(
        f"🔎 Buscando subdominios públicos de {domain}..."
    )

    try:
        encoded_domain = urllib.parse.quote(domain)
        url = f"https://api.ctlogs.dev/v1/hosts/{encoded_domain}"

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Web-XPL-Bot/1.0"}
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        hosts = data.get("hosts", [])
        subdomains = []

        for item in hosts:
            host = item.get("host")

            if host and host not in subdomains:
                subdomains.append(host)

        if not subdomains:
            output = "No se encontraron subdominios."
        else:
            output = "\n".join(subdomains)

        if len(output) > 4000:
            output = output[:4000] + "\n...[resultado truncado]"

        await update.message.reply_text(
            f"```text\n{output}\n```",
            parse_mode="Markdown"
        )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Error al consultar certificados: {error}"
        )


async def ipinfo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Uso: /ipinfo <IP>\n"
            "Ejemplo: /ipinfo 8.8.8.8"
        )
        return

    ip = context.args[0].strip()

    await update.message.reply_text(
        f"🔎 Consultando información de {ip}..."
    )

    try:
        url = f"https://ipinfo.io/{urllib.parse.quote(ip)}/json"

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Web-XPL-Bot/1.0"}
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(
                response.read().decode("utf-8")
            )

        output = json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        )

        if len(output) > 4000:
            output = output[:4000] + "\n...[resultado truncado]"

        await update.message.reply_text(
            f"```json\n{output}\n```",
            parse_mode="Markdown"
        )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Error al consultar IPinfo: {error}"
        )


def main():
    if not TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN no está configurado."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("nmap", nmap_command))
    app.add_handler(CommandHandler("gau", gau_command))
    app.add_handler(CommandHandler("crt", crt_command))
    app.add_handler(CommandHandler("ipinfo", ipinfo_command))

    print("Bot iniciado...")

    app.run_polling()


if __name__ == "__main__":
    main()