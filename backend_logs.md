HP@Emrash MINGW64 ~/Documents/scholarstream-monorepo/backend (hackathon-final)
$ python run.py
[INFO] Checking Port 8081 availability...
[INFO] Port is free and bindable.
[INFO] Environment variables loaded from .env
==> Starting ScholarStream FastAPI Backend...
==> Server will run at: http://localhost:8081
==> Auto-reload DISABLED for stability
2026-05-09 12:17:58 [info     ] OpportunityScraperService: CORTEX MODE ACTIVE legacy_scrapers=REMOVED message=All discovery via Playwright-based Sentinel patrols
2026-05-09 12:17:59 [info     ] Firebase initialized successfully
2026-05-09 12:18:00 [info     ] AdaptiveRateLimiter initialized max_concurrent=5 max_retries=4 max_rpm=30
2026-05-09 12:18:03 [info     ] Gemma AI initialized with Cloud ADC project_id=scholarstream-gemma4good
2026-05-09 12:18:03 [info     ] ScholarStream is running on GEMMA 4 NATIVE ENGINE
2026-05-09 12:18:03 [info     ] Firebase already initialized  
2026-05-09 12:18:03 [info     ] ⚡ GEMMA NATIVE ENGINE ACTIVE (Hackathon Mode)
INFO:     Started server process [10040]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8081 (Press CTRL+C to quit)
INFO:     ('127.0.0.1', 63930) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:06 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 65386) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:08 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 59606) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:10 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 60915) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:11 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 60179) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:12 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 54704) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:12 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     connection closed
2026-05-09 11:18:18 [error    ] Pulse: Announcement failed     [app.services.discovery_pulse] error=WRONGPASS invalid or missing auth token. See https://docs.upstash.com/redis/troubleshooting/http_unauthorized for details.
INFO:     ('127.0.0.1', 59314) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:18 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     ('127.0.0.1', 52154) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:18 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     ('127.0.0.1', 58525) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:18 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     ('127.0.0.1', 64376) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:20 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 63246) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:20 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 64583) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:20 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 63450) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:21 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 58592) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:22 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     ('127.0.0.1', 58021) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:22 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 56733) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:22 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     connection closed
INFO:     connection closed
INFO:     ('127.0.0.1', 56913) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:24 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 64289) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:24 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 56213) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:24 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 53127) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:25 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 56719) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:26 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 58407) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:26 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 57905) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:27 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 62963) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:28 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 53139) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:28 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 55998) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:28 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 60076) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:29 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 53741) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:30 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 59268) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:30 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 61883) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:31 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 57110) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:18:32 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 65066) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:32 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 65177) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:18:32 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 62569) - "WebSocket /ws/opportunities?token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImY1MzMwMzNhMTMzYWQyM2EyYzlhZGNmYzE4YzRlM2E3MWFmYWY2MjkiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc2Nob2xhcnN0cmVhbS1pNGkiLCJhdWQiOiJzY2hvbGFyc3RyZWFtLWk0aSIsImF1dGhfdGltZSI6MTc2NjUyMTY4MiwidXNlcl9pZCI6IkVMM0dGS1UxdmJRWUlPNkdkRDFITmNNU0RBYjIiLCJzdWIiOiJFTDNHRktVMXZiUVlJTzZHZEQxSE5jTVNEQWIyIiwiaWF0IjoxNzcxNTE1NTQ1LCJleHAiOjE3NzE1MTkxNDUsImVtYWlsIjoib2dhbUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsib2dhbUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.2cAF444QSuJMZ8e1sYgk2O2ERTICp3Dlj3qN09zCelYlicqBspLOfphxbnrD9Myd-m6mRcbTPpx_wAvP7sLh_Mp9myLI9pGtYS3nKTpPeeBD2yrhAvPO3J0EvqGooZ5yOv6WRzjLYzbKKiXkXYcOFre3Cm62KAn9f3pnRbVy4A8n2aPb6ibcl7g9UF2WavqYd_1k0P7gQCoPw0DBN_4h-X9KLuuc1QV7gjMFJngpHhVW3qfMzTanBg9pGrjuMTMi80rACtfZroVpibZm8vqzvotxqevICVXCs5uOVtBhbzdOqRURbZZnQldXTDXcUneUnlb-3UeXqXl2BFsFLHeoig" [accepted]     
2026-05-09 11:20:06 [error    ] Token verification failed      [app.routes.websocket] error=Firebase ID token has incorrect "aud" (audience) claim. Expected "scholarstream-gemma4good" but got "scholarstream-i4i". Make sure the ID token comes from the same Firebase project as the service account used to authenticate this SDK. See https://firebase.google.com/docs/auth/admin/verify-id-tokens for details on how to retrieve ID token.
INFO:     ('127.0.0.1', 50565) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:06 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection closed
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 330, in asgi_send
    await self.send(data)  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\websockets\legacy\protocol.py", line 635, in send
    await self.ensure_open()
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\websockets\legacy\protocol.py", line 944, in ensure_open
    raise self.connection_closed_exc()
