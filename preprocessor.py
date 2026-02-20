import pandas as pd
import re

def preprocess(data):

    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[APMapm]{2}\s-\s'
    
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

  

    #--making dataframe 
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

# Remove special unicode space
    df['message_date'] = (
        df['message_date']
            .astype(str)
            .str.replace('\u202f', ' ', regex=False)
            .str.replace(' -', '', regex=False)
            .str.strip()
)

    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='mixed',
        dayfirst=True,
        errors='raise'   # IMPORTANT: do not allow silent failure
)

#--
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Feature engineering
    df['year'] = df['message_date'].dt.year
    df['month_num']= df['message_date'].dt.month
    df['month'] = df['message_date'].dt.month_name()
    df['only_date'] = df['message_date'].dt.date
    df['day_name'] = df['message_date'].dt.day_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    return df     

    
