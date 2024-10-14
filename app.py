import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Paths for CSV files to store tasks, goals, and announcements
TASKS_FILE = 'tasks.csv'
GOALS_FILE = 'team_goals.csv'
ANNOUNCEMENTS_FILE = 'announcements.csv'
WORK_UPLOAD_FOLDER = 'uploads/'

# Create upload folder if not exists
if not os.path.exists(WORK_UPLOAD_FOLDER):
    os.makedirs(WORK_UPLOAD_FOLDER)

# Logo for VetBuddy
logo = "vetbuddy_logo.png"

# Function to load data from CSV file
def load_data(file_path, columns):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=columns)

# Function to save data to CSV file
def save_data(df, file_path):
    df.to_csv(file_path, index=False)

# Function to assign new tasks
def assign_task(df, team_member, task, date):
    new_task = pd.DataFrame({
        'Date': [date.strftime('%Y-%m-%d')],
        'Team Member': [team_member],
        'Task': [task],
        'Status': ['Pending'],
        'Comments': ['']
    })
    df = pd.concat([df, new_task], ignore_index=True)
    return df

# Function to update task status
def update_task_status(df, team_member, status, date):
    df.loc[(df['Team Member'] == team_member) & (df['Date'] == date.strftime('%Y-%m-%d')), 'Status'] = status
    return df

# Function to delete tasks
def delete_task(df, index):
    df = df.drop(index)
    return df

# Function to check if task exists for comment
def check_task_exists(df, username, date):
    return (df['Team Member'] == username) & (df['Date'] == date.strftime('%Y-%m-%d'))

# Function to show the login page
def show_login_page():
    # Center the content manually using Streamlit's layout options
    st.markdown("<h1 style='text-align: center;'>🐾 Welcome to VetBuddy! 🐾</h1>", unsafe_allow_html=True)
    left_co, cent_co, right_co = st.columns(3)
    with cent_co:
        st.image(logo, use_column_width=True)  # Centered logo using columns
    st.markdown("<h3 style='text-align: center;'>Smarter AI 💡, Healthier Pets 🐾, Happier Vets 😊</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>🔑 Login to Continue</h4>", unsafe_allow_html=True)

# Load task and goal data
task_df = load_data(TASKS_FILE, ['Date', 'Team Member', 'Task', 'Status', 'Comments'])
goals_df = load_data(GOALS_FILE, ['Week Start Date', 'Daily Goal', 'Week Plan'])
announcements_df = load_data(ANNOUNCEMENTS_FILE, ['Date', 'Announcement'])

# Display login page and logo
show_login_page()

# Admin or user login
panel = st.sidebar.radio("Select Panel", ["Admin Panel", "Employee Panel"])

if panel == "Admin Panel":
    password = st.text_input("Enter admin password", type="password")
    if password == "adminpassword":
        st.success("Logged in as Admin 👨‍💼")

        # Quick entry system for weekly and daily goals
        st.subheader("Quick Entry for Weekly and Daily Goals 📝")
        quick_entry = st.text_area("Enter goals (Format: Week Start Date; Daily Goal; Week Plan)", placeholder="2024-10-14; Exercise daily; Week Plan for team...")
        if st.button("Add Goals"):
            try:
                week_start, daily_goal, week_plan = quick_entry.split(";")
                new_goal = pd.DataFrame({
                    'Week Start Date': [week_start.strip()],
                    'Daily Goal': [daily_goal.strip()],
                    'Week Plan': [week_plan.strip()]
                })
                goals_df = pd.concat([goals_df, new_goal], ignore_index=True)
                save_data(goals_df, GOALS_FILE)
                st.success(f"Goals for {week_start.strip()} added successfully")
            except:
                st.error("Please enter the goals in the correct format.")

        # Admin can assign tasks
        st.subheader("Assign Tasks to Team Members 📋")
        team_member = st.selectbox("Select Team Member", ['Akshat Srivastava', 'Rishika', 'Annika', 'Akshat Juneja'])
        task_desc = st.text_area("Task Description")
        task_date = st.date_input("Select Task Date", datetime.today())

        if st.button("Assign Task"):
            task_df = assign_task(task_df, team_member, task_desc, task_date)
            save_data(task_df, TASKS_FILE)
            st.success(f"Task assigned to {team_member} for {task_date.strftime('%Y-%m-%d')} ✅")

        # Display tasks with delete option
        st.subheader("All Assigned Tasks 📝")
        if not task_df.empty:
            for idx, row in task_df.iterrows():
                st.write(f"**{row['Team Member']}** - {row['Task']} (Date: {row['Date']})")
                if st.button(f"Delete Task {idx}", key=idx):
                    task_df = delete_task(task_df, idx)
                    save_data(task_df, TASKS_FILE)
                    st.success(f"Task {idx} deleted successfully")

        # Announcements Section
        st.subheader("Post Announcements 📢")
        announcement = st.text_area("Write Announcement")
        upload_choice = st.radio("Preferred Option to Upload", ["Link (Preferred)", "None"])

        if upload_choice == "Link (Preferred)":
            link = st.text_input("Add the Link")
            if st.button("Post Announcement"):
                new_announcement = pd.DataFrame({
                    'Date': [datetime.now().strftime('%Y-%m-%d')],
                    'Announcement': [f"{announcement} - Link: {link}"]
                })
                announcements_df = pd.concat([announcements_df, new_announcement], ignore_index=True)
                save_data(announcements_df, ANNOUNCEMENTS_FILE)
                st.success("Announcement posted with link! 📣")
        else:
            if st.button("Post Announcement"):
                new_announcement = pd.DataFrame({
                    'Date': [datetime.now().strftime('%Y-%m-%d')],
                    'Announcement': [announcement]
                })
                announcements_df = pd.concat([announcements_df, new_announcement], ignore_index=True)
                save_data(announcements_df, ANNOUNCEMENTS_FILE)
                st.success("Announcement posted! 📣")

        # Display announcements
        st.subheader("All Announcements 📢")
        if not announcements_df.empty:
            st.dataframe(announcements_df)

elif panel == "Employee Panel":
    st.info("Employee Panel 👩‍💼👨‍💻")
    username = st.selectbox("Select your name", ['Akshat Srivastava', 'Rishika', 'Annika', 'Akshat Juneja'])
    
    # View and update tasks
    selected_date = st.date_input("Select Date to View Tasks", datetime.today())
    user_tasks = task_df[(task_df['Team Member'] == username) & (task_df['Date'] == selected_date.strftime('%Y-%m-%d'))]
    
    st.subheader(f"Tasks for {username} on {selected_date.strftime('%Y-%m-%d')} 📅")
    if not user_tasks.empty:
        st.dataframe(user_tasks)
        task_status = st.selectbox("Update Task Status", ['Pending', 'In Progress', 'Completed'])
        if st.button("Update Status"):
            task_df = update_task_status(task_df, username, task_status, selected_date)
            save_data(task_df, TASKS_FILE)
            st.success("Task status updated successfully")
    else:
        st.write(f"No tasks assigned for {selected_date.strftime('%Y-%m-%d')}")

    # Add comments
    st.subheader("Add Additional Comments 📝")
    comment = st.text_area("Leave a comment for the task")
    if st.button("Submit Comment"):
        task_exists = check_task_exists(task_df, username, selected_date)
        if task_exists.any():
            task_df.loc[task_exists, 'Comments'] = comment
            save_data(task_df, TASKS_FILE)
            st.success("Comment added successfully!")
        else:
            st.error("No task found for this date. Cannot add a comment.")