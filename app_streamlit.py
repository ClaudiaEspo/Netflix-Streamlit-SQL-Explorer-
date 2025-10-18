import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os
# ==========================
# Step 1: Percorsi file
# ==========================
csv_path = r"C:\Users\espoc\Desktop\script\sql\netflix_titles.csv"
db_path = r"C:\Users\espoc\Desktop\script\sql\netflix.db"

# ==========================
# Step 2: Crea il database SQLite se non esiste
# ==========================
if not os.path.exists(db_path):
    st.write("Creazione database SQLite da CSV...")
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql("netflix", conn, if_exists="replace", index=False)
    conn.close()
    st.success("Database creato con successo!")

# ==========================
# Step 3: Connessione al database
# ==========================
conn = sqlite3.connect(db_path)

st.title("Netflix Data Explorer 🎬")

# ==========================
# Sidebar: filtri interattivi
# ==========================
# Lista paesi e tipi
countries = ["All"] + list(pd.read_sql_query("SELECT DISTINCT country FROM netflix WHERE country IS NOT NULL", conn)['country'])
types = ["All"] + list(pd.read_sql_query("SELECT DISTINCT type FROM netflix WHERE type IS NOT NULL", conn)['type'])

# Sidebar Streamlit
selected_country = st.sidebar.selectbox("Seleziona Paese", countries)
selected_type = st.sidebar.selectbox("Seleziona Tipo", types)

# Filtra generi (listed_in)
all_genres = pd.read_sql_query("SELECT listed_in FROM netflix", conn)
genres_set = set()
for g in all_genres['listed_in'].dropna():
    for genre in g.split(', '):
        genres_set.add(genre)
genres = ["All"] + sorted(list(genres_set))
selected_genre = st.sidebar.selectbox("Seleziona Genere", genres)

# ==========================
# Costruzione query dinamica
# ==========================
query = "SELECT show_id, title, type, country, release_year, rating, listed_in FROM netflix WHERE 1=1"

if selected_country != "All":
    query += f" AND country='{selected_country}'"
if selected_type != "All":
    query += f" AND type='{selected_type}'"
if selected_genre != "All":
    query += f" AND listed_in LIKE '%{selected_genre}%'"

query += " LIMIT 1000"  # Limite per non appesantire la tabella

df = pd.read_sql_query(query, conn)

st.subheader("Tabella Filtrata")
st.dataframe(df)

# ==========================
# Grafico: conteggio titoli per tipo
# ==========================
st.subheader("Conteggio Titoli per Tipo")
if not df.empty:
    type_count = df['type'].value_counts()
    st.bar_chart(type_count)
else:
    st.write("Nessun dato da mostrare")

# ==========================
# Grafico: distribuzione per anno di rilascio
# ==========================
st.subheader("Distribuzione Anni di Rilascio")
if not df.empty:
    year_counts = df['release_year'].value_counts().sort_index()
    st.line_chart(year_counts)

# ==========================
# Esecuzione query SQL diretta
# ==========================
st.subheader("Esegui la tua query SQL")
user_query = st.text_area("Scrivi qui la query SQL", "SELECT title, type, country, release_year FROM netflix LIMIT 10")

if st.button("Esegui Query"):
    try:
        result = pd.read_sql_query(user_query, conn)
        st.dataframe(result)
    except Exception as e:
        st.error(f"Errore nella query: {e}")

# ==========================
# Chiusura connessione
# ==========================
conn.close()
