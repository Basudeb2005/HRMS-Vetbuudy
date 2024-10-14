import streamlit as st
import pandas as pd
from datetime import datetime
import os
from alldis import display_anno, display_achv, display_milestones  # Import the display functions

# Paths for CSV files
TASKS_FILE = 'tasks.csv'
GOALS_FILE = 'team_goals.csv'
ANNOUNCEMENTS_FILE = 'announcements.csv'
ACHIEVEMENTS_FILE = 'achievements.csv'
MILESTONES_FILE = 'milestones.csv'
TEAM_MEMBERS_FILE = 'team_members.csv'
WORK_UPLOAD_FOLDER = 'uploads/'

# Ensure COMMENTS_FILE is loaded correctly with the required columns
# Define file paths
COMMENTS_FILE = 'comments.csv'

# Define a function to load data from CSV
def load_data(file_path, columns):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=columns)

# Define a function to save data to CSV
def save_data(df, file_path):
    df.to_csv(file_path, index=False)

# Load the comments CSV with required columns
comment_df = load_data(COMMENTS_FILE, ['Date', 'Team Member', 'Task', 'Comment'])

# Load the task CSV
task_df = load_data(TASKS_FILE, ['Date', 'Team Member', 'Task', 'Status', 'Comments'])
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

# Function to delete tasks by serial number and date
def delete_task(df, serial_number):
    if serial_number in df.index:
        df = df.drop(serial_number)
        df.reset_index(drop=True, inplace=True)  # Reset the index after deletion
    return df

# Display login page and logo
def show_login_page():
    st.markdown("<h1 style='text-align: center;'>🐾 Welcome to VetBuddy! 🐾</h1>", unsafe_allow_html=True)
    left_co, cent_co, right_co = st.columns(3)
    with cent_co:
        st.image(logo, use_column_width=True)  # Centered logo using columns
    st.markdown("<h3 style='text-align: center;'>Smarter AI 💡, Healthier Pets 🐾, Happier Vets 😊</h3>", unsafe_allow_html=True)
   

