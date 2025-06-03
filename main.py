import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import requests
import yfinance as yf
from textblob import TextBlob
#Title and Subheader
st.title("Life Expectancy By Country - By Florence")
st.write("Life Expectancy Data of India and USA from the year 1960 till 2016.")

# Multicolumn Support
col1, col2 = st.columns(2)
IN_flag = Image.open(r"IN.png") #path to IN.jpg
col1.header("INDIA")
col1.image(IN_flag, use_container_width=True)

US_flag = Image.open(r"US.png") # path to US.png
col2.header("USA")
col2.image(US_flag, use_container_width=True)

# reading a csv and displaying the first six rows on the screen.
df = pd.read_csv('lf.csv')
st.write(df.head())

# Display full data base on checkbox.
if st.checkbox('show full data'):
    df


# Dropdown to select a column
selected_column = st.selectbox("Select a column to check for missing data:", df.columns)

# Button to check for missing data
if st.button("Check Missing Data"):
    # Identify rows with missing values in the selected column
    missing_data = df[df[selected_column].isnull()]
    if missing_data.empty:
        st.write(f"No missing data found in column '{selected_column}'.")
    else:
        st.write(f"Rows with missing data in column '{selected_column}':")
        st.write(missing_data)

# Display barplot and data on search Input
_input = st.text_input("Enter Year to Search")
if _input:
    _df = df[df['year'] == int(_input)]
    if len(_df['year'])>0:
        _df
    if len(_df['year'])>0:
        sns.set_theme(style="whitegrid")
        fig, ax = plt.subplots()
        fig = plt.figure(figsize=(7, 4))
        ax = sns.barplot(data=_df, y="Lf-overall", x="year", hue="country", palette="tab20_r")
        st.pyplot(fig)
    else:
        st.write('Data Does Not Exist in the Database')




def analyze_sentiment(text):
    """Analyzes the sentiment of the given text."""
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

st.title("Simple Sentiment Analyzer")
st.write("Enter some text below and I'll tell you if it's positive, negative, or neutral!")

user_input = st.text_area("Enter your text here:")

if st.button("Analyze Sentiment"):
    if user_input:
        sentiment = analyze_sentiment(user_input)
        st.success(f"Sentiment: **{sentiment}**")
        st.info(f"Polarity: {TextBlob(user_input).sentiment.polarity:.2f} (ranges from -1.0 to 1.0)")
        st.info(f"Subjectivity: {TextBlob(user_input).sentiment.subjectivity:.2f} (ranges from 0.0 to 1.0)")
    else:
        st.warning("Please enter some text to analyze.")




# Sidebar Column
st.sidebar.title('Sidebar Widgets')

rating = st.sidebar.radio('Are You Happy with the Example',('Yes','No','Not Sure'))
if rating == 'Yes':
    st.sidebar.success('Thank You for Selecting Yes')
elif rating =='No':
    st.sidebar.info('Thank You for Selecting No')
elif rating =='Not Sure':
    st.sidebar.info('Thank You for Selecting Not sure')

rating = st.sidebar.selectbox("How much would you rate this App? ",
                     ['5 Stars', '4 Stars', '3 Stars','2 Stars','1 Star'])

st.sidebar.success(rating)

st.sidebar.write('Find Square of a Number')
get_number = st.sidebar.slider("Select a Number", 1, 10)
st.sidebar.write('Square of Number',get_number, 'is', get_number*get_number)

#
# displaying API data
API_URL = 'https://cleanuri.com/api/v1/shorten'
st.title("URL shortener")
_url = st.text_input('Enter URL')
pressed = st.button('Get Short Link')

if pressed:
    if _url !='':
        data = {'url': _url}
        r = requests.post(API_URL, data=data)
        st.write(r.json())
    else:
        st.write('Please enter the right URL first')


st.title("HK Stock analysis")        

user_input = st.text_input("Enter your stock symbol:")

if st.button("Get Analysis"):
    if user_input:
        try:
            # Fetch stock data using yfinance
            ticketData = yf.Ticker(user_input)
            tickerDf = ticketData.history(period="1y", start="2025-01-01", end="2025-4-30")

            # Display close price and volume
            
            st.write("Historical Close Price and Volume for 2025:")
            st.line_chart(tickerDf.Close)
            st.line_chart(tickerDf.Volumn)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a valid stock symbol.")
