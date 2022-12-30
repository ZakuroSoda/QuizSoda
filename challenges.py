import sqlite3
import os

DOWNLOAD_FILE_TEMPLATE = """
<div class="g-1 row my-4">
    <a href="/files/{id}" style="width: 100%;" class="btn btn-outline-info" download>Download Challenge Files</a>
</div>
"""
MODAL_TEMPLATE = """
<div class="modal fade" id="{id}" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content rounded-4 shadow">
        <div class="modal-body p-5">
          <h2 class="fw-bold mb-0">{title}</h2>
          <h5>{points} points - {solves} solves</h5>
          <ul class="d-grid gap-4 my-4 list-unstyled">
            <li class="d-flex gap-4">
              <div>
                {description}
              </div>
            </li>
          </ul>
          {file_template}
          <div class="g-1 row">
            <div class="col-md-7">
                <form action="/challenges/{id}" method="POST">
                  <input name="answer" type="text" class="form-control" id="answer" placeholder="answer" required> 
            </div>
            <div class="col-md-3">
                  <button type="submit" style="width: 100%;" class="btn btn-outline-primary">Submit</button>
                </form>
              </div>
            <div class="col-md-2">
                <button type="button" style="width: 100%;" data-bs-dismiss="modal" class="btn btn-outline-danger">Close</button>
            </div>
          </div>
        </div>
      </div>
    </div>
</div>
"""
CARD_TEMPLATE = """
<div class="col-sm mx-3">
    <div class="card px-3" style="width: 18rem;" {{% if '{id}' in solvedChallenges %}}solved{{% endif %}}>
        <div class="card-body">
            <h5 class="card-title">{title}</h5>
            <p class="card-text">{points}</p>
        </div>
        <a href="" data-bs-toggle="modal" data-bs-target="#{id}" class="stretched-link"></a>
    </div>
</div>
"""
MAIN_TEMPLATE = """
{{% include 'basehead.html' %}}
<div class="container">
{alerts}
{cards}
{modals}
</div>
</body>
</html>
"""
ALERT_TEMPLATE = """
<div class="alert alert-{{alertType}} alert-dismissible my-5" role="alert" {% if not alertType %}hidden{% endif %}>
    <div>{{alertMessage}}</div>
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
</div>
"""

def initDatabaseFromFiles():
    con = sqlite3.connect('./db/challenges.db')
    cur = con.cursor()
    categories = os.listdir('./challenges')
    for category in categories:
        cur.execute(f"DROP TABLE IF EXISTS '{category}'")
        cur.execute(f"CREATE TABLE '{category}' (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, answer TEXT NOT NULL, points INTEGER NOT NULL, solves INTEGER NOT NULL DEFAULT 0, files BIT NOT NULL DEFAULT 0)")
        con.commit()
        
        challenges = os.listdir(f'./challenges/{category}')
        for challenge in challenges:
            title = challenge
            description = open(f'./challenges/{category}/{challenge}/DESCRIPTION', 'r').read()
            answer = open(f'./challenges/{category}/{challenge}/ANSWER', 'r').read()
            points = int(open(f'./challenges/{category}/{challenge}/POINTS', 'r').read())
            cur.execute(f"INSERT INTO '{category}' (title, description, answer, points) VALUES (?, ?, ?, ?)", (title, description, answer, points))
            con.commit()

            if os.path.isfile(f'./challenges/{category}/{challenge}/dist.zip'):
                cur.execute(f"UPDATE '{category}' SET files=1 WHERE title=?", (title,))
                con.commit()

### only run initDatabaseFromFiles() if you have edited the files in the challenges folder, otherwise you can just edit the database directly

def createModalsFromDatabase():
    con = sqlite3.connect('./db/challenges.db')
    cur = con.cursor()

    cur.execute("SELECT name FROM sqlite_schema WHERE name!='sqlite_sequence'")
    categoriesRaw, categories = cur.fetchall(), []

    for i in range(len(categoriesRaw)):
        categories.append(categoriesRaw[i][0])
    
    all_modal_templates = """"""

    for category in categories:
        cur.execute(f"SELECT id, title, description, points, solves, files FROM '{category}'")
        challenges = cur.fetchall()
        for challenge in challenges:
            template = MODAL_TEMPLATE.format(
                id=f"{category.replace(' ','_')}-{challenge[0]}",
                title=challenge[1],
                description=challenge[2],
                points=challenge[3],
                solves=challenge[4],
                file_template="{file_template}"
            )

            if challenge[5] == 1:
                template = template.replace("{file_template}", DOWNLOAD_FILE_TEMPLATE.format(id=f"{category.replace(' ','_')}-{challenge[0]}"))
            else:
                template = template.replace("{file_template}", "")

            all_modal_templates += template

    return all_modal_templates

