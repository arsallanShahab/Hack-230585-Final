from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import datetime
from sklearn.metrics import mean_squared_error, r2_score
import yfinance as yf


def get_stock_info(name):
    stock = yf.Ticker(name)
    # stock_max = stock_history["Close"].idxmax()
    # stock_min = stock_history["Close"].idxmin()
    print('Info')
    print(stock.info["longName"], stock.info["longBusinessSummary"])
    print()
    print('ISIN')
    print(stock.isin)
    print()
    print('Major Holders')
    print(stock.major_holders)
    print()
    print('Institutional Holders')
    print(stock.institutional_holders)
    print("\n")


def predict_stock(name):
    start = pd.to_datetime('2004-01-01')
    stock = [name]
    yf_initializer = yf.Ticker(name)
    yesterday_data = yf_initializer.history("1d")
    stock_history = yf.download(stock, start=start, end=datetime.date.today())
    features = stock_history[['Open', 'Low', 'Close', 'Volume']]
    target = stock_history['High']
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    X_pred = pd.DataFrame([{
        "Open": float(yesterday_data["Open"].iloc[0]),
        "Low": float(yesterday_data["Low"].iloc[0]),
        "Close": float(yesterday_data["Close"].iloc[0]),
        "Volume": float(yesterday_data["Volume"].iloc[0])
    }])
    y_pred = model.predict(X_pred)
    print(f"\nToday {name} high price should be: ", y_pred)


def top_gainers():
    import pandas as pd
    gainers = pd.read_html('https://finance.yahoo.com/gainers')
    print("\n", gainers, "\n")

    # print(f'Mean Squared Error: {mse:.2f}')
    # print(f'R-squared: {r2:.2f}')
    # print(f'One day data: {yesterday_data}')
