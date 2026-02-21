import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import preprocessor, helper




st.set_page_config(
    page_title="MSG-X",
    page_icon="logo.jpeg"
)
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}                        
</style>
""", unsafe_allow_html=True)

# ---------------- NAVBAR ---------------- #
st.markdown("""
<style>
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background: linear-gradient(90deg, #000000, #111111);
    padding: 18px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 9999;
    box-shadow: 0px 4px 15px rgba(0, 255, 127, 0.2);
}

.nav-logo {
    color: #00FF7F;
    font-size: 24px;
    font-weight: bold;
    letter-spacing: 1px;
}

.nav-links a {
    color: white;
    text-decoration: none;
    margin-left: 30px;
    font-size: 16px;
    transition: 0.3s;
}

.nav-links a:hover {
    color: #00FF7F;
}

body {
    padding-top: 90px;
}
</style>

<div class="navbar">
    <div class="nav-logo">MSG-X</div>
    <div class="nav-links">
       
       

</div>
""", unsafe_allow_html=True)





# ---------------- TOP CONTROLS ---------------- #
st.markdown("## Upload Chat File")

uploaded_file = st.file_uploader("Upload WhatsApp Chat")

if uploaded_file:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "overall")

    selected_user = st.selectbox("Select User", user_list)
    show_analysis = st.button("Analyze ")


    




 

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.session_state['chat_df'] = df
    st.dataframe(df)
         
    # featch unique users

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "overall")
   
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
    if show_analysis:
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


    # ---------------- TIME DIFFERENCE ANALYSIS ---------------- #
    st.title("Reply Behaviour Pattern")
# Remove group notifications
    df_time = df[df['user'] != 'group_notification'].copy()

    df_time['message_date'] = pd.to_datetime(df_time['message_date'])
    df_time = df_time.sort_values('message_date')

    users = df_time['user'].unique()

    if len(users) == 2:

        reply_data = {users[0]: [], users[1]: []}

        for i in range(1, len(df_time)):
            prev_user = df_time.iloc[i-1]['user']
            curr_user = df_time.iloc[i]['user']

            if prev_user != curr_user:
                diff = (
                    df_time.iloc[i]['message_date'] - df_time.iloc[i-1]['message_date']
                ).total_seconds() / 60

                reply_data[curr_user].append(diff)

        def categorize(times):
            categories = {
                "Under 1 min": 0,
                "1-5 mins": 0,
                "5-30 mins": 0,
                "30+ mins": 0
            }

            for t in times:
                if t <= 1:
                    categories["Under 1 min"] += 1
                elif t <= 5:
                    categories["1-5 mins"] += 1
                elif t <= 30:
                    categories["5-30 mins"] += 1
                else:
                    categories["30+ mins"] += 1

            return categories

        

        col1, col2 = st.columns(2)

        for idx, user in enumerate(users):
            behaviour = categorize(reply_data[user])

            fig, ax = plt.subplots()
            ax.bar(behaviour.keys(), behaviour.values())
            plt.xticks(rotation=45)

            if idx == 0:
                col1.pyplot(fig)
                col1.subheader(user)
            else:
                col2.pyplot(fig)
                col2.subheader(user)

    else:
        st.warning("Works only for 2-person chats.")   

    # conversation effort 
        
    st.title("Conversation Effort Analysis")
    st.markdown("""
                 Effort Score = (Message Share × 30) + (Normalized Message Length × 20) +(Question Rate × 20) +(Initiation Rate × 30) """)

    effort_df = helper.conversation_effort(df)

    st.dataframe(effort_df)
    st.markdown("""\n
                If score is 80-100 -> high effort\n
                   If score is 50- 80 -> moderate effort\n
                   If score is 30- 50 -> low effort\n
                   If score is below 30 ->very low effort""")
    top5 = effort_df.head(5)
    fig, ax = plt.subplots()
    ax.bar(top5['user'], top5['Effort Score'])
    ax.set_ylabel("Effort Score (0–100)")
    plt.xticks(rotation=90)
    
    st.pyplot(fig)
           
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

     # Button:
    
    st.markdown("""
    <style>


    div.stButton > button {
        background: transparent;
        color: #00ff88;
        border: 2px solid #00ff88;
        border-radius: 40px;
        padding: 14px 30px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
                
    }

    /* Hover Effect */
    div.stButton > button:hover {
        background-color: #00ff88;
        color: black;
        box-shadow: 0 0 20px #00ff88;
    }

    </style>
    """, unsafe_allow_html=True)

    # Center button
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        if st.button(" Enter Vibe Meter"):

            df_temp = st.session_state['chat_df']
            user_count = len(df_temp[df_temp['user'] != 'group_notification']['user'].unique())

            if user_count == 2:
                st.switch_page("pages/vibemeter.py")
            else:
                st.warning("Vibe Meter available only for 2-person chats ")

    