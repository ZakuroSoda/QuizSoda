import sqlite3
import os


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
          <div class="g-1 row">
            <div class="col-md-7">
                <form action="/{id}" method="POST">
                  <input type="text" class="form-control" id="answer" placeholder="answer" required> 
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

def initDatabaseFromFiles():
    con = sqlite3.connect('./db/challenges.db')
    cur = con.cursor()
    categories = os.listdir('./challenges')
    for category in categories:
        cur.execute(f"DROP TABLE IF EXISTS '{category}'")
        cur.execute(f"CREATE TABLE '{category}' (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT NOT NULL, answer TEXT NOT NULL, points INTEGER NOT NULL, solves INTEGER NOT NULL DEFAULT 0)")
        con.commit()
        
        challenges = os.listdir(f'./challenges/{category}')
        for challenge in challenges:
            title = challenge
            description = open(f'./challenges/{category}/{challenge}/DESCRIPTION', 'r').read()
            answer = open(f'./challenges/{category}/{challenge}/ANSWER', 'r').read()
            points = int(open(f'./challenges/{category}/{challenge}/POINTS', 'r').read())
            cur.execute(f"INSERT INTO '{category}' (title, description, answer, points) VALUES (?, ?, ?, ?)", (title, description, answer, points))
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
        cur.execute(f"SELECT id, title, description, points, solves FROM '{category}'")
        challenges = cur.fetchall()
        for challenge in challenges:
            template = MODAL_TEMPLATE.format(
                id=f"{category.replace(' ','_')}-{challenge[0]}",
                title=challenge[1],
                description=challenge[2],
                points=challenge[3],
                solves=challenge[4]
            )

            all_modal_templates += template

    return all_modal_templates


print(createModalsFromDatabase())