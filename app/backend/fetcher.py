import yfinance as yf
from datetime import datetime


def get_latest_price():
    """Return (price, timestamp) for the latest S&P 500 close price, or (None, None) on failure.

    Uses yf.Ticker.history() for more reliable fetching and logs errors.
    """
    try:
        t = yf.Ticker("^GSPC")
        data = t.history(period="1d", interval="1m")
        if data is None or data.empty:
            print("fetcher: no data returned for ^GSPC")
            return None, None

        # prefer 'Close' but fall back if not present
        if 'Close' in data.columns:
            last = data['Close'].iloc[-1]
        else:
            # try 'close' lowercase
            last = data.iloc[-1].iloc[-1]

        ts = data.index[-1]
        # convert to python datetime if pandas Timestamp
        try:
            ts = ts.to_pydatetime()
        except Exception:
            pass

        return float(last), ts
    except Exception as e:
        print(f"fetcher error: {e}")
        return None, None


def get_history(period='1d', interval='1m'):
    """Return a DataFrame with historical data for plotting or analysis, or None on failure."""
    try:
        t = yf.Ticker("^GSPC")
        data = t.history(period=period, interval=interval)
        return data
    except Exception as e:
        print(f"fetcher history error: {e}")
        return None