def createCardsFromDatabase():
    ### This is how the cards should be like
    ### CATEGORY NAME
    ### CARD 1 CARD 2 CARD 3
    ### CARD 4 CARD 5 CARD 6
    ### CARD 7 (blank col) (blank col)

    con = sqlite3.connect('./db/challenges.db')
    cur = con.cursor()

    cur.execute("SELECT name FROM sqlite_schema WHERE name!='sqlite_sequence'")
    categoriesRaw, categories = cur.fetchall(), []

    for i in range(len(categoriesRaw)):
        categories.append(categoriesRaw[i][0])
    
    all_cards = []

    for i in range(len(categories)):
        all_cards.append([])

        cur.execute(f"SELECT id, title, points FROM '{categories[i]}' ORDER BY points")
        challenges = cur.fetchall()

        for challenge in challenges:
            template = CARD_TEMPLATE.format(
              id=f"{categories[i].replace(' ','_')}-{challenge[0]}",
              title=challenge[1],
              points=challenge[2]
            )
            all_cards[i].append(template)
    
    ### Start of UI row and column magic ###

    all_categories_all_cards = []

    for i in range(len(categories)):
        categoryTitle = f"""
<div class="row mx-3 my-5">
    <h1>Category: {categories[i]}</h1>
</div>
"""
        counter = 0
        categoryCardsAll = categoryTitle

        indexOfBeginningOfLastRow = len(all_cards[i])-(len(all_cards[i])%3)
        if indexOfBeginningOfLastRow == len(all_cards[i]):
            indexOfBeginningOfLastRow = indexOfBeginningOfLastRow-3

        for j in range(len(all_cards[i])):

            if j == indexOfBeginningOfLastRow:
                break

            counter += 1

            if counter == 1:
                categoryCardsAll += '\n<div class="row my-5">\n'
            
            categoryCardsAll += all_cards[i][j]

            if counter == 3:
                categoryCardsAll += '\n</div>\n'
                counter = 0
            
        if len(all_cards[i])%3 == 1:
            categoryCardsAll += f"""
<div class="row my-5">
{all_cards[i][j]}
<div class="col-sm mx-3"></div>
<div class="col-sm mx-3"></div>

</div>
"""
        elif len(all_cards[i])%3 == 2:
            categoryCardsAll += f"""
<div class="row my-5">
{all_cards[i][j]}
{all_cards[i][j+1]}
<div class="col-sm mx-3"></div>

</div>
"""
        else:
            categoryCardsAll += f"""
<div class="row my-5">
{all_cards[i][j]}
{all_cards[i][j+1]}
{all_cards[i][j+2]}

</div>
"""
        all_categories_all_cards.append(categoryCardsAll)

    return all_categories_all_cards

def assembleChallengePage():
    ALL_CATEGORIES_ALL_CARDS = createCardsFromDatabase()
    ALL_MODAL_TEMPLATES = createModalsFromDatabase()

    ALL_CARD_TEMPLATES = """"""
    for category in ALL_CATEGORIES_ALL_CARDS:
        ALL_CARD_TEMPLATES += category
    #This joins all the cards (separated by category) into one long string

    FINAL = MAIN_TEMPLATE.format(
      cards=ALL_CARD_TEMPLATES,
      modals=ALL_MODAL_TEMPLATES,
      alerts=ALERT_TEMPLATE
    )
    
    return FINAL

def checkAnswer(id, answer):
    # the id will be in the format of category-challengeid
    # for example: web-1 or binary_exploitation-2

    category, challengeid = id.split('-')[0].replace('_',' '), id.split('-')[1]

    con = sqlite3.connect('./db/challenges.db')
    cur = con.cursor()

    cur.execute(f"SELECT answer, points FROM '{category}' WHERE id=?", (challengeid,))
    result = cur.fetchone()
    correctAnswer, points = result[0], result[1]

    if answer == correctAnswer:
        return points
    else:
        return 0

def updateChallengeSolves(id):
    category, challengeid = id.split('-')[0].replace('_',' '), id.split('-')[1]

    con = sqlite3.connect('./db/challenges.db')
    cur = con.cursor()

    cur.execute(f"UPDATE '{category}' SET solves=solves+1 WHERE id=?", (challengeid,))
    con.commit()

def getFileLocation(id):
    category, challengeid = id.split('-')[0].replace('_',' '), id.split('-')[1]

    con = sqlite3.connect('./db/challenges.db')
    cur = con.cursor()

    cur.execute(f"SELECT title FROM '{category}' WHERE id=? AND files=1", (challengeid,))

    try: 
        title = cur.fetchone()[0]
        path = f"./challenges/{category}/{title}/dist.zip"
        return path
    except:
        return None

def resetChallengeSolves():
    con = sqlite3.connect('./db/challenges.db')
    cur = con.cursor()

    cur.execute("SELECT name FROM sqlite_schema WHERE name!='sqlite_sequence'")
    categoriesRaw, categories = cur.fetchall(), []

    for i in range(len(categoriesRaw)):
        categories.append(categoriesRaw[i][0])

    for category in categories:
        cur.execute(f"UPDATE '{category}' SET solves=0")
        con.commit()
