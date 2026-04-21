# SmartVote Navigator AI (Production Cloud Edition)

### 1. Project Name
**SmartVote Navigator AI**

### 2. Problem Statement
Many potential voters abandon the process due to confusion over registration dates, eligibility, and polling locations. 

### 3. Solution Approach
SmartVote Navigator solves this globally through a hyper-scalable, Google Cloud-powered intelligence API. The system utilizes structured logic combined with external mocked API resolution (Google Maps, Calendar) seamlessly delivered via a FastAPI Cloud Run environment.

### 4. Architecture Diagram
```ascii
     [User / Client UI]
             | (REST)
             v
+-----------------------------+
|        Cloud Run            |
| +-------------------------+ |
| |       FastAPI           | |
| | /routes/chat            | |
| | /routes/locations       | |
| | /routes/reminder        | |
| +-------------------------+ |
+------------+----------------+
             |
 +-----------+-----------+
 |           |           |
 v           v           v
[Firestore] [Maps API] [Calendar API]
(Sessions)  (Location)   (Mocked)
```

### 5. Services Used
- **Google Cloud Run:** Fast, scalable execution of the containerized core backend.
- **Google Firebase (Firestore):** Retains deep conversation history enabling resilient sessions.
- **Google Maps API:** Simulated coordinate retrieval and map routing URLs.
- **Google Calendar API:** Generates structured `.ics` metadata and link integration.

### 6. API Endpoints
- **`POST /chat`**: The decision engine. Pass in `{"session_id": "abc", "message": "hello"}` to get an action-triggered response.
- **`GET /locations?zip_code=10001`**: Retrieve coordinate distance details and a mapped URL.
- **`POST /reminder`**: Receive an active Calendar hook for Election Day.

### 7. Deployment Guide
Deploy your system into production using standard GCP hooks.
Ensure you have the `gcloud` CLI installed.

**1. Create a `firebase.json` or obtain credentials:**
Acquire your Firebase service account JSON and set it locally:
```bash
export FIREBASE_CREDENTIALS_PATH="/path/to/key.json"
```

**2. Submit to Cloud Build:**
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/smartvote-navigator
```

**3. Deploy to Cloud Run:**
```bash
gcloud run deploy smartvote-navigator \
    --image gcr.io/YOUR_PROJECT_ID/smartvote-navigator \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars=MOCK_FIREBASE=False
```

### 8. Testing Guarantee
The backend incorporates strict rules assuring no political bias, underage gating, and rigorous Pydantic typing. Try it yourself locally:
```bash
pip install -r requirements.txt
pytest -v tests/
```