# Main app logic
def main():
    # Load necessary data
    global team_members_df
    team_members_df = load_data(TEAM_MEMBERS_FILE, ['Team Member', 'Position'])
    task_df = load_data(TASKS_FILE, ['Date', 'Team Member', 'Task', 'Status', 'Comments'])
    
    # Show login page
    show_login_page()

    # Admin or user login
    panel = st.sidebar.radio("Select Panel", ["🛠️ Admin Dashboard", "👩‍💼 Team Panel", "📢 Announcements", "🏆 Achievements", "🚀 Company Milestones"])

    if panel == "🛠️ Admin Dashboard":
        password = st.text_input("Enter admin password", type="password")
        if password == "adminpass":
            st.success("Logged in as Admin 👨‍💼")

            # Add/Delete Team Members
            st.subheader("Manage Team Members 🧑‍🤝‍🧑")
            member_action = st.radio("Choose Action", ["Add Team Member", "Delete Team Member"])
            if member_action == "Add Team Member":
                new_member = st.text_input("Enter Team Member's Name")
                new_position = st.text_input("Enter Position (Optional)", placeholder="e.g. Developer")
                if st.button("Add Member"):
                    new_entry = pd.DataFrame({
                        'Team Member': [new_member],
                        'Position': [new_position if new_position else 'No Position']
                    })
                    team_members_df = pd.concat([team_members_df, new_entry], ignore_index=True)
                    save_data(team_members_df, TEAM_MEMBERS_FILE)
                    st.success(f"Team member {new_member} added successfully.")
            elif member_action == "Delete Team Member":
                del_member = st.selectbox("Select Member to Delete", team_members_df['Team Member'].unique())
                if st.button("Delete Member"):
                    team_members_df = team_members_df[team_members_df['Team Member'] != del_member]
                    save_data(team_members_df, TEAM_MEMBERS_FILE)
                    st.success(f"Team member {del_member} deleted successfully.")
            # Quick entry system for weekly and daily goals
            st.subheader("Quick Entry for Weekly and Daily Goals 📝")
            quick_entry = st.text_area(
                "Enter goals (Format: Week Start Date; Daily Goal; Week Plan)", 
                placeholder="2024-10-14; Exercise daily; Week Plan for team...", 
                key="quick_entry_text_area"  # Assign unique key
            )

            if st.button("Add Goals", key="add_goals_button"):  # Assign unique key
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
            team_member = st.selectbox(
                "Select Team Member", team_members_df['Team Member'], key="assign_task_selectbox"  # Assign unique key
            )

            task_desc = st.text_area("Task Description", key="task_desc_text_area")  # Assign unique key
            task_date = st.date_input("Select Task Date", datetime.today(), key="task_date_input")  # Assign unique key

            if st.button("Assign Task", key="assign_task_button"):  # Assign unique key
                task_df = assign_task(task_df, team_member, task_desc, task_date)
                save_data(task_df, TASKS_FILE)
                st.success(f"Task assigned to {team_member} for {task_date.strftime('%Y-%m-%d')} ✅")

            # Display tasks for selected team member with serial numbers
            st.subheader(f"Tasks for {team_member}")
            filtered_tasks = task_df[task_df['Team Member'] == team_member].reset_index(drop=True)
            filtered_tasks['Serial Number'] = filtered_tasks.index + 1  # Add serial number for easier identification
            st.table(filtered_tasks[['Serial Number', 'Date', 'Task', 'Status']])

            # Deleting tasks by serial number
            st.subheader("Delete Task")
            if not filtered_tasks.empty:
                serial_number = st.number_input(
                    "Task Serial Number", min_value=1, max_value=len(filtered_tasks), step=1, key="delete_task_number_input"  # Assign unique key
                )
                if st.button("Delete Task", key="delete_task_button"):  # Assign unique key
                    task_df = delete_task(task_df, serial_number - 1)  # Subtract 1 because serial numbers start at 1
                    save_data(task_df, TASKS_FILE)
                    st.success(f"Task with serial number {serial_number} deleted successfully.")
            else:
                st.write("No tasks available to delete.")

            # Manage Announcements
            st.subheader("Manage Announcements 📢")
            new_announcement = st.text_area("Write Announcement")
            if st.button("Post Announcement"):
                new_announcement_df = pd.DataFrame({
                    'Date': [datetime.now().strftime('%Y-%m-%d')],
                    'Announcement': [new_announcement]
                })
                announcements_df = load_data(ANNOUNCEMENTS_FILE, ['Date', 'Announcement'])
                announcements_df = pd.concat([announcements_df, new_announcement_df], ignore_index=True)
                save_data(announcements_df, ANNOUNCEMENTS_FILE)
                st.success("Announcement posted successfully!")
            # In the "Manage Achievements" section, assign a unique key
            st.subheader("Manage Achievements 🏆")
            selected_member = st.selectbox("Select Team Member", team_members_df['Team Member'], key='achv_member_select')  # Unique key here
            achievement = st.text_area(f"Add Achievement for {selected_member}", key='achv_text_area')  # Also unique key for textarea
            if st.button(f"Add Achievement for {selected_member}", key='add_achv_button'):  # Unique key for button
                achievements_df = load_data(ACHIEVEMENTS_FILE, ['Employee', 'Achievement', 'Date'])
                new_achievement = pd.DataFrame({
                'Employee': [selected_member],
                'Achievement': [achievement],
                'Date': [datetime.now().strftime('%Y-%m-%d')]
                })
                achievements_df = pd.concat([achievements_df, new_achievement], ignore_index=True)
                save_data(achievements_df, ACHIEVEMENTS_FILE)
                st.success(f"Achievement added for {selected_member}!")

            

            # Manage Company Milestones
            st.subheader("Manage Company Milestones 🚀")
            milestone = st.text_area("Add New Milestone")
            if st.button("Add Milestone"):
                milestones_df = load_data(MILESTONES_FILE, ['Milestone', 'Date'])
                new_milestone = pd.DataFrame({
                    'Milestone': [milestone],
                    'Date': [datetime.now().strftime('%Y-%m-%d')]
                })
                milestones_df = pd.concat([milestones_df, new_milestone], ignore_index=True)
                save_data(milestones_df, MILESTONES_FILE)
                st.success("Milestone added successfully!")

    # The rest of the panel for the team to add and manage tasks and comments
    elif panel == "👩‍💼 Team Panel":
        # Load comments CSV
        comment_df = load_data(COMMENTS_FILE, ['Date', 'Team Member', 'Task', 'Comment'])

        st.info("Employee Panel 👩‍💼👨‍💻")
        username = st.selectbox("Select your name", team_members_df['Team Member'])
        
        # View tasks
        selected_date = st.date_input("Select Date to View Tasks", datetime.today())
        user_tasks = task_df[(task_df['Team Member'] == username) & (task_df['Date'] == selected_date.strftime('%Y-%m-%d'))]
        
        st.subheader(f"Tasks for {username} on {selected_date.strftime('%Y-%m-%d')} 📅")
        if not user_tasks.empty:
            # Display tasks in a table
            task_df_display = user_tasks[['Task', 'Status']].reset_index(drop=True)
            task_df_display.index += 1  # Add task numbers starting from 1
            st.table(task_df_display)
            
            # Let the user select a task number to add comments
            task_number = st.number_input("Select Task Number to Add Comment", min_value=1, max_value=len(user_tasks), step=1)
            selected_task = user_tasks.iloc[task_number - 1]  # Get the selected task

            # Display comments for the selected task
            st.subheader(f"Comments for Task {task_number} 📝")
            task_comments = comment_df[(comment_df['Team Member'] == username) & (comment_df['Task'] == selected_task['Task']) & (comment_df['Date'] == selected_task['Date'])]
            if not task_comments.empty:
                st.table(task_comments[['Comment']])
            else:
                st.write("No comments yet for this task.")
            
            # Add comment section for the selected task
            new_comment = st.text_area(f"Leave a new comment for Task {task_number}")
            if st.button(f"Submit New Comment for Task {task_number}"):
                new_comment_df = pd.DataFrame({
                    'Date': [selected_task['Date']],
                    'Team Member': [username],
                    'Task': [selected_task['Task']],
                    'Comment': [new_comment]
                })
                comment_df = pd.concat([comment_df, new_comment_df], ignore_index=True)
                save_data(comment_df, COMMENTS_FILE)
                st.success(f"New comment added for Task {task_number}!")
        else:
            st.write(f"No tasks assigned for {selected_date.strftime('%Y-%m-%d')}")
    elif panel == "📢 Announcements":
        display_anno()  # Call display function from alldis.py

    elif panel == "🏆 Achievements":
        display_achv()  # Call display function from alldis.py

    elif panel == "🚀 Company Milestones":
        display_milestones()  # Call display function from alldis.py

# Run the app
if __name__ == '__main__':
    main()