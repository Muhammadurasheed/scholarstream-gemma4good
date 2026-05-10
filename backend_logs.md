HP@Emrash MINGW64 ~/Documents/scholarstream-monorepo/backend (hackathon-final)
$ python run.py
[INFO] Checking Port 8081 availability...
[INFO] Port is free and bindable.
[INFO] Environment variables loaded from .env
==> Starting ScholarStream FastAPI Backend...
==> Server will run at: http://localhost:8081
==> Auto-reload DISABLED for stability
2026-05-09 12:41:06 [info     ] OpportunityScraperService: CORTEX MODE ACTIVE legacy_scrapers=REMOVED message=All discovery via Playwright-based Sentinel patrols
2026-05-09 12:41:07 [info     ] Firebase initialized successfully
2026-05-09 12:41:07 [info     ] AdaptiveRateLimiter initialized max_concurrent=5 max_retries=4 max_rpm=30
2026-05-09 12:41:10 [info     ] Gemma AI initialized with Cloud ADC project_id=scholarstream-gemma4good
2026-05-09 12:41:10 [info     ] ScholarStream is running on GEMMA 4 NATIVE ENGINE
2026-05-09 12:41:10 [info     ] Firebase already initialized  
2026-05-09 12:41:10 [info     ] ⚡ GEMMA NATIVE ENGINE ACTIVE (Hackathon Mode)
INFO:     Started server process [5052]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8081 (Press CTRL+C to quit)
2026-05-09 11:41:25 [error    ] Pulse: Announcement failed     [app.services.discovery_pulse] error=WRONGPASS invalid or missing auth token. See https://docs.upstash.com/redis/troubleshooting/http_unauthorized for details.
INFO:     ('127.0.0.1', 51574) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
INFO:     127.0.0.1:65002 - "OPTIONS /api/scholarships/matched?user_id=demo_guest_user HTTP/1.1" 200 OK
INFO:     connection open
INFO:     ('127.0.0.1', 59702) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
INFO:     connection open
INFO:     127.0.0.1:51576 - "GET /api/scholarships/matched?user_id=demo_guest_user HTTP/1.1" 200 OK
INFO:     127.0.0.1:62398 - "OPTIONS /api/scholarships/opp_01357e0e1a3e3b67 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 52960) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
INFO:     127.0.0.1:59658 - "OPTIONS /api/scholarships/opp_01357e0e1a3e3b67 HTTP/1.1" 200 OK
INFO:     connection open
INFO:     127.0.0.1:50060 - "OPTIONS /api/applications/start HTTP/1.1" 200 OK
INFO:     127.0.0.1:54129 - "OPTIONS /api/applications/start HTTP/1.1" 200 OK
INFO:     connection closed
INFO:     ('127.0.0.1', 53061) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
INFO:     connection open
INFO:     ('127.0.0.1', 61952) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
INFO:     connection open
INFO:     127.0.0.1:50720 - "GET /api/scholarships/opp_01357e0e1a3e3b67 HTTP/1.1" 200 OK
C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\google\cloud\firestore_v1\base_collection.py:304: UserWarning: Detected filter using positional arguments. Prefer using the 'filter' keyword argument instead.
  return query.where(field_path, op_string, value)
C:\Users\HP\Documents\scholarstream-monorepo\backend\app\database.py:313: UserWarning: Detected filter using positional arguments. Prefer using the 'filter' keyword argument instead.
  .where('scholarship_id', '==', scholarship_id)\
C:\Users\HP\Documents\scholarstream-monorepo\backend\app\database.py:314: UserWarning: Detected filter using positional arguments. Prefer using the 'filter' keyword argument instead.
  .where('status', '==', 'draft')\
