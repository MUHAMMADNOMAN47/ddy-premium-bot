import os
import random
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# ---------------------------
# ✅ CONFIG (EDIT HERE)
# ---------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "")  # set in hosting env
CHANNEL_USERNAME = "@duddyofficial_ddy"  # channel where bot will post

PAIR_ADDRESS = "6d45shzdibc366zcxxqg58im4dz5r6svakcmxd9xsexb"
TOKEN_MINT = "8M3CJC3QzKbaLcCFmyYZGVVZ5MgPVN9DNQatSLNUpump"

WEBSITE = "https://duddy.fun"
X_LINK = "https://x.com/official_duddy"
WHATSAPP_LINK = "https://whatsapp.com/channel/0029VbBmrsNHLHQY5eylWR2d"
DISCORD_LINK = "https://discord.gg/aKgK2RDep"

PUMPFUN_LINK = f"https://pump.fun/coin/{TOKEN_MINT}"

WHITEPAPER_DOWNLOAD = "https://drive.google.com/uc?export=download&id=1doT7OlbdiH132yMvqQ057FrfmwJPjgaY"

JUPITER_BUY = f"https://jup.ag/swap/SOL-{TOKEN_MINT}?ref=fib8e2fpaiav"
JUPITER_TOKEN = f"https://jup.ag/tokens/{TOKEN_MINT}"

BIRDEYE = f"https://birdeye.so/solana/token/{TOKEN_MINT}"
DEX = f"https://dexscreener.com/solana/{PAIR_ADDRESS}"


# ---------------------------
# ✅ HELPERS
# ---------------------------
def format_k(num):
    try:
        num = float(num)
    except:
        return "N/A"

    if num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    if num >= 1_000:
        return f"{num/1_000:.2f}K"
    return f"{num:.0f}"


def fetch_dex_data():
    url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{PAIR_ADDRESS}"
    r = requests.get(url, timeout=10)
    j = r.json()
    pair = j.get("pairs", [None])[0]
    if not pair:
        return None

    return {
        "priceUsd": pair.get("priceUsd"),
        "change24h": (pair.get("priceChange", {}) or {}).get("h24"),
        "liqUsd": (pair.get("liquidity", {}) or {}).get("usd"),
        "vol24h": (pair.get("volume", {}) or {}).get("h24"),
    }


def premium_keyboard():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🟢 Buy DDY (Jupiter)", url=JUPITER_BUY)],
            [
                InlineKeyboardButton("🚀 Pump.fun", url=PUMPFUN_LINK),
                InlineKeyboardButton("📄 Whitepaper", url=WHITEPAPER_DOWNLOAD),
            ],
            [
                InlineKeyboardButton("🌐 Website", url=WEBSITE),
                InlineKeyboardButton("𝕏 X", url=X_LINK),
            ],
            [
                InlineKeyboardButton("📱 WhatsApp", url=WHATSAPP_LINK),
                InlineKeyboardButton("🎮 Discord", url=DISCORD_LINK),
            ],
            [
                InlineKeyboardButton("📊 Birdeye", url=BIRDEYE),
                InlineKeyboardButton("📈 Dex", url=DEX),
            ],
            [InlineKeyboardButton("🧾 DDY Token Page", url=JUPITER_TOKEN)],
        ]
    )


