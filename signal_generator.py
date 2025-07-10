import yfinance as yf
import pandas as pd
import ta
import json

tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX", "BABA", "JPM",
    "V", "DIS", "ADBE", "PYPL", "CRM", "INTC", "CSCO", "ORCL", "BAC", "WFC",
    "C", "GS", "MS", "AXP", "IBM", "QCOM", "TXN", "AMD", "MU", "AVGO",
    "INTU", "NOW", "SBUX", "MCD", "NKE", "LOW", "HD", "LULU", "BKNG", "SPGI",
    "BLK", "T", "VZ", "TMUS", "CHTR", "CMCSA", "DISH", "F", "GM", "HMC",
    "TM", "RIVN", "LCID", "NIO", "LI", "XPEV", "FSR", "PLTR", "SNOW", "TWLO",
    "DDOG", "FSLY", "NET", "OKTA", "ZS", "DOCU", "SQ", "SHOP", "ETSY", "ROKU",
    "ZM", "UBER", "LYFT", "DIDI", "BIDU", "PDD", "JD", "TCEHY", "PINS", "TWTR",
    "SNAP", "COST", "WMT", "TGT", "CVS", "MCK", "DG", "DLTR", "ROST", "TJX",
    "KMX", "BBY", "ULTA", "ORLY", "AZO", "TSCO", "GPC", "AAP", "CPRT", "FAST",
    "CHRW", "FDX", "UPS", "DAL", "UAL", "LUV", "ALK", "JBLU", "AAL", "HES",
    "COP", "OXY", "XOM", "CVX", "EOG", "PSX", "VLO", "MPC", "PXD", "CHK",
    "RRC", "APA", "EQT", "SWN", "FANG", "CLR", "CXO", "MRO", "SLB", "HAL",
    "BKR", "NOV", "WMB", "KMI", "ET", "OKE", "EXPD", "JBHT", "GFL", "WM",
    "RSG", "DHI", "LEN", "PHM", "NVR", "MTH", "TOL", "KBH", "LGIH", "EXR",
    "PSA", "AVB", "EQR", "ESS", "MAA", "UDR", "VTR", "WPC", "DRE", "HCP",
    "O", "REG", "PEAK", "BXP", "SLG", "VNO", "ARE", "FRT", "KIM", "SPG",
    "WELL", "BHVN", "MRNA", "BNTX", "NVAX", "INO", "GILD", "BIIB", "AMGN",
    "REGN", "VRTX", "ILMN", "ALXN", "EXAS"
]

signals = []

for symbol in tickers:
    try:
        data = yf.download(symbol, period="2d", interval="1h", progress=False)
        if data.empty:
            continue

        data['rsi'] = ta.momentum.RSIIndicator(data['Close']).rsi()
        last_rsi = data['rsi'].iloc[-1]

        if last_rsi < 30:
            signals.append({"ticker": symbol, "signal": "BUY", "rsi": round(last_rsi, 2)})
        elif last_rsi > 70:
            signals.append({"ticker": symbol, "signal": "SELL", "rsi": round(last_rsi, 2)})
    except Exception as e:
        print(f"Errore con {symbol}: {e}")

if signals:
    message = "📊 *Segnali di trading aggiornati*\n\n"
    for s in signals:
        if s["signal"] == "BUY":
            message += f"✅ *BUY* {s['ticker']} (RSI: {s['rsi']})\n"
        else:
            message += f"❌ *SELL* {s['ticker']} (RSI: {s['rsi']})\n"
else:
    message = "⚠️ Nessun segnale rilevato al momento."

with open("signals.json", "w") as f:
    json.dump(signals, f)

with open("message.txt", "w") as f:
    f.write(message)
