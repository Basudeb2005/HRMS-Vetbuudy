import streamlit as st
import pandas as pd
import datetime

# Path for CSV files
ANNOUNCEMENTS_FILE = 'announcements.csv'
ACHIEVEMENTS_FILE = 'achievements.csv'
MILESTONES_FILE = 'milestones.csv'

# Function to display announcements in a more user-friendly format
def display_anno():
    st.title("📢 Announcements")

    # Load announcements data
    announcements_df = load_data(ANNOUNCEMENTS_FILE, ['Date', 'Announcement'])

    if announcements_df.empty:
        st.write("No announcements available.")
    else:
        # Display a calendar and list of announcements by date
        announcement_dates = pd.to_datetime(announcements_df['Date']).dt.date.unique()

        st.markdown("### 📅 Announcement Dates")
        selected_date = st.date_input("Select a date to view announcements", min_value=min(announcement_dates), max_value=max(announcement_dates))

        # Filter announcements by the selected date
        filtered_announcements = announcements_df[announcements_df['Date'] == selected_date.strftime('%Y-%m-%d')]

        if not filtered_announcements.empty:
            st.markdown(f"### Announcements for {selected_date.strftime('%Y-%m-%d')}")
            for idx, row in filtered_announcements.iterrows():
                st.markdown(f"**🗓 {row['Date']}:** {row['Announcement']}")
        else:
            st.write("No announcements on this date.")

# Function to display achievements in a more user-friendly format
def display_achv():
    st.title("🏆 Team Achievements")

    # Load achievements data
    achievements_df = load_data(ACHIEVEMENTS_FILE, ['Employee', 'Achievement', 'Date'])

    if achievements_df.empty:
        st.write("No achievements yet.")
    else:
        st.markdown("### 🎉 Recent Achievements")
        
        # Display achievements in a card-like format
        for idx, row in achievements_df.iterrows():
            st.markdown(f"""
            <div style="border: 2px solid #4CAF50; padding: 10px; margin: 10px 0; border-radius: 10px;">
                <strong>🏅 {row['Employee']}</strong><br>
                <em>{row['Achievement']}</em><br>
                <small>📅 {row['Date']}</small>
            </div>
            """, unsafe_allow_html=True)

# Function to display milestones in a more user-friendly format
def display_milestones():
    st.title("🚀 Company Milestones")

    # Load milestones data
    milestones_df = load_data(MILESTONES_FILE, ['Milestone', 'Date'])

    if milestones_df.empty:
        st.write("No milestones achieved yet.")
    else:
        st.markdown("### 🌟 Key Milestones")

        # Create a timeline-like format for milestones
        for idx, row in milestones_df.iterrows():
            st.markdown(f"""
            <div style="border-left: 4px solid #4CAF50; padding-left: 10px; margin: 10px 0;">
                <strong>📅 {row['Date']}</strong><br>
                <em>{row['Milestone']}</em>
            </div>
            """, unsafe_allow_html=True)

# Helper function to load data
def load_data(file_path, columns):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=columns)