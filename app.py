import streamlit as st
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

# تنظیمات صفحه
st.set_page_config(page_title="سرمایه‌گذار هوشمند", layout="wide")

# نوار کناری برای ناوبری
pages = {
    "صفحه اصلی": "home",
    "پرتفوی نمونه": "portfolio"
}
page = st.sidebar.radio("📂 انتخاب بخش", list(pages.keys()))

# تابع دریافت قیمت روزانه از وب‌سایت TSETMC
@st.cache_data(ttl=3600)
def fetch_current_price(instrument_id):
    """
    این تابع قیمت پایانی روزانه را برای یک نماد با شناسه‌ی TSETMC بازمی‌گرداند.
    شناسه‌ها باید در mapping پایین تعریف شوند.
    """
    url = f"https://www.tsetmc.com/Loader.aspx?ParTree=15131F&i={instrument_id}"
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        # تگ‌هایی که قیمت را نگهداری می‌کنند ممکن است متفاوت باشند؛ لطفاً بررسی کنید
        price_str = soup.find(id="lblLast").get_text().replace(',', '')
        return float(price_str)
    except Exception as e:
        st.error(f"خطا در دریافت قیمت برای شناسه {instrument_id}: {e}")
        return None

# نگاشت نماد به شناسه TSETMC
symbol_to_id = {
    'شپنا': '10021204322607755',
    'فولاد': '26331843695355338',
    'فملی': '52172491489979424'
    # شناسه سایر نمادها را اینجا اضافه کنید
}

if pages[page] == "home":
    # صفحه اصلی
    st.title("💼 خلاصه کتاب سرمایه‌گذار هوشمند")
    st.markdown("""
    به وب‌سایتی خوش آمدید که بر اساس اصول بنجامین گراهام طراحی شده است — پدر سرمایه‌گذاری ارزشی.

    در اینجا، مفاهیم کلیدی کتاب **سرمایه‌گذار هوشمند** را به زبان ساده بررسی می‌کنیم، و سپس از آن‌ها در پرتفوی‌های نمونه استفاده می‌کنیم که عملکرد آن‌ها را به‌صورت روزانه پیگیری خواهیم کرد.
    """)

    st.header("📘 فصل‌های مهم و مفاهیم کلیدی")
    st.markdown("""
    ### ۱. مفهوم "حاشیه امنیت"
    یعنی سهامی بخرید که قیمت بازار آن بسیار پایین‌تر از ارزش ذاتی آن باشد. این اختلاف، محافظ شما در برابر خطای محاسبه و نوسانات بازار است.

    ### ۲. شخصیت آقای بازار (Mr. Market)
    بازار همیشه منطقی نیست. آقای بازار هر روز قیمت پیشنهادی متفاوتی ارائه می‌دهد، اما شما مجبور نیستید همیشه معامله کنید.

    ### ۳. سرمایه‌گذار تدافعی در مقابل کارآفرینانه
    - **سرمایه‌گذار تدافعی**: دنبال سهام با ثبات و ریسک پایین است.
    - **سرمایه‌گذار کارآفرینانه**: به دنبال فرصت‌هایی برای خرید سهام کم‌ارزش‌گذاری‌شده و پتانسیل رشد بالا.

    ### ۴. تفاوت بین سرمایه‌گذاری و سفته‌بازی
    سرمایه‌گذاری = تحلیل، حاشیه امنیت، دید بلندمدت.
    سفته‌بازی = حدس زدن جهت بازار بدون تحلیل بنیادی.
    """)

    st.header("🧠 انواع سرمایه‌گذار از دید گراهام")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("سرمایه‌گذار تدافعی")
        st.markdown("""
        - انتخاب سهام بزرگ و معتبر
        - تمرکز بر درآمد ثابت و سود تقسیمی
        - حداقل معامله در سال
        - ریسک‌گریز
        """)
    with col2:
        st.subheader("سرمایه‌گذار کارآفرینانه")
        st.markdown("""
        - تحلیل عمیق شرکت‌ها
        - جست‌وجو برای سهام زیرقیمت واقعی
        - پذیرش نوسان بیشتر در مقابل بازده بالقوه بیشتر
        - تحلیل نسبت‌های مالی
        """)

    st.markdown("---")
    st.markdown("🧾 این محتوا صرفاً جهت آموزش و افزایش دانش مالی است و توصیه سرمایه‌گذاری محسوب نمی‌شود.")

elif pages[page] == "portfolio":
    # صفحه پرتفوی نمونه
    st.title("📊 پرتفوی نمونه")
    st.markdown("در این بخش، پرتفوی سود تقسیمی را با عملکرد روزانه مشاهده کنید.")

    # داده‌های اولیه پرتفوی
    data = {
        'نماد': ['شپنا', 'فولاد', 'فملی'],
        'وزن (%)': [40, 30, 30],
        'قیمت خرید': [2500, 1200, 800],
        'تاریخ خرید': ['2025-01-01', '2025-01-01', '2025-01-01']
    }
    df = pd.DataFrame(data)

    # دریافت قیمت‌های جاری و محاسبه بازده
    current_prices = []
    returns = []
    for symbol, buy_price in zip(df['نماد'], df['قیمت خرید']):
        inst_id = symbol_to_id.get(symbol)
        price = fetch_current_price(inst_id) if inst_id else None
        current_prices.append(price)
        if price:
            returns.append((price - buy_price) / buy_price * 100)
        else:
            returns.append(None)
        time.sleep(1)  # جلوگیری از ارسال درخواست‌های سریع پیاپی

    df['قیمت جاری'] = current_prices
    df['بازده (%)'] = returns

    st.subheader("💵 پرتفوی سود تقسیمی")
    st.table(df)

    # محاسبه بازده کل پرتفوی
    weighted_return = sum((r * w / 100) for r, w in zip(returns, df['وزن (%)']) if r is not None)
    st.markdown(f"**بازده کل پرتفوی: {weighted_return:.2f}%**")

    st.markdown("---")
    st.markdown("🧾 این پرتفوی صرفاً نمونه است و توصیه سرمایه‌گذاری نیست.")
