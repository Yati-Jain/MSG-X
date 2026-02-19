from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extract =  URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    # total messages
    num_messages = df.shape[0]

    # total words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch a number of link shere
    links=[]
    for message in df ['message'] :
        links.extend(extract.find_urls(message))
    return num_messages, len(words), num_media_messages, len(links)




def most_active_user(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/ df.shape[0])* 100, 2).reset_index().rename(columns ={ 'user': 'Name', 'count':'percent'})
    return x,df


def Create_wordCloud(selected_user, df):
    if selected_user !='overall':
        df = df[df['user']== selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=15,background_color='white')    
    df_wc = wc.generate(df['message'].str.cat(sep =" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user !='overall':
        df = df[df['user']== selected_user]
    temp = df[df['user'] != 'group_notification']    
    temp = temp[~temp['message'].str.contains('media', case=False, na=False)]

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))  
    return most_common_df     


def emoji_helper(selected_user, df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(
        Counter(emojis).most_common(),
        columns=['emoji', 'count']
    )

    return emoji_df
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

# conversation effort 
def conversation_effort(df):

    df = df[df['user'] != 'group_notification'].copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    users = df['user'].unique()
    total_messages = len(df)

    df['only_date'] = df['date'].dt.date
    total_days = df['only_date'].nunique()

    effort_results = []

    max_avg_length = df['message'].apply(len).mean()

    for user in users:

        user_df = df[df['user'] == user]
        msg_count = len(user_df)

        # Message Share
        message_share = msg_count / total_messages

        # Avg Length
        avg_length = user_df['message'].apply(len).mean()

        # Question Rate
        question_rate = user_df['message'].str.count('\?').sum() / msg_count

        # Initiation Rate
        initiations = 0
        for date in df['only_date'].unique():
            day_df = df[df['only_date'] == date]
            if day_df.iloc[0]['user'] == user:
                initiations += 1

        initiation_rate = initiations / total_days

        # Effort Score (0–100)
        effort_score = (
            message_share * 30 +
            (avg_length / max_avg_length) * 20 +
            question_rate * 20 +
            initiation_rate * 30
        ) 

        effort_results.append([user, round(effort_score, 2)])

    effort_df = pd.DataFrame(effort_results, columns=['user', 'Effort Score'])

    return effort_df
