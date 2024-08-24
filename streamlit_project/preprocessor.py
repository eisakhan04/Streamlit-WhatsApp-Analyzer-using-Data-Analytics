import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:AM|PM)\s-\s'
    
    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)

    # Debugging: Check the lengths of messages and dates
    if len(messages) != len(dates):
        print(f"Length of messages: {len(messages)}")
        print(f"Length of dates: {len(dates)}")
        print("There is a mismatch between the number of messages and dates.")

        # Adjusting lengths to match if necessary (optional)
        # If messages has an extra element, we can remove it
        if len(messages) > len(dates):
            messages = messages[:len(dates)]
        elif len(dates) > len(messages):
            dates = dates[:len(messages)]

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime type
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate user and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional time-related information
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute


    period = []
    for hour in df[['day_name' , 'hour']]['hour']:
        if hour == 23:
           period.append(str(hour) + "-" + str('00'))
        elif hour ==0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))

    df['period'] = period        
        

    return df
