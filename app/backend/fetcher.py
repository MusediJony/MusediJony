import yfinance as yf


def get_latest_price():
    """Return (price, timestamp) for the latest S&P 500 close price, or (None, None) on failure."""
    try:
        data = yf.download(tickers="^GSPC", period="1d", interval="1m", progress=False)
        if data is None or data.empty:
            return None, None
        last = data['Close'].iloc[-1]
        ts = data.index[-1].to_pydatetime()
        return float(last), ts
    except Exception:
        return None, None


def get_history(period='1d', interval='1m'):
    """Return a DataFrame with historical data for plotting or analysis."""
    try:
        data = yf.download(tickers="^GSPC", period=period, interval=interval, progress=False)
        return data
    except Exception:
        return None
