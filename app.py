"""
Application Streamlit - Formateur SQL.

Permet de coller du code SQL ou de charger un fichier .sql, de le corriger
automatiquement selon les normes de l'equipe (sqlfluff + .sqlfluff), et de
telecharger / copier le resultat.
"""

from pathlib import Path

import streamlit as st

from sql_format_agent import CONFIG_PATH, format_sql, lint_sql

st.set_page_config(page_title="Formateur SQL", page_icon="🛠️", layout="wide")

st.title("🛠️ Formateur SQL")
st.caption("Corrige automatiquement ton code SQL selon les normes de l'equipe (sqlfluff).")

# --- Entree du code SQL -----------------------------------------------------
uploaded_file = st.file_uploader("Charger un fichier .sql", type=["sql"])

if uploaded_file is not None:
    default_sql = uploaded_file.read().decode("utf-8")
else:
    default_sql = ""

sql_input = st.text_area(
    "Ou colle ton code SQL ici",
    value=default_sql,
    height=300,
    placeholder="select * from ma_table where id=1",
)

col1, col2 = st.columns(2)
with col1:
    run = st.button("✅ Corriger le script", type="primary", use_container_width=True)
with col2:
    show_violations = st.checkbox("Afficher les violations restantes", value=False)

# --- Traitement --------------------------------------------------------------
if run:
    if not sql_input.strip():
        st.warning("Colle ou charge un script SQL avant de lancer la correction.")
    else:
        with st.spinner("Correction en cours..."):
            try:
                fixed_sql = format_sql(sql_input)
            except Exception as exc:  # erreur sqlfluff (ex: SQL invalide)
                st.error(f"Erreur lors du formatage : {exc}")
            else:
                st.subheader("Résultat formaté")
                st.code(fixed_sql, language="sql")

                st.download_button(
                    label="📥 Télécharger le script corrigé",
                    data=fixed_sql,
                    file_name="script_corrige.sql",
                    mime="text/sql",
                    use_container_width=True,
                )

                if fixed_sql == sql_input:
                    st.success("Le script était déjà conforme aux normes.")
                else:
                    st.success("Le script a été reformaté.")

                if show_violations:
                    violations = lint_sql(fixed_sql)
                    st.subheader("Violations restantes")
                    if violations:
                        st.table(violations)
                    else:
                        st.info("Aucune violation restante.")

st.divider()
with st.expander("ℹ️ Règles appliquées (.sqlfluff)"):
    st.code(Path(CONFIG_PATH).read_text(encoding="utf-8"), language="ini")
