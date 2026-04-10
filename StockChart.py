#必要ライブラリインポート
import yfinance as yf
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

st.title('株価チャートアプリ')

st.sidebar.write("""
# America株価チャート
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")
st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"""
### 過去 **{days}日間** の株価
""")



@st.cache_data
def get_data(days, tickers):
    symbols = list(tickers.values())
    
    # period指定より start/end の方が安定
    end = pd.Timestamp.today()
    start = end - pd.Timedelta(days=days)
    
    raw = yf.download(symbols, start=start, end=end, auto_adjust=True, progress=False)
    
    # yfinance 0.2系はMultiIndexになる場合がある
    if isinstance(raw.columns, pd.MultiIndex):
        close = raw['Close']
    else:
        close = raw[['Close']]
    
    # DataFrameに統一
    if isinstance(close, pd.Series):
        close = close.to_frame()
        close.columns = symbols
    
    # 企業名に列名変換
    inv_tickers = {v: k for k, v in tickers.items()}
    close = close.rename(columns=inv_tickers)
    
    # NaNを含む列を確認（デバッグ用）
    st.sidebar.write(f"取得行数: {len(close)}")
    
    close.index = close.index.strftime('%d %B %Y')
    df = close.T
    df.index.name = 'Name'
    return df



#@st.cache_data
#def get_data(days, tickers):
#    df = pd.DataFrame()
#    for company in tickers.keys():
    #company = 'Apple'

#        tkr = yf.Ticker(tickers[company])
#        hist = tkr.history(period=f'{days}d')

#        hist.index = hist.index.strftime('%d %B %Y')
#        hist = hist[['Close']]
#        hist.columns = [company]

#        hist = hist.T
#        hist.index.name = 'Name'
#        df = pd.concat([df, hist])
#    return df

try:
    st.sidebar.write("""
    ## 米国市場株価の範囲指定
    """)
    ymin,ymax = st.sidebar.slider(
        '範囲を指定してください', 0.0, 800.0, (0.0, 800.0)
    )

    tickers = {
        'Apple':'AAPL',
        'Microsoft':'MSFT',
        'Google':'GOOGL',
        'Amazon':'AMZN',
        'Meta':'META',
        'Netflix':'NFLX',
        'Tesla':'TSLA',
        'Nvidia':'NVDA'
    }
    df = get_data(days, tickers)
    companies = st.multiselect(
        '株価を表示する企業を選択してください',
        list(df.index),
        ['Microsoft','Google','Amazon','Nvidia']
    )

    if not companies:
        st.error('少なくとも一社は選んでください')
    else:
        #選択された企業のデータを企業名インデックスでソート表示
        data = df.loc[companies]
        st.write("### 株価(USD)", data.sort_index())
        #グラフ用に日付インデックスに整形
        data = data.T.reset_index()
        #グラフ用にピボット解体
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value':'Stock Prices(USD)'}
        )

        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color="Name:N"
            )
        )
        st.altair_chart(chart, use_container_width=True)
except Exception as e:
    st.error(
        f"otto!エラーが発生しました。{e}"
    )

