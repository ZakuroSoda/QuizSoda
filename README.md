## QuizSoda

<img src='static/logo.png' width=100px>  

Hello there! QuizSoda is meant to be a highly simplified quiz/CTF platform.  

We are written in flask, with all of our storage done with SQLite.

We are still in development.

# Challenge Upload Guide

Upload challenges with the following format.

```
└── challenges
    ├── category
        └── challenge name
            ├── DESCRIPTION
            ├── FLAG
            ├── POINTS (only if dynamic scoring fails)
            ├── HINTS (optional) [NOT FUNCTIONAL YET]
            └── dist
                └── files to be released (no folders allowed, please zip archive if needed)
```

> Apologies but for now no distribution of files and web challenges are functional.  
> After all this is a quiz platform!