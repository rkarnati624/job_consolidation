from base64 import b64encode
import requests
import json
import dateutil.parser
from datetime import datetime, timedelta

current_date = datetime.today().date()


# getting a token for api call
def get_token():
    client_id = r'42fb3e9a-3159-400d-8d6c-c6024942b5af'
    client_pw = r'SZ"H&M-}b"7gfc$'
    client_combined = client_id + ":" + client_pw
    # client_combined_base64_as_bytes = b64encode(str.encode(client_combined))
    client_combined_base64 = b64encode(str.encode(client_combined)).decode()

    response = requests.post('https://account.demandware.com/dw/oauth2/access_token',
                             headers={'Authorization': 'Basic %s' % client_combined_base64,
                                      "Content-Type": "application/x-www-form-urlencoded"},
                             data={'grant_type': 'client_credentials'})
    # print(response)
    json_to_python = response.json()
    return json_to_python['access_token']


def get_job_execution_search(job):
    global token
    payload = {
        "count": 3,
        "expand": [
            "string"],
        "query": {"term_query":
                      {"fields": ["job_id"],
                       "operator": "is",
                       "values": ["%s" % job]}},
        "sorts": [
            {
                "field": "start_time",
                "sort_order": "desc"
            }
        ],
        "start": 0
    }
    payload = json.dumps(payload)
    response = requests.post('https://staging-web-lumens.demandware.net/s/-/dw/data/v20_4/job_execution_search',
                             headers={'Authorization': 'Bearer %s' % token, "Content-Type": "application/json"},
                             data=payload, verify=False)
    job_status = response.json()
    print(job_status)
    return job_status


if __name__ == "__main__":
    client_id = r'42fb3e9a-3159-400d-8d6c-c6024942b5af'
    client_pw = r'SZ"H&M-}b"7gfc$'
    client_combined = client_id + ":" + client_pw
    # client_combined_base64_as_bytes = b64encode(str.encode(client_combined))
    client_combined_base64 = b64encode(str.encode(client_combined)).decode()

    response = requests.post('https://account.demandware.com/dw/oauth2/access_token',
                             headers={'Authorization': 'Basic %s' % client_combined_base64,
                                      "Content-Type": "application/x-www-form-urlencoded"},
                             data={'grant_type': 'client_credentials'})
    # print(response)
    json_to_python = response.json()
    token = json_to_python['access_token']
    print(token)
    get_job_execution_search(job='Custom_NN_Sale_Lumens1')
    print("catalog replication is finished for current date")
