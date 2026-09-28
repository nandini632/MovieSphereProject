from dotenv import load_dotenv
import os
import requests

load_dotenv()

LOGIN_URL = os.getenv("SALESFORCE_LOGIN_URL")
CLIENT_ID = os.getenv("SALESFORCE_CLIENT_ID")
CLIENT_SECRET = os.getenv("SALESFORCE_CLIENT_SECRET")


def get_salesforce_token():
    response = requests.post(
        f"{LOGIN_URL}/services/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    )

    response.raise_for_status()
    return response.json()["access_token"]


def get_salesforce_accounts():
    token = get_salesforce_token()

    url = f"{LOGIN_URL}/services/data/v65.0/query"
    query = """
        SELECT Id, Name, MovieSphere__c, Movie_Title__c,
               Movie_Rating__c, Movie_Year__c,
               Movie_Genre__c, Movie_Description__c
        FROM Account
        WHERE MovieSphere__c != NULL
        LIMIT 20
    """

    response = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        params={"q": query},
    )

    response.raise_for_status()
    return response.json()["records"]


if __name__ == "__main__":
    records = get_salesforce_accounts()
    print("Salesforce records:", len(records))