import yfinance as yf
import pandas as pd
import altair as alt
import streamlit as st

st.title('株価チャートアプリ')

st.sidebar.write("""
# America株価チャート
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")
st.sidebar.write("## 表示日数選択")
days = st.sidebar.slider('日数', 1, 50, 20)

st.write(f"### 過去 **{days}日間** の株価")

# @st.cache_data
def get_data(days, tickers):
    symbols = list(tickers.values())
    raw = yf.download(
        symbols,
        period=f'{days}d',
        auto_adjust=False,
        progress=False
    )

    # level=0 が 'Close' の列だけを抽出（xs不使用）
    mask = raw.columns.get_level_values(0) == 'Close'
    close = raw.loc[:, mask]
    close.columns = close.columns.get_level_values(1)  # ティッカー名だけにする

    inv_tickers = {v: k for k, v in tickers.items()}
    close = close.rename(columns=inv_tickers)
    close.index = close.index.strftime('%d %B %Y')

    df = close.T
    df.index.name = 'Name'
    return df

try:
    st.sidebar.write("## 米国市場株価の範囲指定")
    ymin, ymax = st.sidebar.slider('範囲を指定してください', 0.0, 3000.0, (0.0, 3000.0))

    tickers = {
        'Apple':     'AAPL',
        'Microsoft': 'MSFT',
        'Google':    'GOOGL',
        'Amazon':    'AMZN',
        'Meta':      'META',
        'Netflix':   'NFLX',
        'Tesla':     'TSLA',
        'Nvidia':    'NVDA'
    }

    df = get_data(days, tickers)

    companies = st.multiselect(
        '株価を表示する企業を選択してください',
        list(df.index),
        ['Microsoft', 'Google', 'Amazon', 'Nvidia']
    )

    if not companies:
        st.error('少なくとも一社は選んでください')
    else:
        data = df.loc[companies]
        st.write("### 株価(USD)", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None,
                        scale=alt.Scale(domain=[ymin, ymax])),
                color="Name:N"
            )
        )
        st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error(f"エラーが発生しました: {e}")
