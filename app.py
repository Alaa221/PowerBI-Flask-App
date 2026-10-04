import os
import requests
import msal
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")
REPORT_ID = os.getenv("REPORT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
POWERBI_SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]

def get_aad_token():
    if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET]):
        raise RuntimeError("Missing TENANT_ID, CLIENT_ID or CLIENT_SECRET in .env")

    cca = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    )
    result = cca.acquire_token_for_client(scopes=POWERBI_SCOPE)

    if "access_token" not in result:
        raise RuntimeError(result.get("error_description", str(result)))

    return result["access_token"]

def get_embed_config():
    if not WORKSPACE_ID or not REPORT_ID:
        raise RuntimeError("Missing WORKSPACE_ID or REPORT_ID in .env")

    token = get_aad_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    report_url = (
        f"https://api.powerbi.com/v1.0/myorg/groups/"
        f"{WORKSPACE_ID}/reports/{REPORT_ID}"
    )
    report_response = requests.get(report_url, headers=headers, timeout=30, verify=False)
    report_response.raise_for_status()
    report = report_response.json()

    generate_token_url = (
        f"https://api.powerbi.com/v1.0/myorg/groups/"
        f"{WORKSPACE_ID}/reports/{REPORT_ID}/GenerateToken"
    )
    token_response = requests.post(
    generate_token_url,
    headers=headers,
    json={"accessLevel": "View"},
    timeout=30,
    verify=False
)
    token_response.raise_for_status()

    embed_token = token_response.json()["token"]

    return {
        "id": report["id"],
        "name": report.get("name", ""),
        "embedUrl": report["embedUrl"],
        "accessToken": embed_token,
    }

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/powerbi")
def powerbi_config():
    try:
        return jsonify(get_embed_config())
    except requests.HTTPError as e:
        detail = e.response.text if e.response is not None else str(e)
        return jsonify({"error": detail}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
