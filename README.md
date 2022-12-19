## QuizSoda

<img src='static/logo.png' width=100px>  

Hello there! QuizSoda is a highly simplified quiz/CTF platform.  

Written in:
- Frontend: Bootstrap
- Backend: Flask
- Language: Python
- DB: SQL (SQLite)

We have reached beta stage.

## Documentation

None. Zero docs. Go figure it out yourself.

```python
if __name__ == '__main__':
    # resetAll()
    app.run(port=5000, host='0.0.0.0', debug=True)
```

Setup: Follow the challenge upload guide and then uncomment `resetAll()`.  
Once done, you can comment it out again. (Up to you: anyway debug is still on...)

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