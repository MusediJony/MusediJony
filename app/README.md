# S&P 500 Live Tracker (Local)

Local Streamlit app that polls the S&P 500 index (^GSPC) and shows a live price chart. Sends a notification each time the price moves by $0.50 or more from the last notified price.

Quick start

1. Open a terminal and change into the `app` directory:

```powershell
cd app
```

2. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run the Streamlit app:

```powershell
streamlit run streamlit_app.py
```

Notes
- The app uses `yfinance` to fetch index data (1m interval). Run it from the `app` folder so the local imports resolve.
- Notifications use `plyer` with a fallback to console printing if the system notifier is unavailable.
