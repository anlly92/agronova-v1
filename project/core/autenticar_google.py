from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/calendar"]

flow = InstalledAppFlow.from_client_secrets_file(
    "core/credentials.json", scopes=SCOPES
)

creds = flow.run_local_server(port=8082, access_type='offline', prompt='consent')
with open("token.json", "w") as token:
    token.write(creds.to_json())
print("Autenticación completada y token.json generado.") 