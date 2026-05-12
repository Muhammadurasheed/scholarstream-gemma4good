# ScholarStream: The Agentic User Journey

This document outlines the high-fidelity, autonomous pipeline that powers ScholarStream.

## **Phase 1: The DNA Synthesis (Onboarding)**
1.  **Identity Capture**: The user enters their "Academic DNA"—Major (e.g., *Biomedical Engineering*), Location (e.g., *Nigeria*), and Interests (e.g., *Prosthetics, AI, Social Impact*).
2.  **Vectorization**: Behind the scenes, the **Cortex Vectorization Engine** transforms these raw strings into a high-dimensional embedding. This represents the student's unique intellectual footprint in our "Opportunity Latent Space."
3.  **Genesis Trigger**: Upon clicking "Complete Onboarding," a `POST /api/scholarships/discover` request is dispatched. The system detects a "New User" state and initializes the **Genesis Mission**.

## **Phase 2: The Strategy Chamber (Gemma Reasoning)**
4.  **Cortex Brain Activation**: The **GemmaAIService** is summoned. It receives the user's DNA and enters the "Thinking" state.
5.  **Autonomous Planning**: Instead of searching a fixed database, Gemma formulates a **Strategic Hunt Plan**:
    *   *“Since the user is in Nigeria studying Biomed, I will prioritize Mastercard Foundation portals and search for ‘Bio-Tech Grants Africa’ on specialized medical subreddits.”*
6.  **Telemetry Broadcast**: This internal reasoning is telegraphed to the **Mission Control Console** via the `DiscoveryPulseService`. The user sees: `🧠 [THOUGHT] Analyzing Digital DNA: Formulating specialized hunt for Bio-Tech signals in West Africa.`

## **Phase 3: The Drone Deployment (Sentinels in Motion)**
7.  **Sentinel Dispatch**: The **Sentinel Navigator** receives the strategy (optimized queries, target URLs). It deploys a fleet of Playwright-powered "Drones."
8.  **Deep Web Scouting**: Drones hit multiple targets simultaneously:
    *   **Google Dorks**: Scouring for "Apply Now" bio-grants.
    *   **Niche Social**: Scanning Reddit and LinkedIn for high-signal recruitment posts.
    *   **Portal Infiltration**: Directly extracting structured data from global foundations (Mastercard, Rhodes, etc.).
9.  **Real-Time Observation**: The dashboard updates with the **Live Telemetry Feed**:
    *   `📡 [DRONE-01] Investigating Mastercard Foundation portal...`
    *   `⚠️ [CHALLENGE] Encountered Cloudflare challenge on Reddit. Rerouting via secondary stealth proxy...`

## **Phase 4: The Refinery (Strict Governance & Scoring)**
10. **Extraction & Enrichment**: Raw HTML is pulled back to the **Refinery Worker**. Gemma 4 extracts the "Essence" (Amount, Deadline, Eligibility) and filters out the noise.
11. **The 60% Trust Floor**: Every opportunity is matched against the User DNA using the **70/30 Cortex Formula**. 
    *   If a "Tech Hackathon" is found, the **Strict Filter** (Gemma Judgment) triggers: *“User is Medical. Is this hackathon relevant? NO.”* -> The score is capped at 15% and it **never** hits the user's dashboard.
12. **Cortex Picks Generation**: For elite matches (>85%), a **Deep Match Report** is generated, explaining *why* this is a life-changing fit.

## **Phase 5: The Landing (Mission Accomplished)**
13. **Dashboard Arrival**: The **Genesis Hunt Overlay** fades away. The user's dashboard is populated with **Cortex Picks**—ultra-personalized, verified, and fresh.
14. **Always-On Patrol**: The system doesn't stop. The **Sentinel Heartbeat** enters "Patrol Mode," continuing to scan the internet every 30 minutes. If a new match is found while the user is away, a real-time notification (WebSocket) is ready for their next login.

---

### **Engineering Principles**
*   **Agentic Autonomy**: Decisions are made by Gemma, not hardcoded if-statements.
*   **Observability**: What the AI "thinks" is what the user "sees."
*   **Relevance First**: Precision is more important than volume.

*Allahu Musta'an.*
