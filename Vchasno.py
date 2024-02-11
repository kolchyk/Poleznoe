import requests
import pandas as pd
import json
API_HOST = "https://vchasno.ua"
headers = {"Authorization": "GgPq3irGr2pzbeor1-0bGXnexnSa0OPbHzVi"}
response = requests.get(f"{API_HOST}/api/v2/incoming-documents?date_created_from=2023-01-01&with_recipients=1&status=7000&status=7001&status=7002&status=7003&status=7004&status=7005&status=7006&status=7007&status=7010", headers=headers)
response_data = json.loads(response.text)
documents_list = response_data['documents']
documents_df = pd.DataFrame(documents_list)
filtered_df = documents_df[documents_df['status'] != 7008]
non_list_columns = [col for col in filtered_df.columns if not filtered_df[col].apply(lambda x: isinstance(x, list)).any()]
columns_to_drop = filtered_df[non_list_columns].columns[filtered_df[non_list_columns].nunique() == 1]
filtered_df.drop(columns=columns_to_drop, inplace=True)





# Функция для извлечения email-адресов, теперь с проверкой типа данных
def extract_emails(recipient_data):
    if isinstance(recipient_data, str):
        # Если данные в формате строки, преобразуем их в список словарей
        try:
            recipients_list = json.loads(recipient_data.replace("'", "\""))
        except json.JSONDecodeError:
            return None, None
    elif isinstance(recipient_data, list):
        # Если данные уже в формате списка, используем их напрямую
        recipients_list = recipient_data
    else:
        return None, None
    
    # Извлечение email-адресов
    emails = [recipient['emails'][0] for recipient in recipients_list if 'emails' in recipient and recipient['emails']]
    email_1 = emails[0] if len(emails) > 0 else None
    email_2 = emails[1] if len(emails) > 1 else None
    return email_1, email_2

# Применение функции к каждой строке столбца и создание новых столбцов
filtered_df[['email_Darnytsia', 'email_partner']] = filtered_df['recipients'].apply(lambda x: pd.Series(extract_emails(x)))
