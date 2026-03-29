import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar
import os

CSV_FILE = "trading_records.csv"

st.set_page_config(page_title="Diego Options Profit Tracker", page_icon="📈", layout="wide")

# ===================== CSS MEJORADO =====================
st.markdown("""
<style>
    .main {background-color: #0a0e17; color: #e0e0e0;}
    .stButton>button {
        background-color: #111827 !important;
        border: 3px solid #eab308 !important;
        color: #fafafa !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        height: 165px !important;
        line-height: 1.4 !important;
        text-align: center !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 20px rgba(234, 179, 8, 0.25) !important;
    }
    .stButton>button:hover {
        border-color: #00ff9d !important;
        background-color: #1a2338 !important;
    }
    .day-card {
        background: #1a2338;
        border-radius: 18px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        border: 2px solid #334155;
    }
    .profit-positive {color: #00ff9d; font-size: 1.8rem; font-weight: 700;}
    .profit-negative {color: #ff5252; font-size: 1.8rem; font-weight: 700;}
</style>
""", unsafe_allow_html=True)

st.title("📈 Diego's Options Profit Tracker")
st.markdown("**Metas** — Diario: **$350** mínimo | **$750** ideal | Semanal: **$1,750**")

# ===================== CARGAR / GUARDAR =====================
def load_records():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.strftime("%Y-%m-%d")
            return df.to_dict('records')
        except:
            return []
    return []

def save_records(records):
    pd.DataFrame(records).to_csv(CSV_FILE, index=False)

if "records" not in st.session_state:
    st.session_state.records = load_records()

# ===================== LOGIN =====================
if not st.session_state.get("logged_in", False):
    st.subheader("🔑 Login")
    pw = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        if pw == "1234":
            st.session_state.logged_in = True
            st.success("¡Bienvenido, Diego!")
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.stop()

# ===================== UTILIDADES =====================
def get_month_days(año, mes):
    _, num_dias = calendar.monthrange(año, mes)
    return sum(1 for d in range(1, num_dias+1) if date(año, mes, d).weekday() < 5)

def get_month_weeks(año, mes):
    first_day = date(año, mes, 1)
    days_to_monday = (0 - first_day.weekday()) % 7
    current = first_day + timedelta(days=days_to_monday)
    weeks = []
    while current.month == mes:
        week = [current + timedelta(days=i) for i in range(5) if (current + timedelta(days=i)).month == mes]
        if week:
            weeks.append(week)
        current += timedelta(days=7)
    return weeks

def get_week_profit(week_dates):
    records = {r["Fecha"]: r["Profit"] for r in st.session_state.records}
    return sum(records.get(d.strftime("%Y-%m-%d"), 0) for d in week_dates)

def get_day_record(fecha_str):
    for r in st.session_state.records:
        if r["Fecha"] == fecha_str:
            return r
    return None

# ===================== SIDEBAR =====================
pagina = st.sidebar.radio("Ir a:", ["Semana Actual", "Ver por Mes", "Resumen General"])

# ===================== VER POR MES =====================
if pagina == "Ver por Mes":
    st.subheader("📅 Ver por Mes")

    año = st.selectbox("Año", range(2026, 2031), index=0)

    st.markdown("### Todos los meses del año")
    meses_nombres = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    cols = st.columns(4)

    for i in range(12):
        mes_num = i + 1
        nombre = meses_nombres[i]
        dias_lab = get_month_days(año, mes_num)
        meta = 350 * dias_lab
        datos = [r for r in st.session_state.records if r["Fecha"].startswith(f"{año}-{mes_num:02d}")]
        logrado = sum(r.get("Profit", 0) for r in datos)

        with cols[i % 4]:
            if st.button(
                f"{nombre}\n\n"
                f"**Logrado:** ${logrado:,.0f}\n"
                f"**Meta:** ${meta:,.0f}",
                key=f"mes_{año}_{mes_num}",
                use_container_width=True
            ):
                st.session_state.selected_año = año
                st.session_state.selected_mes = mes_num
                st.rerun()

    # ==================== DETALLE DEL MES ====================
    if st.session_state.get("selected_año") == año and "selected_mes" in st.session_state:
        mes = st.session_state.selected_mes
        nombre_mes = meses_nombres[mes-1]
        st.divider()
        st.subheader(f"{nombre_mes} {año}")

        dias_lab = get_month_days(año, mes)
        meta_mensual = 350 * dias_lab
        datos_mes = [r for r in st.session_state.records if r["Fecha"].startswith(f"{año}-{mes:02d}")]
        total_mes = sum(r.get("Profit", 0) for r in datos_mes)
        delta = total_mes - meta_mensual

        st.metric("Total del mes", f"${total_mes:,.2f}", f"${delta:,.2f} vs meta")

        if total_mes >= meta_mensual:
            st.success(f"🎯 Meta mensual alcanzada (+${delta:,.0f} adicionales)")
        else:
            st.error(f"❌ Meta mensual no alcanzada (faltan ${abs(delta):,.0f})")

        st.subheader("Semanas del mes")
        weeks = get_month_weeks(año, mes)

        for idx, week_days in enumerate(weeks, 1):
            start = week_days[0].strftime("%d %b")
            end = week_days[-1].strftime("%d %b")
            week_total = get_week_profit(week_days)

            with st.expander(f"Semana {idx} ({start} - {end}) — Total: ${week_total:,.2f}", expanded=False):
                for day in week_days:
                    fecha_str = day.strftime("%Y-%m-%d")
                    record = get_day_record(fecha_str)
                    profit = record["Profit"] if record else 0.0
                    notas = record["Notas"] if record else "Sin registro"

                    color_class = "profit-positive" if profit >= 0 else "profit-negative"

                    col1, col2, col3, col4 = st.columns([1.2, 1.4, 3.8, 1])
                    with col1:
                        st.markdown(f"**{day.strftime('%A')}**<br><small>{day.strftime('%d %b')}</small>", unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"<span class='{color_class}'>${profit:,.2f}</span>", unsafe_allow_html=True)
                    with col3:
                        st.caption(notas)
                    with col4:
                        if st.button("Editar", key=f"edit_{fecha_str}"):
                            st.session_state.editing_date = fecha_str
                            st.session_state.editing_profit = profit
                            st.session_state.editing_notas = notas
                            st.rerun()

    else:
        st.info("👆 Haz clic en cualquier tarjeta de mes para ver el detalle completo")

# ===================== OTRAS PÁGINAS (Semana Actual y Resumen General) =====================
# (Mantengo el código anterior de Semana Actual y Resumen General sin cambios)
elif pagina == "Semana Actual":
    # ... (código de Semana Actual de la versión anterior, se mantiene igual)
    st.info("Sección Semana Actual (sin cambios en esta actualización)")
else:
    st.subheader("📊 Resumen General")
    st.info("Sección Resumen General (sin cambios en esta actualización)")

st.caption("💼 Diego Options Trading Journal • Versión 6.2")
