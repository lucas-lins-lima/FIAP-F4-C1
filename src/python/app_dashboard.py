import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from services.climate_service import (
    create_climate_data, list_climate_data, get_climate_data,
    update_climate_data, delete_climate_data
)
from services.component_service import (
    create_component, list_components, get_component,
    update_component, delete_component
)
from services.sensor_service import (
    create_sensor_record, list_sensor_records,
    update_sensor_record, delete_sensor_record
)

from weasyprint import HTML


st.set_page_config(page_title="Dashboard Irrigação", layout="wide")
st.title("FarmTech Solutions - Dashboard de Irrigação Inteligente")

aba = st.sidebar.radio("Selecione a tabela para gerenciar:", ["Visão Geral", "Dados Climáticos", "Registros de Sensores", "Componentes"])

# ---------------------- VISÃO GERAL --------------------------
if aba == "Visão Geral":
        sensor_df = pd.DataFrame(list_sensor_records())

        if sensor_df.empty:
            st.info("Nenhum dado de sensor disponível para mostrar a situação atual da safra.")
        else:
            sensor_df["timestamp"] = pd.to_datetime(sensor_df["timestamp"])
            latest = sensor_df.sort_values("timestamp", ascending=False).iloc[0]

            st.subheader("🌾 Estado Atual da Safra")

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric("Umidade do Solo", f"{latest['soil_moisture']:.2f} %")

            with col2:
                ph_label = f"{latest['soil_ph']:.2f}"
                st.metric("pH do Solo", ph_label)

            with col3:
                phos = "Presente" if latest["phosphorus_present"] else "Ausente"
                st.metric("Fósforo (P)", phos)

            with col4:
                pot = "Presente" if latest["potassium_present"] else "Ausente"
                st.metric("Potássio (K)", pot)

            with col5:
                status = latest["irrigation_status"]
                emoji = "💧" if status == "ATIVADA" else "⛔"
                st.metric("Irrigação", f"{emoji} {status}")

# ---------------------- CLIMATE DATA -------------------------
if aba == "Dados Climáticos":
    st.header("🌤️ Dados Climáticos")
    df = pd.DataFrame(list_climate_data())

    if df.empty:
        st.info("Nenhum dado climático disponível.")
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        st.dataframe(df, use_container_width=True)

        st.subheader("📊 Visualização de tendências climáticas")

        # Temperatura ao longo do tempo
        fig_temp, ax_temp = plt.subplots()
        ax_temp.plot(df["timestamp"], df["temperature"], marker='o', linestyle='-', color='orange')
        ax_temp.set_title("Temperatura ao longo do tempo")
        ax_temp.set_xlabel("Data")
        ax_temp.set_ylabel("Temperatura (°C)")
        ax_temp.grid(True)
        st.pyplot(fig_temp)

        # Umidade ao longo do tempo
        fig_hum, ax_hum = plt.subplots()
        ax_hum.plot(df["timestamp"], df["air_humidity"], marker='s', linestyle='-', color='blue')
        ax_hum.set_title("Umidade do ar ao longo do tempo")
        ax_hum.set_xlabel("Data")
        ax_hum.set_ylabel("Umidade (%)")
        ax_hum.grid(True)
        st.pyplot(fig_hum)

        # Histograma
        fig, ax = plt.subplots()
        ax.hist(df["temperature"], bins=10, color="skyblue")
        ax.set_title("Distribuição da temperatura ambiente")
        ax.set_xlabel("Temperatura (°C)")
        ax.set_ylabel("Frequência")
        st.pyplot(fig)

        # Dispersão temperatura x umidade
        fig2, ax2 = plt.subplots()
        ax2.scatter(df["temperature"], df["air_humidity"], color="green")
        ax2.set_xlabel("Temperatura (°C)")
        ax2.set_ylabel("Umidade do Ar (%)")
        ax2.set_title("Correlação entre temperatura e umidade")
        st.pyplot(fig2)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Exportar como CSV",
            data=csv,
            file_name='climate_data.csv',
            mime='text/csv'
        )

        try:
            html = df.to_html(index=False)
            HTML(string=html).write_pdf("climate_data.pdf")
            with open("climate_data.pdf", "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="⬇️ Exportar como PDF",
                data=pdf_bytes,
                file_name='climate_data.pdf',
                mime='application/pdf'
            )
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

    with st.expander("Novo Registro Climático"):
        col1, col2, col3 = st.columns(3)
        with col1:
            temperature = st.number_input("Temperatura (°C)", format="%.2f")
        with col2:
            air_humidity = st.number_input("Umidade do ar (%)", format="%.2f")
        with col3:
            rain_forecast = st.checkbox("Previsão de chuva")

        if st.button("Cadastrar"):
            record = create_climate_data({
                "temperature": temperature,
                "air_humidity": air_humidity,
                "rain_forecast": rain_forecast,
                "timestamp": datetime.utcnow()
            })
            st.success(f"Registro criado com ID {record['id']}")
            st.rerun()

    with st.expander("Editar ou remover registro climático"):
        ids = [r["id"] for r in list_climate_data()]
        selected_id = st.selectbox("Selecione o registro:", ids)
        if selected_id:
            registro = get_climate_data(selected_id)
            temp = st.number_input("Nova Temperatura", value=registro["temperature"], format="%.2f")
            hum = st.number_input("Nova Umidade", value=registro["air_humidity"], format="%.2f")
            rain = st.checkbox("Chuva prevista", value=registro["rain_forecast"])
            if st.button("Atualizar"):
                update_climate_data(selected_id, {"temperature": temp, "air_humidity": hum, "rain_forecast": rain})
                st.success("Atualizado com sucesso!")
                st.rerun()
            if st.button("Deletar"):
                delete_climate_data(selected_id)
                st.success("Removido com sucesso!")
                st.rerun()

