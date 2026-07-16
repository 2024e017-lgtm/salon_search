import pandas as pd
import streamlit as st
import plotly.express as px

# 1. データの読み込み
try:
    df = pd.read_csv("merged.csv")
except FileNotFoundError:
    st.error("データファイル「merged.csv」が見つかりません。先にJupyter Notebookを実行してください。")
    st.stop()

# 2. アプリのタイトルと紹介文
st.title("能登応援！宿泊先サーチアプリ")
st.markdown("""
能登・九十九湾エリアの宿泊施設データを、価格や星評価から自由に探索できるアプリです。
震災からの復興に向けて、素晴らしい宿を客観的なデータから見つけ出しましょう！
""")

# 3. サイドバー・フィルター設定
st.sidebar.header("検索フィルター")

# 価格制限スライダー (最小値〜最大値)
min_p = int(df['price'].min()) if not pd.isna(df['price'].min()) else 1000
max_p = int(df['price'].max()) if not pd.isna(df['price'].max()) else 50000
price_limit = st.sidebar.slider(
    "1人あたり予算の上限（円）",
    min_value=min_p,
    max_value=max_p,
    step=500,
    value=max_p
)

# 星評価の下限
star_limit = st.sidebar.slider(
    "星評価の下限",
    min_value=0.0,
    max_value=5.0,
    step=0.1,
    value=3.0
)

# 4. データのフィルタリング
filtered_df = df.copy()
filtered_df['star_eval'] = filtered_df['star'].fillna(0.0)

filtered_df = filtered_df[
    (filtered_df['price'] <= price_limit) &
    (filtered_df['star_eval'] >= star_limit)
]

# 5. メイン画面の描画
st.subheader(f"条件に合う宿泊施設: {len(filtered_df)} 件")

if len(filtered_df) > 0:
    # 散布図の作成
    fig = px.scatter(
        filtered_df,
        x='pop_score',
        y='price',
        hover_data=['name_hotel', 'access', 'star', 'review'],
        labels={'pop_score': '人気スコア', 'price': '1人あたり価格（円）'},
        title='宿泊価格 × 人気スコア'
    )
    st.plotly_chart(fig)

    # 宿泊先一覧 of 表示
    st.subheader("おすすめの宿泊先一覧")
    for index, row in filtered_df.iterrows():
        star_disp = f"★ {row['star']}" if not pd.isna(row['star']) else "評価未設定"
        st.markdown(f"### [{row['name_hotel']}]({row['link_hotel']})")
        st.write(f"**価格（1人あたり）:** {int(row['price']):,} 円〜 | **評価:** {star_disp} | **口コミ:** {int(row['review'])} 件")
        st.write(f"**アクセス:** {row['access']}")
        st.write("---")
else:
    st.warning("条件に一致する宿泊施設がありません。フィルターを緩めてみてください。")