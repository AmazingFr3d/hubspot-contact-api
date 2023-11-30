import requests
import time
from creds import creds

api = creds.api_key


def get_id(email):
    url = f"https://api.hubapi.com/crm/v3/objects/contacts/{email}?idProperty=email"
    payload = {}
    headers = {
        'Authorization': api
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(f"{email} | {response.status_code} | {response.reason}")
    if response.status_code != 404:
        hub_id = dict(response.json())
        hub_id = hub_id['id']
        return hub_id


def delete_id(hub_id):
    url = f"https://api.hubapi.com/crm/v3/objects/contacts/{hub_id}"
    payload = {}
    headers = {
        'Authorization': api
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    if response.status_code != 404:
        print("Contact Deleted!")
    else:
        print(response.status_code, response.reason)


def helper(data):
    count = 0
    for index, row in data.iterrows():

        if row['Stat'] != "Done":
            hub_id = get_id(row['Email'])
            if hub_id:
                delete_id(hub_id)
                data.loc[index, ['Stat']] = "Done"
                # data.drop(index, inplace=True)
                data.to_csv("contacts_to_delete.csv", index=False)
            else:
                data.loc[index, ['Stat']] = "Done"
                # data.drop(index, inplace=True)
                data.to_csv("contacts_to_delete.csv", index=False)

            count += 2
            if count == 100:
                time.sleep(20)
                count = 0
