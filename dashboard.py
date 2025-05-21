import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "tracker.db"

st.set_page_config(page_title="Job Application Tracker", layout="wide")

# Load applications from SQLite
@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM applications", conn)
    conn.close()
    return df

df = load_data()

st.title("🎯 AI Job Application Tracker")
st.write(f"Total Applications: {len(df)}")
# Status distribution chart (if status exists)
if 'status' in df.columns:
    st.subheader("📊 Application Status Breakdown")
    status_counts = df['status'].value_counts()
    st.bar_chart(status_counts)

    st.subheader("📈 Application Outcome Pie Chart")
    st.write(status_counts)
    st.pyplot(status_counts.plot.pie(autopct='%1.1f%%', figsize=(5, 5)).get_figure())


# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    status_options = st.multiselect("Status", df['status'].dropna().unique().tolist(), default=df['status'].dropna().unique().tolist() if 'status' in df.columns else [])

# Optional: Filter by status
if 'status' in df.columns and status_options:
    df = df[df['status'].isin(status_options)]

# Display table
st.dataframe(df, use_container_width=True)

# Export button
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV", data=csv, file_name="applications_log.csv", mime="text/csv")

# Status update form (optional)
if st.checkbox("✍️ Update Application Status"):
    app_id = st.number_input("Application ID", min_value=1)
    new_status = st.text_input("New Status (e.g., submitted, interview, rejected, offer)")
    feedback = st.text_input("Feedback/Note")

    if st.button("Update"):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE applications SET status = ?, feedback = ? WHERE id = ?", (new_status, feedback, app_id))
        conn.commit()
        conn.close()
        st.success("✅ Application updated!")
        st.experimental_rerun()
