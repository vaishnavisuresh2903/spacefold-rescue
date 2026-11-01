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