# ---------------------- SENSOR RECORDS -------------------------
elif aba == "Registros de Sensores":
    st.header("🧪 Registros dos Sensores")
    df = pd.DataFrame(list_sensor_records())

    if df.empty:
        st.info("Nenhum registro de sensor disponível.")
    else:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        st.dataframe(df, use_container_width=True)

        with st.expander("Visualização de Nutrientes e Irrigação"):
            fig_nutri, ax_nutri = plt.subplots()
            df['phosphorus_present'] = df['phosphorus_present'].astype(bool)
            df['potassium_present'] = df['potassium_present'].astype(bool)
            nutrient_counts = pd.DataFrame({
                "Fósforo": df['phosphorus_present'].value_counts(),
                "Potássio": df['potassium_present'].value_counts()
            })
            nutrient_counts.plot(kind='bar', ax=ax_nutri, color=['purple', 'green'])
            ax_nutri.set_title("Presença de Nutrientes (P e K)")
            ax_nutri.set_xlabel("Presença")
            ax_nutri.set_ylabel("Quantidade")
            st.pyplot(fig_nutri)

            fig_irrig, ax_irrig = plt.subplots()
            df_sorted = df.sort_values(by="timestamp")
            df_sorted['status_numeric'] = df_sorted['irrigation_status'].apply(lambda x: 1 if x == "ATIVADA" else 0)
            ax_irrig.step(df_sorted["timestamp"], df_sorted['status_numeric'], where='post')
            ax_irrig.set_yticks([0, 1])
            ax_irrig.set_yticklabels(["DESLIGADA", "ATIVADA"])
            ax_irrig.set_title("Status da Irrigação ao Longo do Tempo")
            ax_irrig.set_xlabel("Data/Hora")
            ax_irrig.set_ylabel("Status")
            ax_irrig.grid(True)
            st.pyplot(fig_irrig)

    with st.expander("Novo registro de sensor"):
        umidade = st.number_input("Umidade do solo", format="%.2f")
        phos = st.checkbox("Fósforo presente")
        pot = st.checkbox("Potássio presente")
        ph = st.number_input("pH do solo", format="%.2f")
        status = st.selectbox("Status da irrigação", ["ATIVADA", "DESLIGADA"])
        if st.button("Cadastrar sensor"):
            create_sensor_record({
                "soil_moisture": umidade,
                "phosphorus_present": phos,
                "potassium_present": pot,
                "soil_ph": ph,
                "irrigation_status": status,
                "timestamp": datetime()
            })
            st.success("Sensor cadastrado!")
            st.rerun()

    with st.expander("Editar ou remover registro existente"):
        df = pd.DataFrame(list_sensor_records())

        if df.empty:
            st.info("Nenhum registro disponível.")
        else:
            df["id_str"] = df["id"].astype(str)
            selected_id = st.selectbox("Selecione o ID do registro", df["id_str"])
            selected_row = df[df["id_str"] == selected_id].iloc[0]

            new_umidade = st.number_input("Umidade do solo", value=selected_row["soil_moisture"], format="%.2f")
            new_phos = st.checkbox("Fósforo presente", value=selected_row["phosphorus_present"])
            new_pot = st.checkbox("Potássio presente", value=selected_row["potassium_present"])
            new_ph = st.number_input("pH do solo", value=selected_row["soil_ph"], format="%.2f")
            new_status = st.selectbox(
                "Status da irrigação",
                ["ATIVADA", "DESLIGADA"],
                index=0 if selected_row["irrigation_status"] == "ATIVADA" else 1,
                key=f"status_select_{selected_id}"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Atualizar registro"):
                    update_sensor_record(selected_row["id"], {
                        "soil_moisture": new_umidade,
                        "phosphorus_present": new_phos,
                        "potassium_present": new_pot,
                        "soil_ph": new_ph,
                        "irrigation_status": new_status,
                        "timestamp": datetime.now().isoformat()
                    })
                    st.success("Registro atualizado!")
                    st.rerun()

            with col2:
                if st.button("❌ Remover este registro"):
                    delete_sensor_record(selected_row["id"])
                    st.warning("Registro removido com sucesso!")
                    st.rerun()

# ---------------------- COMPONENTS -------------------------
elif aba == "Componentes":
    st.header("🔧 Componentes")
    df = pd.DataFrame(list_components())
    if df.empty:
        st.info("Nenhum componente disponível.")
    else:
        st.dataframe(df, use_container_width=True)

    with st.expander("Novo componente"):
        name = st.text_input("Nome do componente")
        type_ = st.selectbox("Tipo", ["Sensor", "Actuator"])
        if st.button("Cadastrar Componente"):
            create_component({"name": name, "type": type_})
            st.success("Componente criado!")
            st.rerun()

    with st.expander("Editar ou remover componente"):
        componentes = list_components()
        ids = [r["id"] for r in componentes if r is not None]

        if not ids:
            st.info("Nenhum componente disponível.")
        else:
            selected_id = st.selectbox("Selecione o componente:", ids)

            if selected_id:
                comp = get_component(selected_id)

                if comp is None:
                    st.error("Componente não encontrado.")
                else:
                    new_name = st.text_input("Novo nome", value=comp.get("name", ""))
                    new_type = st.selectbox(
                        "Novo tipo",
                        ["Sensor", "Actuator"],
                        index=0 if comp.get("type") == "Sensor" else 1
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Atualizar componente"):
                            update_component(selected_id, {"name": new_name, "type": new_type})
                            st.success("Atualizado!")
                            st.rerun()

                    with col2:
                        if st.button("Deletar componente"):
                            delete_component(selected_id)
                            st.success("Removido!")
                            st.rerun()