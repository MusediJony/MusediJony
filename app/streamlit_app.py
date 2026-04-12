import time
import pandas as pd
import streamlit as st
from backend.fetcher import get_latest_price
from notifications.notifier import notify


st.set_page_config(page_title="S&P 500 Tracker", layout="wide")

st.title("S&P 500 Live Tracker")
col_left, col_right = st.columns([1, 3])
metric_holder = col_left.empty()
chart_holder = col_right.empty()

if 'prices' not in st.session_state:
    st.session_state['prices'] = []
if 'times' not in st.session_state:
    st.session_state['times'] = []
if 'last_notified_price' not in st.session_state:
    st.session_state['last_notified_price'] = None

INTERVAL_SECONDS = 5
MAX_POINTS = 240

try:
    while True:
        price, ts = get_latest_price()
        if price is None:
            st.warning("Failed to fetch latest price — retrying...")
            time.sleep(INTERVAL_SECONDS)
            continue

        st.session_state['prices'].append(price)
        st.session_state['times'].append(ts)

        # trim
        if len(st.session_state['prices']) > MAX_POINTS:
            st.session_state['prices'] = st.session_state['prices'][-MAX_POINTS:]
            st.session_state['times'] = st.session_state['times'][-MAX_POINTS:]

        # compute delta vs previous point
        if len(st.session_state['prices']) > 1:
            prev = st.session_state['prices'][-2]
            delta = price - prev
        else:
            delta = 0.0

        metric_holder.metric(label="Current Price", value=f"${price:,.2f}", delta=f"${delta:+.2f}")

        df = pd.DataFrame({'price': st.session_state['prices']}, index=pd.to_datetime(st.session_state['times']))
        chart_holder.line_chart(df)

        # notify when price moves by $0.50 or more from last notified price
        last_notified = st.session_state['last_notified_price']
        if last_notified is None:
            st.session_state['last_notified_price'] = price
        elif abs(price - last_notified) >= 0.5:
            notify("S&P 500 moved", f"Price ${price:.2f} (change ${price-last_notified:+.2f})")
            st.session_state['last_notified_price'] = price

        time.sleep(INTERVAL_SECONDS)
except KeyboardInterrupt:
    pass
