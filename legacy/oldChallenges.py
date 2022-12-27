import os

'''
This was an old script to generate the webpage statically before running the main flask app.
However it has been revamped and refactored into a much more readable, concise, and logical script which gives me confidence.
Confidence to generate the page dynamically on load.
'''

class Challenge:

    CHALLENGEID = 1
    
    def __init__(self, category, title, description, flag, points):
        self.category, self.title, self.description, self.flag, self.points = category, title, description, flag, points

        self.id = f'challenge-{Challenge.CHALLENGEID}'
        Challenge.CHALLENGEID += 1

        self.solves = 0

    def create_card(self) -> str:
        template = f"""
<div class="col-sm mx-3">
    <div class="card px-3" style="width: 18rem;">
        <div class="card-body">
            <h5 class="card-title">{self.title}</h5>
            <p class="card-text">{self.points}</p>
        </div>
        <a href="" data-bs-toggle="modal" data-bs-target="#{self.id}" class="stretched-link"></a>
    </div>
</div>
        """
        return template
        
    def create_modal(self) -> str:
        template = f"""
<div class="modal fade" id="{self.id}" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content rounded-4 shadow">
        <div class="modal-body p-5">
          <h2 class="fw-bold mb-0">{self.title}</h2>
          <h5>{self.points} points - {self.solves} solves</h5>
          <ul class="d-grid gap-4 my-4 list-unstyled">
            <li class="d-flex gap-4">
              <div>
                {self.description}
              </div>
            </li>
          </ul>
          <div class="g-1 row">
            <div class="col-md-7">
                <form action="/{self.id}" method="POST">
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
        return template

def initialise():
    allChallenges = []

    global categories
    categories = os.listdir('./challenges')

    challengesPerCategory = {}

    for category in categories:
        challengeCounter = 1
        for challenge in os.listdir(f'./challenges/{category}'):
            try:
                allChallenges.append(Challenge(
                    category,
                    challenge, 
                    open(f'./challenges/{category}/{challenge}/DESCRIPTION', 'r').read(), 
                    open(f'./challenges/{category}/{challenge}/FLAG', 'r').read(),
                    int(open(f'./challenges/{category}/{challenge}/POINTS', 'r').read())
                ))
                challengesPerCategory[category] = challengeCounter
                challengeCounter += 1
            except Exception as e:
                print(e)

    return allChallenges

ALL_CHALLENGES = initialise()

def generate_page():

    ##### START OF CARD GENERATOR #####

    ### Do not touch this disgusting code and solution ###

    cards, working = [], []
    prevCategory = categories[0]

    for i in range(len(ALL_CHALLENGES)):
        card = ALL_CHALLENGES[i].create_card()
        working.append(card)

        if i != len(ALL_CHALLENGES)-1:
            if prevCategory != ALL_CHALLENGES[i+1].category:
                prevCategory = ALL_CHALLENGES[i+1].category
                cards.append(working)
                working = []
        else: #on the last chall
            cards.append(working)
            working = [] # not needed, for standardisation

    ### This is how cards is organised: [[challenge with cat 1, challenge with cat 1], [challenge with cat 2, challenge with cat 2, challenge with cat 2]]
    ### Do not touch this disgusting code and solution ###

    ALL_CARDS = [] # not a constant but do I care
    ALL_MODALS = [] # again idc

    ### Generate Cards
    for i in range(len(categories)):
        categorySTRING = f"""
<div class="row mx-3 my-5">
    <h1>Category: {categories[i]}</h1>
</div>

<div class="row my-5">
"""        

        cardsOfChallengesInThisCategory = cards[i]
        counter = 0
        
        # forgive me lord for I have sinned with this solution
        indexOfBeginningOfLastRow = len(cardsOfChallengesInThisCategory)-(len(cardsOfChallengesInThisCategory)%3)
        # what are my var names lmao
        if indexOfBeginningOfLastRow == len(cardsOfChallengesInThisCategory):
            indexOfBeginningOfLastRow = indexOfBeginningOfLastRow-3
        
        for j in range(len(cardsOfChallengesInThisCategory)):

            categorySTRING += cardsOfChallengesInThisCategory[j] + '\n'
            counter += 1

            if j == indexOfBeginningOfLastRow:
                break
            
            if counter == 3:
                categorySTRING += '</div>\n<div class="row my-5">'
                counter = 0
        
        if (len(cardsOfChallengesInThisCategory) % 3) == 1:

            categorySTRING += """
<div class="col-sm mx-3"></div>
<div class="col-sm mx-3"></div>
</div>
"""
        elif (len(cardsOfChallengesInThisCategory) % 3) == 2:
            
            categorySTRING += cardsOfChallengesInThisCategory[j+1] + '\n'
            categorySTRING += """
<div class="col-sm mx-3"></div>
</div>
"""
        else:
            categorySTRING += cardsOfChallengesInThisCategory[j+1] + '\n'
            categorySTRING += cardsOfChallengesInThisCategory[j+2] + '\n'
            categorySTRING += '</div>\n'
                

        ALL_CARDS.append(categorySTRING)

    ##### END OF CARD GENERATOR #####

    ##### START OF MODAL GENERATOR #####
    for i in range(len(ALL_CHALLENGES)):
        modal = ALL_CHALLENGES[i].create_modal()
        ALL_MODALS.append(modal)
    ##### END OF MODAL GENERATOR
    
    ##### START FINAL ASSEMBLY #####
    START = """
{% include 'baseHeadNoLogin.html' %}
<div class="container">
"""
    END = """
</div>
</body>
</html>    
"""

    FINAL = START

    for categoryCards in ALL_CARDS:
        FINAL += categoryCards
    for modal in ALL_MODALS:
        FINAL += modal

    FINAL += END

    generatedTemplate = open("./templates/generatedTemplate.html", "w")
    generatedTemplate.write(FINAL)
    generatedTemplate.close()

if __name__ == '__main__':
    generate_page()
