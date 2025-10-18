# Netflix Streamlit SQL Explorer 🎬

Un'applicazione web interattiva costruita con **Streamlit** per esplorare e visualizzare il dataset Netflix utilizzando **SQLite** e **Pandas**.

---

## 📋 Descrizione

Questo progetto permette di:
- Importare automaticamente il dataset Netflix da CSV a SQLite
- Filtrare i dati per paese, tipo e genere
- Visualizzare statistiche interattive con grafici
- Eseguire query SQL personalizzate
- Esplorare i contenuti Netflix in modo intuitivo

---

## 🛠️ Tecnologie utilizzate

- **Python 3.x**
- **Streamlit** - Framework per applicazioni web
- **Pandas** - Manipolazione dati
- **SQLite** - Database relazionale
- **Matplotlib** - Visualizzazioni grafiche

---

## 📦 Installazione

### 1. Clona il repository o scarica i file

```bash
git clone <url-repository>
cd netflix-streamlit-sql-explorer
```

### 2. Installa le dipendenze

```bash
pip install streamlit pandas matplotlib
```

### 3. Prepara il dataset

Scarica il file `netflix_titles.csv` da [Kaggle - Netflix Shows](https://www.kaggle.com/shivamb/netflix-shows) e posizionalo nella directory del progetto.

---

## 🚀 Come eseguire l'applicazione

```bash
streamlit run app.py
```

L'applicazione si aprirà automaticamente nel browser su `http://localhost:8501`

---

## ⚙️ Funzionalità principali

### 1️⃣ Creazione automatica del database

```python
if not os.path.exists(db_path):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql("netflix", conn, if_exists="replace", index=False)
```

- Se il database non esiste, viene creato automaticamente dal CSV
- I dati vengono importati nella tabella `netflix`

### 2️⃣ Filtri interattivi nella sidebar

L'applicazione offre tre filtri dinamici:

- **Paese**: filtra per paese di produzione
- **Tipo**: Movie o TV Show
- **Genere**: filtra per categorie (Drama, Comedy, Action, ecc.)

```python
selected_country = st.sidebar.selectbox("Seleziona Paese", countries)
selected_type = st.sidebar.selectbox("Seleziona Tipo", types)
selected_genre = st.sidebar.selectbox("Seleziona Genere", genres)
```

### 3️⃣ Query SQL dinamica

La query viene costruita dinamicamente in base ai filtri selezionati:

```python
query = "SELECT show_id, title, type, country, release_year, rating, listed_in FROM netflix WHERE 1=1"

if selected_country != "All":
    query += f" AND country='{selected_country}'"
if selected_type != "All":
    query += f" AND type='{selected_type}'"
if selected_genre != "All":
    query += f" AND listed_in LIKE '%{selected_genre}%'"
```

### 4️⃣ Tabella dati filtrati

```python
st.dataframe(df)
```

Mostra i risultati della query in una tabella interattiva e scorrevole.

### 5️⃣ Grafico: Conteggio per tipo

```python
type_count = df['type'].value_counts()
st.bar_chart(type_count)
```

Visualizza un grafico a barre che mostra la distribuzione tra Movie e TV Show.

### 6️⃣ Grafico: Distribuzione temporale

```python
year_counts = df['release_year'].value_counts().sort_index()
st.line_chart(year_counts)
```

Mostra un grafico a linee con la distribuzione dei contenuti per anno di rilascio.

### 7️⃣ Editor SQL personalizzato

```python
user_query = st.text_area("Scrivi qui la query SQL", 
                          "SELECT title, type, country, release_year FROM netflix LIMIT 10")

if st.button("Esegui Query"):
    result = pd.read_sql_query(user_query, conn)
    st.dataframe(result)
```

Permette agli utenti di eseguire query SQL personalizzate direttamente dall'interfaccia.

---

## 📁 Struttura del progetto

```
netflix-streamlit-sql-explorer/
│
├── app.py                  # File principale Streamlit
├── netflix_titles.csv      # Dataset Netflix (da scaricare)
├── netflix.db             # Database SQLite (generato automaticamente)
└── README.md              # Documentazione
```

---

## 🔧 Configurazione

Modifica i percorsi dei file nel codice se necessario:

```python
csv_path = r"C:\Users\espoc\Desktop\script\sql\netflix_titles.csv"
db_path = r"C:\Users\espoc\Desktop\script\sql\netflix.db"
```

---

## 📊 Esempi di query SQL personalizzate

### Trova i 10 film più recenti

```sql
SELECT title, release_year, country 
FROM netflix 
WHERE type='Movie' 
ORDER BY release_year DESC 
LIMIT 10
```

### Conta i contenuti per paese

```sql
SELECT country, COUNT(*) as total 
FROM netflix 
GROUP BY country 
ORDER BY total DESC 
LIMIT 10
```

### Film italiani degli ultimi 5 anni

```sql
SELECT title, release_year, rating 
FROM netflix 
WHERE country='Italy' AND type='Movie' AND release_year >= 2019
ORDER BY release_year DESC
```

---

## 🎯 Funzionalità future

- [ ] Export dei risultati in CSV/Excel
- [ ] Grafici più avanzati (distribuzione per rating, durata)
- [ ] Analisi sentiment delle descrizioni
- [ ] Ricerca full-text nei titoli e descrizioni
- [ ] Confronto tra paesi e generi

---

## 🐛 Troubleshooting

### Errore: "File not found"
Verifica che il percorso del CSV sia corretto e che il file esista.

### Errore nella query SQL
Controlla la sintassi SQL. Ricorda che SQLite ha alcune limitazioni rispetto ad altri database.

### L'app non si avvia
Assicurati di aver installato tutte le dipendenze:
```bash
pip install streamlit pandas matplotlib
```

---

## 📝 Licenza

Questo progetto è rilasciato sotto licenza MIT. Il dataset Netflix è proprietà di Kaggle/Netflix.

---

## 👨‍💻 Autore

Progetto didattico per imparare SQL, Streamlit e data visualization.