def premium_post_text():
    d = fetch_dex_data()

    if not d:
        return (
            "$DDY Auto Update 🐶🔥\n\n"
            "Price: N/A\n24H: N/A\nLiquidity: N/A\nVolume 24H: N/A\n\n"
            f"CA: {TOKEN_MINT}\n\n"
            "#DUDDY\n$DDY"
        )

    price = f"${d['priceUsd']}" if d.get("priceUsd") else "N/A"
    ch = f"{d['change24h']}%" if d.get("change24h") is not None else "N/A"
    liq = f"${format_k(d.get('liqUsd'))}"
    vol = f"${format_k(d.get('vol24h'))}"

    mood = "Tracking smoothly ✅"
    try:
        c = float(d["change24h"])
        if c >= 20:
            mood = "Momentum strong ✅"
        elif c <= -10:
            mood = "Cooldown ⚠️"
        else:
            mood = "Building up 📈"
    except:
        pass

    return (
        "$DDY Auto Update 🐶🔥\n\n"
        f"• Price: {price}\n"
        f"• 24H: {ch}\n"
        f"• Liquidity: {liq}\n"
        f"• Volume (24H): {vol}\n\n"
        f"CA: {TOKEN_MINT}\n\n"
        f"{mood}\n\n"
        "#DUDDY\n"
        "$DDY"
    )


def random_meme_text():
    memes = [
        "🐶🔥 DUDDY holders don’t panic… we reload.\nNo stress, when DUDDY is with you ✅\n#DUDDY #DDY\n$DDY",
        "🚀 DDY isn’t a quick flip — it’s a journey.\nWeak hands fade, real holders stay 💎\n#DUDDY #DDY\n$DDY",
        "😄 Market shaking? DDY chilling.\nWe don’t chase… we build ✅🐶\n#DUDDY #DDY\n$DDY",
        "⚡️ DDY energy is different.\nPatience prints, hype follows 🔥\n#DUDDY #DDY\n$DDY",
        "🟢 When DDY moves… it doesn’t ask permission.\nStrap in 🐶🚀\n#DUDDY #DDY\n$DDY",
    ]
    return random.choice(memes)


# ---------------------------
# ✅ COMMANDS
# ---------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = (
        "✅ *DDY Premium Bot Ready*\n\n"
        "Commands:\n"
        "• /price — Auto Update Post\n"
        "• /meme — Meme Post\n"
        "• /links — Official Buttons\n"
        "• /long — Pepper Long Setup\n"
        "• /short — Pepper Short Setup\n\n"
        "🐶 DUDDY is with you."
    )
    await update.message.reply_text(txt, reply_markup=premium_keyboard(), parse_mode="Markdown")


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = premium_post_text()
    # Post in channel
    await context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=msg,
        reply_markup=premium_keyboard(),
        disable_web_page_preview=True,
    )
    await update.message.reply_text("✅ Posted DDY premium update to channel.")


async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = random_meme_text()
    await context.bot.send_message(
        chat_id=CHANNEL_USERNAME,
        text=msg,
        reply_markup=premium_keyboard(),
        disable_web_page_preview=True,
    )
    await update.message.reply_text("✅ Posted DDY meme to channel.")


async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ DDY Official Links",
        reply_markup=premium_keyboard(),
        disable_web_page_preview=True,
    )


async def long_setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    template = (
        "$DDY — Pepper Long Setup ✅\n\n"
        "Entry: ________\n"
        "SL: ________\n"
        "Targets:\n"
        "TP1 → ________\n"
        "TP2 → ________\n"
        "TP3 → ________\n\n"
        "Plan: Buy dips, scale out, protect capital.\n\n"
        "#DDY\n$DDY"
    )
    await update.message.reply_text(template, reply_markup=premium_keyboard())


async def short_setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    template = (
        "$DDY — Pepper Short Setup ⚠️\n\n"
        "Entry: ________\n"
        "SL: ________\n"
        "Targets:\n"
        "TP1 → ________\n"
        "TP2 → ________\n"
        "TP3 → ________\n\n"
        "Plan: Wait for rejection, manage risk.\n\n"
        "#DDY\n$DDY"
    )
    await update.message.reply_text(template, reply_markup=premium_keyboard())


# ---------------------------
# ✅ MAIN
# ---------------------------
def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN env var missing. Set BOT_TOKEN in your hosting environment.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("meme", meme))
    app.add_handler(CommandHandler("links", links))
    app.add_handler(CommandHandler("long", long_setup))
    app.add_handler(CommandHandler("short", short_setup))

    print("✅ DDY Premium Bot running...")
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
