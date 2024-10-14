import pandas as pd
from datetime import datetime
file_path = 'tasks.csv'

# Load tasks from CSV
def load_tasks(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Team Member', 'Task', 'Status'])

# Save tasks to CSV
def save_tasks(df, file_path):
    df.to_csv(file_path, index=False)

# Assign new task
def assign_task(df, team_member, task):
    new_task = {
        'Date': datetime.now().strftime('%Y-%m-%d'),
        'Team Member': team_member,
        'Task': task,
        'Status': 'Pending'
    }
    return df.append(new_task, ignore_index=True)

# Update task status
def update_task_status(df, team_member, status):
    df.loc[df['Team Member'] == team_member, 'Status'] = status
    return df