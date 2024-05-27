import streamlit as st
import plotly.express as px
import pandas as pd
from custom_css import local_css

# set config page
st.set_page_config(page_title="Smart Sense", page_icon=":partly_sunny:", layout="wide")

st.title(":partly_sunny: Smart Sense Weather Data Analysis")


# Load local CSS file
local_css("style.css")

# set the tabs
tab1, tab2 = st.tabs(["About Us", "Data Visualization"])

# Set tab 1
with tab1:
    # Read the markdown content from "about_us.md" file
    with open("about_us.md", "r") as file:
        about_us_content = file.read()
    st.markdown(about_us_content)

# Set tab 2
with tab2:


    st.subheader("Weather Data Visualization")
    # Load data
    @st.cache_data
    def load_data():
        url = "http://3.120.134.165/boxes/clima01.csv"
        # Read CSV file, considering line 1 as header and skipping rows until line 2
        df = pd.read_csv(url, skiprows=1, names=['UTC_server_time', 'ID', 'UTC_box_time', 'windspeed1', 'windspeed2', 'winddir', 
                                                  'rain', 'radsolar', 'soilhum', 'soiltemp', 'airtemp1', 'airpress', 'airhum1', 
                                                  'airtemp2', 'airhum2', 'line_number'])
        # Convert 'UTC_server_time' and 'UTC_box_time' columns to datetime
        df['UTC_server_time'] = pd.to_datetime(df['UTC_server_time'])
        df['UTC_box_time'] = pd.to_datetime(df['UTC_box_time'])
        # Filter data from February 7th onwards
        df = df[df['UTC_server_time'] >= '2024-02-07']
        return df

    # Load data
    df = load_data()

    # Select variables to plot
    selected_variables = st.multiselect("Select variables to plot:", df.columns)

    # Check if selected_variables is not empty
    if selected_variables:
        # Group by variable if more than one selected
        if len(selected_variables) > 1:
            groupby_variable = st.selectbox("Group by variable:", df.columns)

            # Create plot
            fig = px.line(df, x='UTC_server_time', y=selected_variables, title="Weather Parameters over Time", color=groupby_variable)

            # Update Y axis labels with units
            for var in selected_variables:
                fig.update_yaxes(title_text=f"{var} (units)")

        else:
            # Create plot
            fig = px.line(df, x='UTC_server_time', y=selected_variables[0], title=f"{selected_variables[0]} over Time")

            # Update Y axis label with unit
            fig.update_yaxes(title_text=f"{selected_variables[0]} (units)")

        # Display plot
        st.plotly_chart(fig)
    else:
        st.warning("Please select at least one variable to plot.")


     # Show the most updated values of soilhum, soiltemp, and radsolar in styled boxes
    
    soilhum = df["soilhum"].iloc[-1]
    soiltemp = df["soiltemp"].iloc[-1]
    radsolar = df["radsolar"].iloc[-1]

    # Calculate delta values
    delta_soilhum = df["soilhum"].diff().iloc[-1]  # Calculate difference between current and previous soil humidity
    delta_soiltemp = df["soiltemp"].diff().iloc[-1]
    delta_radsolar = df["radsolar"].diff().iloc[-1]   

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Soil Humidity (%):", soilhum, delta_soilhum)
    col2.metric("Soil Temperature (°C):",soiltemp, delta_soiltemp)
    col3.metric("Radiation solar (J):", radsolar, delta_radsolar)
    