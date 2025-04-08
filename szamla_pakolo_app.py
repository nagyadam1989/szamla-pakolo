
import streamlit as st
import pandas as pd
import io

# Jelszóvédelem
st.set_page_config(page_title="Jelszavas Számlaösszekötő", layout="centered")
st.title("🔐 Számlák és tranzakciók összekapcsolása")

# Egyszerű jelszavas belépés
password = st.text_input("Add meg a jelszót a belépéshez:", type="password")
if password != "szamla123":
    st.warning("Kérlek, add meg a helyes jelszót.")
    st.stop()

# Fájlok feltöltése
st.success("✅ Hozzáférés engedélyezve. Töltsd fel a fájlokat.")

excel_file = st.file_uploader("Excel fájl (.xlsx)", type=["xlsx"])
csv_file = st.file_uploader("CSV fájl (.csv)", type=["csv"])

if excel_file and csv_file:
    try:
        excel_df = pd.read_excel(excel_file)
        csv_df = pd.read_csv(csv_file)

        merged_df = pd.merge(
            csv_df,
            excel_df[['Számlaszám', 'Vevő']],
            left_on='Details',
            right_on='Vevő',
            how='left'
        )

        st.success("✅ Fájlok összekapcsolva!")
        st.dataframe(merged_df.head())

        # Letöltés
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            merged_df.to_excel(writer, index=False)
        output.seek(0)

        st.download_button(
            label="⬇️ Letöltés Excel fájlként",
            data=output,
            file_name="osszekapcsolt_adatok.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"Hiba történt: {e}")
else:
    st.info("📁 Kérlek, töltsd fel mindkét fájlt.")
