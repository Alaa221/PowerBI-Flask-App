POWER BI + PYTHON FLASK DEMO
============================

IMPORTANT:
The screenshot you sent shows a Power BI Pro workspace. That is enough to
develop/test an embedded solution with trial embed tokens, but production
embedding requires a supported capacity.

Also, the powerbi:// URL you sent is not the Workspace ID or Report ID.
Do not put that URL in WORKSPACE_ID.

1) Create a normal Power BI workspace (not "My workspace").
   Microsoft service principal embedding does not support My workspace.

2) Publish your report to that workspace.

3) Open the report in Power BI Service and copy its browser URL.
   It will look similar to:
   https://app.powerbi.com/groups/<WORKSPACE_ID>/reports/<REPORT_ID>/...

4) Create a Microsoft Entra App Registration.
   Get:
   - Tenant ID
   - Application (client) ID
   - Client secret

5) In Power BI Admin Portal, a Power BI admin must enable:
   - Embed content in apps
   - Allow service principals to use Power BI APIs

6) Add the app/service principal to the Power BI workspace as Member
   or Admin.

7) Copy .env.example to .env and fill in the values.

8) Install:
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt

9) Run:
   python app.py

10) Open:
   http://127.0.0.1:5000

SECURITY:
Never put CLIENT_SECRET in HTML or JavaScript.
Keep it only in the Python backend/.env.
Do not commit .env to Git.

NEXT STEP:
Send me the browser URL of the actual report (the https://app.powerbi.com/...
URL). I can tell you exactly where the Workspace ID and Report ID are.
