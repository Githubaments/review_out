import streamlit as st
import gspread
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from google.oauth2 import service_account



# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive", ],
)

gc = gspread.authorize(credentials)

# Open the Google Sheet by name

sheet = gc.open_by_key('1_doOck1fbnoIsvnVKjYLNWxcnDwk2IWpcXqyp4yuBPI').get_worksheet(1)

# Get data from column A (metrics) and column B (questions)
metrics_column = sheet.col_values(1)  # Assumes metrics are in column A
questions_column = sheet.col_values(2)  # Assumes questions are in column B

# Create Dataframe
data = {
    'Metrics': metrics_column,
    'Questions': questions_column
}

df

df = pd.DataFrame(data)

def main():
    st.title("End of Day Review")

    # List of metrics and questions
    metrics = df['Metrics'].tolist()
    questions = df['Questions'].tolist()

    # Dictionary to store scores for each metric
    scores = {}

    # Loop through each metric and create a radio button selection for scores 1-5
    for metric, question in zip(metrics, questions):
        score = st.radio(f"{question}", [1, 2, 3, 4, 5], horizontal=True)
        scores[metric] = score

    # Text input for Aspiration, Improvement, Realisation, and Gratitude
    results = st.text_area("What are your results today?")
    ideas = st.text_area("What are your ideas for tomorrow?")
    goals = st.text_area("What are your goals for next week")
    aspiration = st.text_area("What are your aspirations for the future?")
    improvement = st.text_area("What could you have improved today?")
    realisation = st.text_area("What did you realize today?")
    gratitude = st.text_area("What are you grateful for today?")
    compliments_given = st.text_area("Compliments received?")
    compliments_received = st.text_area("Compliments given?")

    # Creating a dictionary with data
    data = {
        'Date': datetime.now().strftime('%Y-%m-%d'),  # Putting date first
        **scores,  # Unpacking the scores dictionary
        'Results': results,
        'Ideas': ideas,
        'Goals': goals,
        'Aspiration': aspiration,
        'Improvement': improvement,
        'Realisation': realisation,
        'Gratitude': gratitude,
        'Compliments Given': compliments_given,
        'Compliments Received': compliments_received
    }

    df = pd.DataFrame([data], columns=data.keys())  # Creating a single-row dataframe from the data

    # Display the DataFrame on the Streamlit app
    st.write(df)

    with st.form(key='my_form'):
        if st.form_submit_button(label="Submit"):
            try:
    
                # Get the number of rows that have data
                num_rows = len(sheet.get_all_values())
    
                # Calculate the starting cell for new data (considering the header is only added once)
                start_cell = f"A{num_rows + 1}" if num_rows > 0 else "A1"
    
                # Append the data
                if num_rows == 0:
                    # If the sheet is empty, also include the headers
                    sheet.update(start_cell, [df.columns.values.tolist()] + df.values.tolist())
                else:
                    # Otherwise, just append the data rows
                    sheet.update(start_cell, df.values.tolist())
    
                    st.write(f"New data written to sheet")
    
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()