INFO:     127.0.0.1:50720 - "GET /api/scholarships/opp_01357e0e1a3e3b67 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54241 - "POST /api/applications/start HTTP/1.1" 200 OK   
INFO:     127.0.0.1:51955 - "POST /api/applications/start HTTP/1.1" 200 OK   
2026-05-09 11:46:04 [warning  ] Gemini call failed, retrying once [app.utils.rate_limiter] backoff_s=0.12 error=
2026-05-09 11:46:18 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=1 new_effective_rpm=15
2026-05-09 11:46:18 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=2 backoff_s=1.84 max_retries=4
2026-05-09 11:47:17 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=2 new_effective_rpm=7
2026-05-09 11:47:17 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=3 backoff_s=1.1 max_retries=4
INFO:     127.0.0.1:55691 - "POST /api/applications/start HTTP/1.1" 200 OK   
2026-05-09 11:52:20 [warning  ] No opportunities extracted     [app.services.cortex.refinery] url=https://angelhack.com/events/
2026-05-09 11:52:22 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=1 new_effective_rpm=5
2026-05-09 11:52:22 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=1 backoff_s=0.6 max_retries=4
2026-05-09 11:52:29 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=2 new_effective_rpm=5
2026-05-09 11:52:29 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=2 backoff_s=1.52 max_retries=4
2026-05-09 11:52:56 [warning  ] No opportunities extracted     [app.services.cortex.refinery] url=https://www.hackquest.io/hackathons
2026-05-09 11:54:56 [warning  ] Gemini call failed, retrying once [app.utils.rate_limiter] backoff_s=0.75 error=
2026-05-09 11:55:01 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=1 new_effective_rpm=5
2026-05-09 11:55:01 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=2 backoff_s=1.68 max_retries=4
2026-05-09 11:55:05 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=2 new_effective_rpm=5
2026-05-09 11:55:05 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=3 backoff_s=2.69 max_retries=4
2026-05-09 11:55:14 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=3 new_effective_rpm=5
2026-05-09 11:55:14 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=4 backoff_s=3.75 max_retries=4
2026-05-09 11:55:21 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=4 new_effective_rpm=5
2026-05-09 11:55:21 [error    ] Gemini call failed after all retries [app.utils.rate_limiter] last_error=Client error '429 Too Many Requests' for url 'https://aiplatform.googleapis.com/v1/projects/scholarstream-gemma4good/locations/global/endpoints/openapi/chat/completions?key=AQ.Ab8RN6IEtFkxN_BJ-JeRB-eE retries=4
2026-05-09 11:55:21 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=5 new_effective_rpm=5
2026-05-09 11:55:21 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=1 backoff_s=0.35 max_retries=4
2026-05-09 11:56:04 [warning  ] All load strategies failed     [app.services.crawler_service] attempt=1 url=https://dorahacks.io/hackathon
2026-05-09 11:56:09 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=6 new_effective_rpm=5
2026-05-09 11:56:09 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=1 backoff_s=0.38 max_retries=4
2026-05-09 11:56:17 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=7 new_effective_rpm=5
2026-05-09 11:56:17 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=2 backoff_s=0.97 max_retries=4
2026-05-09 11:56:25 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=8 new_effective_rpm=5
2026-05-09 11:56:25 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=3 backoff_s=4.24 max_retries=4
2026-05-09 11:56:38 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=9 new_effective_rpm=5
2026-05-09 11:56:38 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=4 backoff_s=8.84 max_retries=4
2026-05-09 11:56:58 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=10 new_effective_rpm=5
2026-05-09 11:56:58 [error    ] Gemini call failed after all retries [app.utils.rate_limiter] last_error=Client error '429 Too Many Requests' for url 'https://aiplatform.googleapis.com/v1/projects/scholarstream-gemma4good/locations/global/endpoints/openapi/chat/completions?key=AQ.Ab8RN6IEtFkxN_BJ-JeRB-eE retries=4
2026-05-09 11:56:58 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=11 new_effective_rpm=5
2026-05-09 11:56:58 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=2 backoff_s=0.6 max_retries=4
2026-05-09 11:57:13 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=12 new_effective_rpm=5
2026-05-09 11:57:13 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=1 backoff_s=0.3 max_retries=4
2026-05-09 11:57:22 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=13 new_effective_rpm=5
2026-05-09 11:57:22 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=2 backoff_s=3.27 max_retries=4
2026-05-09 11:57:43 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=14 new_effective_rpm=5
2026-05-09 11:57:43 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=3 backoff_s=7.17 max_retries=4
2026-05-09 11:57:55 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=15 new_effective_rpm=5
2026-05-09 11:57:55 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=4 backoff_s=4.61 max_retries=4
2026-05-09 11:58:09 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=16 new_effective_rpm=5
2026-05-09 11:58:09 [error    ] Gemini call failed after all retries [app.utils.rate_limiter] last_error=Client error '429 Too Many Requests' for url 'https://aiplatform.googleapis.com/v1/projects/scholarstream-gemma4good/locations/global/endpoints/openapi/chat/completions?key=AQ.Ab8RN6IEtFkxN_BJ-JeRB-eE retries=4
2026-05-09 11:58:09 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=17 new_effective_rpm=5
2026-05-09 11:58:09 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=3 backoff_s=2.03 max_retries=4
2026-05-09 11:58:19 [warning  ] All load strategies failed     [app.services.crawler_service] attempt=2 url=https://dorahacks.io/hackathon
2026-05-09 11:58:23 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=18 new_effective_rpm=5
2026-05-09 11:58:23 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=1 backoff_s=1.65 max_retries=4
2026-05-09 11:58:34 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=19 new_effective_rpm=5
2026-05-09 11:58:34 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=2 backoff_s=0.43 max_retries=4
2026-05-09 12:00:34 [warning  ] All load strategies failed     [app.services.crawler_service] attempt=3 url=https://dorahacks.io/hackathon
2026-05-09 12:00:34 [error    ] Direct fetch failed after all retries [app.services.crawler_service] error=Page.goto: Timeout 30000ms exceeded.
Call log:
  - navigating to "https://dorahacks.io/hackathon", waiting until "commit"   
 url=https://dorahacks.io/hackathon
