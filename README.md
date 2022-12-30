## QuizSoda

<img src='static/logo.png' width=100px><img src='static/logo.png' width=100px><img src='static/logo.png' width=100px>  

Hello there! QuizSoda is a highly simplified quiz/CTF platform.  

<img src="https://img.shields.io/badge/Stage-Beta-60B932?style=plastic"><img src="https://img.shields.io/badge/-Flask%202.2.x-black?logo=flask&style=plastic"><img src="https://img.shields.io/badge/-SQLite%203.x-003B57?logo=SQLite&style=plastic">

---

Written in:
- Frontend: Bootstrap
- Backend: Flask
- Language: Python
- DB: SQL (SQLite)

We have reached beta stage.

## Documentation

1. Run `setup.py`.
```bash
python3 setup.py
```
2. Run `app.py`
```bash
python3 app.py
```
3. Check `http://127.0.0.1:5000/`

### Challenge Upload Guide

Upload challenges with the following format.

```
└── challenges
    ├── category
        └── challenge name
            ├── DESCRIPTION
            ├── FLAG
            ├── POINTS
            └── dist.zip (optional)
     ├── category
        └── challenge name
            ├── DESCRIPTION
            ├── FLAG
            └── POINTS
```

### Gallery

<img src="./docs/home.PNG">
<img src="./docs/register.PNG">
<img src="./docs/login.PNG">
<img src="./docs/ChallengesBefore.PNG">
<img src="./docs/ChallengesAfter.PNG">
<img src="./docs/ChallengeModal.PNG">
<img src="./docs/Leaderboard.PNG">
<img src="./docs/Account.PNG">
