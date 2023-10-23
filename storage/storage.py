from kivy.storage.jsonstore import JsonStore

store = JsonStore('financeiro_mic.json')


# content_data = { "table_name": "users",
#                 [
#                  {"user_name": "person_1", "mensal_income": 10000.00, user_phone:"+5511"},
#                  {"user_name": "person_2", "mensal_income": 1000.00,  user_phone:"+5521"},
#                 ]
def insert_data(content_data):
    store.put(content_data["table_name"], objects=content_data["json_content"])

def select_data(content_data):
    return store.get(content_data["table_name"])[content_data["data_id"]]

def delete_table(content_data):
  if store.exists(content_data["table_name"]):
     store.delete(content_data["table_name"])