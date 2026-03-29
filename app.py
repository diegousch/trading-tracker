import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar
import os

CSV_FILE = "trading_records.csv"

st.set_page_config(page_title="Diego Options Tracker", page_icon="📈", layout="centered")

# CSS profesional de trading
st.markdown("""
<style>
    .main {background-color: #0e1117; color: #fafafa;}
    .stButton>button {background-color: #00cc66; color: white; border-radius: 8px; font-weight: bold;}
    .stSuccess {background-color: #003322;}
    .stError {background-color: #330000;}
    .metric-label {font-size: 1.1rem;}
</style>
""", unsafe_allow_html=True)

st.title("📈 Diego's Options Profit Tracker")
st.markdown("**Meta diaria:** $350 mínimo | $700 ideal")

# ===================== CARGAR / GUARDAR PERMANENTE =====================
def load_records():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            return df.to_dict('records')
        except:
            return []
    return []

def save_records(records):
    pd.DataFrame(records).to_csv(CSV_FILE, index=False)

if "records" not in st.session_state:
    st.session_state.records = load_records()

# Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔑 Login")
    email = st.text_input("Email", "diego@example.com")
    pw = st.text_input("Contraseña", type="password", value="1234")
    if st.button("Entrar"):
        if pw == "1234":
            st.session_state.logged_in = True
            st.success("¡Bienvenido, Diego!")
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.stop()

# Sidebar
st.sidebar.header("📅 Navegación")
opcion = st.sidebar.radio("Ir a:", ["Registrar Operación", "Ver por Mes", "Gráficos y Resumen"])

# ===================== REGISTRAR / EDITAR / BORRAR =====================
if opcion == "Registrar Operación":
    st.subheader("💰 Registrar o Editar Profit")

    # Selector de fecha (cualquier día)
    fecha_seleccionada = st.date_input("Fecha", value=date.today())
    fecha_str = fecha_seleccionada.strftime("%Y-%m-%d")

    # Buscar si ya existe ese día
    registro_actual = next((r for r in st.session_state.records if r["Fecha"] == fecha_str), None)
    profit_inicial = registro_actual["Profit"] if registro_actual else 0.0
    notas_inicial = registro_actual["Notas"] if registro_actual else ""

    profit = st.number_input("Profit del día ($)", value=profit_inicial, step=10.0)
    notas = st.text_area("Notas / Operaciones", value=notas_inicial, placeholder="Ej: 2 calls SPY + 1 put...")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Guardar / Actualizar"):
            # Si existe, actualizar; si no, agregar
            if registro_actual:
                registro_actual["Profit"] = round(profit, 2)
                registro_actual["Notas"] = notas
            else:
                st.session_state.records.append({
                    "Fecha": fecha_str,
                    "Día": fecha_seleccionada.strftime("%A"),
                    "Profit": round(profit, 2),
                    "Notas": notas
                })
            save_records(st.session_state.records)
            st.success(f"✅ Guardado: ${profit:,.2f} el {fecha_str}")
            st.rerun()

    with col2:
        if registro_actual and st.button("🗑️ Borrar este día", type="secondary"):
            st.session_state.records = [r for r in st.session_state.records if r["Fecha"] != fecha_str]
            save_records(st.session_state.records)
            st.success("Día borrado")
            st.rerun()

    # Lista de todos los registros (para ver rápido)
    st.subheader("📋 Todos los registros")
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df.sort_values("Fecha", ascending=False), use_container_width=True)
    else:
        st.info("Aún no hay registros.")

# ===================== VER POR MES =====================
elif opcion == "Ver por Mes":
    st.subheader("📆 Ver por Mes")

    col1, col2 = st.columns(2)
    with col1:
        año = st.selectbox("Año", range(2024, 2027), index=2)
    with col2:
        meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        mes = st.selectbox("Mes", range(1,13), index=3, format_func=lambda x: meses[x-1])

    primer_dia = date(año, mes, 1)
    _, num_dias = calendar.monthrange(año, mes)

    # Calcular meta mensual (días laborables × 350)
    dias_laborables = sum(1 for d in range(1, num_dias+1) if date(año, mes, d).weekday() < 5)
    meta_mensual = 350 * dias_laborables

    st.markdown(f"**{meses[mes-1]} {año}** — Meta mensual: **${meta_mensual:,.0f}**")

    datos_mes = [r for r in st.session_state.records if r["Fecha"].startswith(f"{año}-{mes:02d}")]
    total_mes = sum(r["Profit"] for r in datos_mes)

    st.metric("Total del mes", f"${total_mes:,.2f}", f"${total_mes - meta_mensual:,.2f} vs meta")

    for dia in range(1, num_dias + 1):
        fecha = date(año, mes, dia)
        if fecha.weekday() >= 5: continue
        fecha_str = fecha.strftime("%Y-%m-%d")
        profit_dia = next((r["Profit"] for r in datos_mes if r["Fecha"] == fecha_str), 0)

        if profit_dia >= 700:
            st.success(f"✅ {fecha.strftime('%d %b')} ({fecha.strftime('%A')}) → **${profit_dia:,.2f}**")
        elif profit_dia >= 350:
            st.info(f"✅ {fecha.strftime('%d %b')} ({fecha.strftime('%A')}) → **${profit_dia:,.2f}**")
        elif profit_dia < 0:
            st.error(f"❌ {fecha.strftime('%d %b')} ({fecha.strftime('%A')}) → **${profit_dia:,.2f}**")
        elif profit_dia > 0:
            st.warning(f"⚠️ {fecha.strftime('%d %b')} ({fecha.strftime('%A')}) → **${profit_dia:,.2f}**")
        else:
            st.write(f"📅 {fecha.strftime('%d %b')} ({fecha.strftime('%A')}) → Sin registro")

# ===================== GRÁFICOS Y RESUMEN =====================
else:
    st.subheader("📊 Gráficos y Resumen")

    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        df = df.sort_values("Fecha")

        total_general = df["Profit"].sum()
        promedio = total_general / len(df) if len(df) > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Ganado", f"${total_general:,.2f}")
        col2.metric("Promedio Diario", f"${promedio:,.2f}")
        col3.metric("Días Operados", len(df))

        # Gráfico de barras con colores verde/rojo
        import plotly.express as px
        df["Color"] = ["#00cc66" if p >= 0 else "#ff4444" for p in df["Profit"]]
        fig = px.bar(df, x="Fecha", y="Profit", color="Color", color_discrete_map={"#00cc66":"#00cc66", "#ff4444":"#ff4444"},
                     title="Profit Diario (verde = ganancia, rojo = pérdida)")
        fig.add_hline(y=350, line_dash="dash", line_color="yellow", annotation_text="Mínimo diario $350")
        fig.add_hline(y=700, line_dash="dash", line_color="orange", annotation_text="Ideal diario $700")
        fig.add_hline(y=1750/5, line_dash="dot", line_color="white", annotation_text="Meta semanal promedio ~$350/día")
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df[["Fecha", "Día", "Profit", "Notas"]], use_container_width=True)
    else:
        st.info("Registra algunos días para ver los gráficos.")

# Botón de limpieza (solo prueba)
if st.sidebar.button("🗑️ Limpiar TODO (prueba)"):
    st.session_state.records = []
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
    st.success("Todo borrado")
    st.rerun()

st.sidebar.caption("Versión 3.0 - Datos permanentes")