websockets.exceptions.ConnectionClosedError: no close frame received or sent 

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\websockets.py", line 85, in send
    await self._send(message)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\_exception_handler.py", line 39, in sender
    await send(message)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 343, in asgi_send
    raise ClientDisconnected from exc
uvicorn.protocols.utils.ClientDisconnected

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 242, in run_asgi
    result = await self.app(self.scope, self.asgi_receive, self.asgi_send)  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\uvicorn\middleware\proxy_headers.py", line 60, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\fastapi\applications.py", line 1054, in __call__
    await super().__call__(scope, receive, send)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\applications.py", line 113, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\middleware\errors.py", line 152, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\middleware\base.py", line 101, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\middleware\cors.py", line 77, in __call__
    await self.app(scope, receive, send)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\middleware\exceptions.py", line 62, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send) 
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\routing.py", line 715, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\routing.py", line 735, in app
    await route.handle(scope, receive, send)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\routing.py", line 362, in handle
    await self.app(scope, receive, send)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\routing.py", line 95, in app
    await wrap_app_handling_exceptions(app, session)(scope, receive, send)   
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\routing.py", line 93, in app
    await func(session)
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\fastapi\routing.py", line 383, in app
    await dependant.call(**solved_result.values)
  File "C:\Users\HP\Documents\scholarstream-monorepo\backend\app\routes\websocket.py", line 513, in websocket_endpoint
    await websocket.send_json({
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\websockets.py", line 175, in send_json
    await self.send({"type": "websocket.send", "text": text})
  File "C:\Users\HP\.conda\envs\scholarstream\Lib\site-packages\starlette\websockets.py", line 88, in send
    raise WebSocketDisconnect(code=1006)
starlette.websockets.WebSocketDisconnect
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 57974) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:06 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 49248) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:08 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 64451) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:08 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 61590) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:10 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 60923) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:10 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 59060) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:12 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 61229) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:12 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 56302) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:14 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 58935) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:14 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 53516) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:16 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 55289) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:16 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
2026-05-09 11:20:17 [warning  ] Rate limiter adapting DOWN     [app.utils.rate_limiter] consecutive_429s=1 new_effective_rpm=15
2026-05-09 11:20:17 [warning  ] Gemini 429 — backing off       [app.utils.rate_limiter] attempt=1 backoff_s=2.0 max_retries=4
INFO:     ('127.0.0.1', 60185) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:18 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 57389) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:18 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 49676) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:20 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 57093) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:20 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 57259) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:22 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 62378) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:22 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 63288) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:24 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 56892) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:24 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 53225) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:26 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 54434) - "WebSocket /ws/opportunities?token=GUEST_TOKEN" [accepted]
2026-05-09 11:20:26 [error    ] Token verification failed      [app.routes.websocket] error=Wrong number of segments in token: b'GUEST_TOKEN'
INFO:     connection open
INFO:     connection closed
