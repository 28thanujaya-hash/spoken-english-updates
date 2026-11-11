# Lessons (downloaded by the app)
The app reads `lessons/index.json`, then the week files listed there, from this public repo
(raw.githubusercontent.com). Change a lesson here and the app picks it up next time it opens — no app update needed.
Edit `make_lessons.py` and run it to regenerate the JSON; bump `V` so the app shows "New lessons".
