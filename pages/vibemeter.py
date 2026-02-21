import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import helper

st.set_page_config(page_title="Vibe Meter")

st.title(" Vibe Meter Analysis")
# df
if 'chat_df' not in st.session_state:
    st.error("No chat data found. Please upload chat first.")
    st.stop()

df = st.session_state['chat_df']

st.subheader("Chat Preview")
st.dataframe(df)
# good morning count 
st.subheader(" Good Morning Pattern")

df['lower_msg'] = df['message'].str.lower()

gm_count = df[df['lower_msg'].str.contains("good morning|gm")].groupby('user').count()['message']

st.write("Good Morning Frequency:")
st.write(gm_count)

# effort

effort_df = helper.conversation_effort(df)
st.subheader(" Effort Score")
st.dataframe(effort_df)

 # emotional words
#-----------------------------------------------------

import pandas as pd

# Clean messages
df = df[df['user'] != 'group_notification']
df['lower_msg'] = df['message'].str.lower()

emotional_words = [
"ly","my","gn","miss","baby","love","jaan","cutu","love you",
"cutie","hottie","sexy","bae","dear","mine","highness","majesty",
"princess","queen","sweetu","sweetheart","bacha","mwa","mwaa",
"muhaa","ji"
]

emotion_data = []
total_emotion_count = 0

for user in df['user'].unique():
    user_df = df[df['user'] == user]
    user_total = 0

    for word in emotional_words:
        count = user_df['lower_msg'].str.contains(r'\b' + word + r'\b', regex=True).sum()

        if count > 0:
            emotion_data.append([user, word, count])
            user_total += count

    # Add total row per user
    emotion_data.append([user, "TOTAL", user_total])
    total_emotion_count += user_total

# Create dataframe
emotion_df = pd.DataFrame(emotion_data, columns=["User", "Word", "Count"])

st.subheader(" Emotional Word Dataset")
st.dataframe(emotion_df)

st.subheader(" Overall Emotional Count")
st.write(total_emotion_count)


#_-------------------------------------------------
# personal qution RelativeLayout:
    
total_msgs = len(df)
question_msgs = df[df['message'].str.contains("\?")].shape[0]

ratio = (question_msgs/total_msgs)*100

st.subheader(" Personal Question Ratio")
st.write(f"{round(ratio,2)} %")

# us count
us_count = df['lower_msg'].str.contains("us ").sum()

st.subheader("'Us' Usage")
st.write(us_count)

# jelous count

#--------------------------------------------------------

# Clean data
df = df[df['user'] != 'group_notification']
df['lower_msg'] = df['message'].str.lower()

jealous_words = [
"who was","with him","with her","why late",
"jealous","kisk","kiske","kon"
]

jealous_data = []
overall_jealous_count = 0

for user in df['user'].unique():
    user_df = df[df['user'] == user]
    user_total = 0

    for word in jealous_words:
        count = user_df['lower_msg'].str.contains(word).sum()

        if count > 0:
            jealous_data.append([user, word, count])
            user_total += count

    # Add total row per user
    jealous_data.append([user, "TOTAL", user_total])
    overall_jealous_count += user_total

# Create DataFrame
jealous_df = pd.DataFrame(jealous_data, columns=["User", "Word", "Count"])

st.subheader(" Jealousy Word Dataset")
st.dataframe(jealous_df)

st.subheader(" Overall Jealousy Count")
st.write(overall_jealous_count)
#---------------------------------------------------------------------

# Romantic Emojis
romantic_emojis = ["❤️","😘","😍","🥰","💋","💕","💖","💞"]

# Remove system messages
df = df[df['user'] != 'group_notification']

emoji_data = []
overall_emoji_count = 0

for user in df['user'].unique():
    user_df = df[df['user'] == user]
    user_total = 0

    for emoji in romantic_emojis:
        count = user_df['message'].str.contains(emoji, regex=False).sum()

        if count > 0:
            emoji_data.append([user, emoji, count])
            user_total += count

    # Add total row per user
    emoji_data.append([user, "TOTAL", user_total])
    overall_emoji_count += user_total

# Create DataFrame
emoji_df = pd.DataFrame(emoji_data, columns=["User", "Emoji", "Count"])

st.subheader(" Romantic Emoji Dataset")
st.dataframe(emoji_df)

st.subheader(" Overall Romantic Emoji Count")
st.write(overall_emoji_count)


# future refrence
future_refrence = ["future","marry","wedding","life together","our house"]

future_count = 0
for e in future_refrence:
    future_count += df['message'].str.contains(e).sum()

st.subheader(" Future  Frequency")
st.write(future_count)

# physical
# Clean data
df = df[df['user'] != 'group_notification']
df['lower_msg'] = df['message'].str.lower()

intimate_words = [
"love","lovely","soulmate","darling","honey","sweetheart","baby","bae","boo",
"jaan","jaan u","cutie","cuddle","cuddling","snuggle","hug","hugging",
"kiss","kissing","kissed","lip","lips","flirt","flirting","naughty",
"sexy","hot","attractive","gorgeous","pretty","cute","damn",
"touch","touching","touched","nude","nudes","naked","make out","hookup",
"horny","aroused","passion","passionate","miss you","thinking of you",
"good night baby","gn baby","sweet dreams","can't sleep",
"jealous","only mine","don't leave me","forever yours",
"future together","marry","marriage","proposal"
]

intimate_data = []
overall_intimate_count = 0

for user in df['user'].unique():
    user_df = df[df['user'] == user]
    user_total = 0

    for word in intimate_words:
        count = user_df['lower_msg'].str.contains(r'\b' + word + r'\b', regex=True).sum()

        if count > 0:
            intimate_data.append([user, word, count])
            user_total += count

    # Add total row per user
    intimate_data.append([user, "TOTAL", user_total])
    overall_intimate_count += user_total

# Create DataFrame
intimate_df = pd.DataFrame(intimate_data, columns=["User", "Word", "Count"])

st.subheader("Intimate Word Dataset")
st.dataframe(intimate_df)

st.subheader("Overall Intimate Count")
st.write(overall_intimate_count)


# final score

romantic_score = (
    total_emotion_count * 2 +
    overall_emoji_count * 3 +
    future_count * 1.5 +
    overall_jealous_count * 2 +
    overall_intimate_count * 4
)

st.subheader(" Vibe Meter Score")
st.title(round(romantic_score,2))

if romantic_score > 1500:
    st.success("Strong BF/GF Vibes ")
elif romantic_score > 1000:
    st.warning("Confusing Zone ")
elif romantic_score > 500:
    st.warning("Best Friend Energy ")
elif romantic_score > 300:
    st.warning(" Friend Zone ")    
else:
    st.info(" Just Known")





