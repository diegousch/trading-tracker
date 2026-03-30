import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import calendar
import os

CSV_FILE = "trading_records.csv"

st.set_page_config(
    page_title="Diego Options Profit Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===================== CSS FINAL - COMPACTO Y BONITO =====================
st.markdown("""
<style>
    .main {background-color: #0a0e17; color: #e0e0e0;}
    
    .title {
        font-size: 2.9rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00ff9d, #00ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    
    /* Grid de meses - 4 columnas perfectas y compactas */
    .month-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-top: 1rem;
    }
    .month-card {
        background: #111827;
        border: 2px solid #334155;
        border-radius: 20px;
        padding: 1.4rem 1rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    .month-card:hover {
        border-color: #00ff9d;
        transform: translateY(-6px);
        box-shadow: 0 20px 40px rgba(0, 255, 157, 0.2);
    }
    
    /* Días de la semana - barras compactas verticales */
    .day-bar {
        background: #1a2338;
        border-radius: 16px;
        padding: 1rem 1.4rem;
        margin-bottom: 0.8rem;
        border: 2px solid #334155;
        display: flex;
        align-items: center;
        gap: 1.5rem;
        transition: all 0.3s ease;
    }
    .day-bar:hover {border-color: #00ff9d;}
    
    .profit-positive {color: #00ff9d; font-size: 1.75rem; font-weight: 700;}
    .profit-negative {color: #ff5252; font-size: 1.75rem; font-weight: 700;}
    
    .progress-bar {
        height: 14px;
        background: #334155;
        border-radius: 9999px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .cloud {
        background: #1a2338;
        color: #00ccff;
        padding: 12px 24px;
        border-radius: 9999px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 4px 15px rgba(0, 204, 255, 0.25);
    }
</style>
""", unsafe_allow_html=True)

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
    st.markdown('<div style="max-width:420px; margin:120px auto; text-align:center; padding:2.5rem 2rem; background:#111827; border-radius:24px; border:1px solid #334155;">', unsafe_allow_html=True)
    st.markdown('<p class="title">📈 Diego\'s Options Profit Tracker</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94a3b8; font-size:1.15rem; margin-bottom:2rem;">Tu tracker profesional de opciones</p>', unsafe_allow_html=True)
    st.subheader("🔑 Iniciar sesión")
    pw = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña", label_visibility="collapsed")
    if st.button("Entrar", type="primary", use_container_width=True):
        if pw == "1234":
            st.session_state.logged_in = True
            st.success("¡Bienvenido de nuevo, Diego!")
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ===================== UTILIDADES =====================
def get_current_week():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    return [monday + timedelta(days=i) for i in range(5)]

def get_week_profit(week_dates):
    records = {r["Fecha"]: r["Profit"] for r in st.session_state.records}
    return sum(records.get(d.strftime("%Y-%m-%d"), 0) for d in week_dates)

def get_day_record(fecha_str):
    for r in st.session_state.records:
        if r["Fecha"] == fecha_str:
            return r
    return None

def get_month_days(año, mes):
    _, num_dias = calendar.monthrange(año, mes)
    return sum(1 for d in range(1, num_dias+1) if date(año, mes, d).weekday() < 5)

# NUEVA FUNCIÓN PARA SEMANAS CON SEMANAS PARCIALES AL INICIO DEL MES
def get_month_weeks(año, mes):
    weeks = []
    current = date(año, mes, 1)
    while current.month == mes:
        week = []
        for i in range(7):  # hasta 7 días para capturar parciales
            day = current + timedelta(days=i)
            if day.month != mes:
                break
            if day.weekday() < 5:  # solo lunes a viernes
                week.append(day)
            if len(week) == 5:
                break
        if week:
            weeks.append(week)
        # Avanzar al siguiente lunes (o al día siguiente si es parcial)
        if week:
            last = week[-1]
            days_to_next_monday = (7 - last.weekday()) % 7
            current = last + timedelta(days=days_to_next_monday)
        else:
            current += timedelta(days=1)
    return weeks

# ===================== SIDEBAR =====================
st.sidebar.markdown("### Menú")
pagina = st.sidebar.radio("", ["Semana Actual", "Ver por Mes", "Resumen General"], label_visibility="collapsed")

if st.sidebar.button("🗑️ Limpiar todo (prueba)"):
    st.session_state.records = []
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
    st.success("Todo limpiado")
    st.rerun()

# ===================== SEMANA ACTUAL - BARRAS COMPACTAS =====================
if pagina == "Semana Actual":
    st.markdown('<p class="title">Semana Actual</p>', unsafe_allow_html=True)
    
    week_dates = get_current_week()
    week_total = get_week_profit(week_dates)
    meta_semanal = 1750
    progreso = min(max((week_total / meta_semanal) * 100, 0), 100)

    st.markdown(f"**{week_dates[0].strftime('%d %b')} — {week_dates[4].strftime('%d %b %Y')}**")
    
    st.markdown(f"""
    <div style="background:#111827; padding:1.6rem; border-radius:20px; margin:1rem 0;">
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-weight:600;">
            <span>Progreso semanal</span>
            <span>${week_total:,.0f} / ${meta_semanal}</span>
        </div>
        <div class="progress-bar"><div style="width:{progreso}%; height:100%; background:linear-gradient(90deg, #00ff9d, #00ccff);"></div></div>
    </div>
    """, unsafe_allow_html=True)

    if week_total >= meta_semanal:
        st.success("🎉 Meta semanal completada")
    else:
        st.markdown(f'<div class="cloud">☁️ Faltan <strong>${meta_semanal - week_total:,.0f}</strong> para cerrar la semana</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("Días de la semana")

    for day in week_dates:
        fecha_str = day.strftime("%Y-%m-%d")
        record = get_day_record(fecha_str)
        profit = record["Profit"] if record else 0.0
        notas = record["Notas"] if record else "Sin registro"
        
        color_class = "profit-positive" if profit >= 0 else "profit-negative"
        
        st.markdown(f"""
        <div class="day-bar">
            <div style="min-width:110px;">
                <strong>{day.strftime('%A')}</strong><br>
                <small>{day.strftime('%d %b')}</small>
            </div>
            <div style="flex:1; text-align:center;">
                <span class="{color_class}">${profit:,.2f}</span>
            </div>
            <div style="flex:2; color:#94a3b8; font-size:0.95rem;">
                {notas if len(notas) < 60 else notas[:57] + "..."}
            </div>
            <div style="min-width:100px;">
        """, unsafe_allow_html=True)
        
        if st.button("Editar", key=f"edit_w_{fecha_str}", use_container_width=True):
            st.session_state.editing_date = fecha_str
            st.session_state.editing_profit = profit
            st.session_state.editing_notas = notas
            st.rerun()
        
        st.markdown('</div></div>', unsafe_allow_html=True)

    # Formulario edición
    if "editing_date" in st.session_state:
        fecha = st.session_state.editing_date
        st.divider()
        st.subheader(f"✏️ Editando {fecha}")
        
        profit = st.number_input("Profit del día ($)", value=0.0, step=10.0)  # Siempre inicia en 0
        notas = st.text_area("Notas / Operaciones detalladas", value=st.session_state.editing_notas, height=120)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Guardar cambios", type="primary", use_container_width=True):
                record = get_day_record(fecha)
                if record:
                    record["Profit"] = round(profit, 2)
                    record["Notas"] = notas
                else:
                    st.session_state.records.append({
                        "Fecha": fecha,
                        "Día": datetime.strptime(fecha, "%Y-%m-%d").strftime("%A"),
                        "Profit": round(profit, 2),
                        "Notas": notas
                    })
                save_records(st.session_state.records)
                st.success("✅ Guardado correctamente")
                for k in ["editing_date", "editing_profit", "editing_notas"]:
                    st.session_state.pop(k, None)
                st.rerun()
        with c2:
            if st.button("Cancelar", use_container_width=True):
                for k in ["editing_date", "editing_profit", "editing_notas"]:
                    st.session_state.pop(k, None)
                st.rerun()

# ===================== VER POR MES - GRID 4 COLUMNAS PERFECTO =====================
elif pagina == "Ver por Mes":
    st.markdown('<p class="title">Ver por Mes</p>', unsafe_allow_html=True)
    
    año = st.selectbox("Año", range(2026, 2031), index=0, label_visibility="collapsed")
    
    st.markdown("### Todos los meses del año")
    
    meses_nombres = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    
    st.markdown('<div class="month-grid">', unsafe_allow_html=True)
    
    for i in range(12):
        mes_num = i + 1
        nombre = meses_nombres[i]
        dias_lab = get_month_days(año, mes_num)
        meta = 350 * dias_lab
        datos = [r for r in st.session_state.records if r["Fecha"].startswith(f"{año}-{mes_num:02d}")]
        logrado = sum(r.get("Profit", 0) for r in datos)

        st.markdown(f"""
        <div class="month-card" onclick="document.getElementById('mes_btn_{año}_{mes_num}').click();">
            <h3 style="margin:0 0 8px 0;">{nombre}</h3>
            <div style="font-size:2rem; font-weight:700; color:#00ff9d;">${logrado:,.0f}</div>
            <div style="color:#94a3b8; font-size:0.95rem;">Meta: ${meta:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Seleccionar", key=f"mes_btn_{año}_{mes_num}", use_container_width=True):
            st.session_state.selected_año = año
            st.session_state.selected_mes = mes_num
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Detalle del mes seleccionado
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
            st.success(f"🎯 Meta mensual alcanzada (+${delta:,.0f})")
        else:
            st.error(f"❌ Meta mensual no alcanzada (faltan ${abs(delta):,.0f})")

        st.subheader("Semanas del mes")
        weeks = get_month_weeks(año, mes)

        for idx, week_days in enumerate(weeks, 1):
            start = week_days[0].strftime("%d %b")
            end = week_days[-1].strftime("%d %b")
            week_total = get_week_profit(week_days)

            with st.expander(f"Semana {idx} • {start} - {end} • Total ${week_total:,.2f}", expanded=False):
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
                        if st.button("Editar", key=f"edit_m_{fecha_str}", use_container_width=True):
                            st.session_state.editing_date = fecha_str
                            st.session_state.editing_profit = profit
                            st.session_state.editing_notas = notas
                            st.rerun()

# ===================== RESUMEN GENERAL =====================
else:
    st.markdown('<p class="title">Resumen General</p>', unsafe_allow_html=True)
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        total = df["Profit"].sum()
        dias = len(df)
        promedio = total / dias if dias > 0 else 0
        col1, col2, col3 = st.columns(3)
        col1.metric("Total ganado", f"${total:,.2f}")
        col2.metric("Promedio diario", f"${promedio:,.2f}")
        col3.metric("Días operados", dias)
        
        import plotly.express as px
        fig = px.bar(df, x="Fecha", y="Profit", title="Profit diario", template="plotly_dark")
        fig.add_hline(y=350, line_dash="dash", line_color="#eab308")
        fig.add_hline(y=750, line_dash="dash", line_color="#00ccff")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aún no hay registros.")

st.caption("💼 Diego Options Trading Journal • Versión 7.2 - Grid 4 columnas + Semanas parciales")