2026-05-09 12:00:52 [error    ] Reader LLM extraction failed   [app.services.cortex.reader_llm] error= url=https://devfolio.co/hackathons
2026-05-09 12:00:52 [warning  ] No opportunities extracted     [app.services.cortex.refinery] url=https://devfolio.co/hackathons
2026-05-09 12:00:59 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=20 new_effective_rpm=5
2026-05-09 12:00:59 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=1 backoff_s=0.97 max_retries=4
2026-05-09 12:01:05 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=21 new_effective_rpm=5
2026-05-09 12:01:05 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=2 backoff_s=3.36 max_retries=4
2026-05-09 12:01:17 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=22 new_effective_rpm=5
2026-05-09 12:01:17 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=3 backoff_s=4.29 max_retries=4
2026-05-09 12:01:30 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=23 new_effective_rpm=5
2026-05-09 12:01:30 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=4 backoff_s=12.11 max_retries=4
2026-05-09 12:02:00 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=24 new_effective_rpm=5
2026-05-09 12:02:00 [error    ] Gemini call failed after all retries [app.utils.rate_limiter] last_error=Client error '429 Too Many Requests' for url 'https://aiplatform.googleapis.com/v1/projects/scholarstream-gemma4good/locations/global/endpoints/openapi/chat/completions?key=AQ.Ab8RN6IEtFkxN_BJ-JeRB-eE retries=4
2026-05-09 12:02:00 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=25 new_effective_rpm=5
2026-05-09 12:02:00 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=1 backoff_s=0.09 max_retries=4
2026-05-09 12:02:07 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=26 new_effective_rpm=5
2026-05-09 12:02:07 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=1 backoff_s=1.45 max_retries=4
