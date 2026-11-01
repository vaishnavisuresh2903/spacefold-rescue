# SpaceFold Rescue 
**Team ORIGENIX** | *Fold Small. Think Beyond.*

**SpaceFold Rescue** combines the **Meta Model API** (`muse-spark-1.3`) with a **3D kinematic simulator** to explore how a compact folding structure can adapt within modeled mechanical constraints when deployment gets blocked.

---

##  The Problem
Deployable folding structures can transport shelters and equipment as compact packages that unfold on-site. A jammed hinge can interrupt the planned deployment sequence. Recovery requires identifying which movements remain mechanically possible and recognizing when the modeled constraints require deployment to stop.

## 💡 Our Solution
SpaceFold Rescue is an AI-guided simulation prototype that pairs the **Meta Model API** with a deterministic constraint checker. When a fault occurs, the AI interprets the structure’s state and proposes recovery sequences. The simulator checks those proposals against modeled joint limits and collision constraints before execution.

---

##  How It Works (5-Step Closed Loop)
1. **Start Deployment:** A compact multi-panel structure begins opening in an interactive 3D simulation.
2. **Introduce a Fault:** The user locks a hinge mid-deployment to simulate a mechanical jam.
3. **Analyze the State:** Joint angles, hinge states, movement dependencies, and simulator feedback are sent to the **Meta Model API** (`muse-spark-1.3`) through the backend service.
4. **Propose and Verify Alternatives:** The AI proposes alternative unfolding sequences using the remaining independently movable panels. Because proposals may be mechanically infeasible, the simulator checks the proposed motion paths against modeled joint limits and 3D panel collisions.
5. **Recover or Stop:** A sequence that passes validation executes toward an alternative, partially deployed configuration. If no valid path is found, deployment remains stopped, and the diagnostic panel explains the detected constraint or rejected proposal.

---

##  Repository Structure
* `index.html` — Interactive 3D WebGL/Three.js Kinematic Simulator, Fault Injection Controls, Deterministic Constraint Checker, and Diagnostic UI. Includes a configurable backend URL input and an explicitly labeled offline demonstration fallback mode.
* `azure_backend.py` — FastAPI backend service that orchestrates kinematic telemetry payloads and calls the Meta Model API (`muse-spark-1.3`). Can be run locally for development or deployed to Microsoft Azure App Service / Container Apps.
* `requirements.txt` — Python dependencies for the backend service.

---

##  API Requirement & Offline Demonstration Mode
* **Live Meta AI Analysis (Requires Running Backend):** Live fault interpretation and recovery sequence generation require `azure_backend.py` running with a valid `META_MODEL_API_KEY` and connected to `index.html` via the **Backend API Endpoint** input field.
* **Offline Demonstration Mode (Simulated Responses):** If the backend is unreachable or the user selects **Offline Demo Mode**, `index.html` falls back to pre-programmed deterministic demo scenarios. All outputs in this mode are explicitly labeled `[SIMULATED OFFLINE DEMO — NO LIVE API CALL]` in the UI console.

---

##  Quick Start

### Step 1: Start the Backend Locally
Running `uvicorn` starts the backend service on your local machine (`http://localhost:8000`).

```bash
pip install -r requirements.txt
export META_MODEL_API_KEY="your_meta_model_api_key"
export META_MODEL_NAME="muse-spark-1.3"
uvicorn azure_backend:app --host 0.0.0.0 --port 8000

### Step 2:Verify a Live Meta Model API Response
With the local backend running, send a POST request to ⁠http://localhost:8000/api/recover⁠ with ⁠structure_id: "origami_shelter_v1"⁠ and your hinge states (⁠R1⁠ locked at ⁠35.0°⁠, ⁠E1⁠ unlocked at ⁠25.0°⁠, ⁠W1⁠ unlocked at ⁠25.0°⁠).
Expected Live API Response (⁠muse-spark-1.3⁠): Returns JSON with ⁠"mode": "LIVE_META_MODEL_API"⁠, ⁠"recovery_possible": true⁠, and a ⁠proposed_sequence⁠ extending unlocked panels ⁠E1⁠ and ⁠W1⁠ to ⁠110.0°⁠ within ⁠[0°, 120°]⁠ joint limits.

curl -X POST "http://localhost:8000/api/recover" \
  -H "Content-Type: application/json" \
  -d '{
    "structure_id": "origami_shelter_v1",
    "hinges": [
      {"hinge_id": "R1", "current_deg": 35.0, "min_deg": 0.0, "max_deg": 120.0, "locked": true, "dependencies": ["Roof_Arch"]},
      {"hinge_id": "E1", "current_deg": 25.0, "min_deg": 0.0, "max_deg": 120.0, "locked": false, "dependencies": []},
      {"hinge_id": "W1", "current_deg": 25.0, "min_deg": 0.0, "max_deg": 120.0, "locked": false, "dependencies": []}
    ],
    "simulator_feedback": "Hinge R1 jammed at 35 degrees during primary unfolding."
  }'

Expected Live API JSON Response:

{
  "model_used": "muse-spark-1.3",
  "mode": "LIVE_META_MODEL_API",
  "fault_summary": "Hinge R1 is mechanically locked at 35.0 degrees, preventing full elevation of the primary roof arch.",
  "recovery_possible": true,
  "proposed_sequence": [
    {
      "hinge_id": "E1",
      "target_deg": 110.0,
      "reason": "Extend unlocked East panel outward within [0, 120] degree joint limit to establish lateral coverage."
    },
    {
      "hinge_id": "W1",
      "target_deg": 110.0,
      "reason": "Extend unlocked West panel symmetrically to form a stable partially deployed A-frame configuration."
    }
  ],
  "operator_explanation": "Hinge R1 remains held at 35 degrees. Independent panels E1 and W1 deploy to 110 degrees without panel collision."
}

### Step 3:Launch the 3D Simulator Frontend & Connect to the Backend
1. Serve ⁠index.html⁠ locally (⁠python3 -m http.server 5500⁠) and open ⁠http://localhost:5500/index.html⁠ in your browser.
2. In the right-hand sidebar under Backend Connection Settings, set the Backend API URL to ⁠http://localhost:8000/api/recover⁠ (or your deployed Azure URL) and select Live Meta Model API.

Deploying the Backend to Microsoft Azure
Once tested locally, deploy ⁠azure_backend.py⁠ to Azure App Service (⁠az webapp up --name spacefold-rescue-api --runtime "PYTHON:3.11"⁠) and configure ⁠META_MODEL_API_KEY⁠ and ⁠META_MODEL_NAME="muse-spark-1.3"⁠ in Azure App Settings so the backend is Azure-hosted.

az webapp up --name spacefold-rescue-api --runtime "PYTHON:3.11" --sku B1
az webapp config appsettings set --name spacefold-rescue-api --resource-group <your-rg> \
  --settings META_MODEL_API_KEY="<your_meta_model_api_key>" META_MODEL_NAME="muse-spark-1.3"


After deployment, update the Backend API URL in ⁠index.html⁠ to ⁠https://spacefold-rescue-api.azurewebsites.net/api/recover⁠.

Engineering Scope & Limitations:

This prototype evaluates geometric and kinematic motion feasibility only. Kinematic joint-limit and 3D collision checks do not validate structural strength, material stress, weather resistance, actuator torque/forces, or suitability for human occupancy. Real-world shelter deployment requires separate mechanical and structural engineering validation.
