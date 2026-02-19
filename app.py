import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import preprocessor, helper

import streamlit as st

import streamlit as st


st.set_page_config(
    page_title="MSG-X",
    page_icon="logo.jpeg"
)



 
st.sidebar.title("Watsapp chat analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # featch unique users

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "overall")
    selected_user = st.sidebar.selectbox("show analyst wrt", user_list)
    num_messages = helper.fetch_stats(selected_user, df)
    st.title('Top stats')
    # timeline
    ## Monthly
    if selected_user != 'overall':
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    ## Daily
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)    
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_link = helper.fetch_stats(selected_user, df)
        
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media_messages)  
        with col4:
            st.header("Link shared")
            st.title(num_link)   
    if selected_user == 'overall':
        st.title('most active users')
        x , new_df= helper.most_active_user(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()

            # Set black background
            fig.patch.set_facecolor('black')
            ax.set_facecolor('black')

            #    Ghost Green bars
            ax.bar(x.index, x.values, color='#00FF7F')  # ghost green

            # Make labels white (so visible on black)
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')

            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')

            plt.xticks(rotation=90)

            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)    
    # word cloud
    st.title('Word Cloud')
    df_wc = helper.Create_wordCloud(selected_user, df) 
    fig,ax = plt.subplots()
    
    ax.imshow(df_wc)
    st.pyplot(fig)       
    # most common words 
    most_common_df = helper.most_common_words(selected_user,df)
    fig,ax = plt.subplots()

    ax.barh(most_common_df[0], most_common_df[1])
    plt.xticks(rotation = 'vertical')
    st.title('most common words')
    st.pyplot(fig)
                   
    # emoji analysis 
    emoji_df = helper.emoji_helper(selected_user,df)
    st.title("Emoji Analysis")

    col1,col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax = plt.subplots()
        ax.pie(emoji_df['count'].head(),labels=emoji_df['emoji'].head(),autopct="%0.2f")
        st.pyplot(fig)