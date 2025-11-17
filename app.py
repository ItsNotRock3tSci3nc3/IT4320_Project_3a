from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests

app = Flask(__name__)

API_KEY = "YOUR_ALPHA_VANTAGE_KEY"

if not os.path.exists("static"):
    os.makedirs("static")

# Load stock symbols from CSV
def load_stock_symbols():
    df = pd.read_csv("stocks.csv")
    return df["Symbol"].tolist()

STOCKS = load_stock_symbols()


def get_stock_data(symbol):
    url = (
        f"https://www.alphavantage.co/query?"
        f"function=TIME_SERIES_DAILY&symbol={symbol}"
        f"&apikey={API_KEY}&outputsize=full"
    )
    data = requests.get(url).json()

    if "Time Series (Daily)" not in data:
        print("API ERROR:", data)
        return None
    
    return data



def generate_chart(symbol, series, chart_type, start_date, end_date):
    data = get_stock_data(symbol)

    # If API returned nothing, stop immediately
    if data is None:
        print("No data returned for symbol:", symbol)
        return None

    # If API returned an error message
    if "Time Series (Daily)" not in data:
        print("API Response Error:", data)
        return None
    data = get_stock_data(symbol)

    if "Time Series (Daily)" not in data:
        return None

    ts = data["Time Series (Daily)"]

    df = pd.DataFrame.from_dict(ts, orient="index")
    df.index = pd.to_datetime(df.index)

    df = df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    })

    df = df.sort_index()

    # Filter date range
    if not start_date:
        start_date = df.index.min()
    if not end_date:
        end_date = df.index.max()
    df = df[start_date:end_date]
    if df.empty:
        return None

    if df.empty:
        return None    


    y = df[series]

    plt.figure()

    if chart_type == "line":
        plt.plot(df.index, y)
    elif chart_type == "bar":
        plt.bar(df.index, y)
    elif chart_type == "scatter":
        plt.scatter(df.index, y)

    plt.title(f"{symbol} - {series} ({chart_type})")
    plt.xlabel("Date")
    plt.ylabel(series.capitalize())

    # Save chart
    filepath = os.path.join("static", "plot.png")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()

    return "plot.png"


@app.route("/", methods=["GET", "POST"])
def index():
    chart = None

    if request.method == "POST":
        symbol = request.form.get("symbol")
        series = request.form.get("series")
        chart_type = request.form.get("chart_type")
        start_date = request.form.get("start")
        end_date = request.form.get("end")

        chart = generate_chart(symbol, series, chart_type, start_date, end_date)

    return render_template(
        "index.html",
        stocks=STOCKS,
        chart=chart
    )



if __name__ == "__main__":
    app.run(debug=True)
