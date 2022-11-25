import os
from math import ceil

class Challenge:

    CHALLENGEID = 1
    
    def __init__(self, category, title, description, flag, points):
        self.category, self.title, self.description, self.flag, self.points = category, title, description, flag, points

        self.id = Challenge.CHALLENGEID
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

    return allChallenges, challengesPerCategory



ALL_CHALLENGES, CHALLENGES_PER_CATEGORY = initialise()



def generate_page():
    for category in categories:
        head = f"""
<div class="row mx-3 my-5">
    <h1>Category: {category}</h1>
</div>
"""
        rows = ceil(CHALLENGES_PER_CATEGORY[category] / 3)
        finalRowCards = CHALLENGES_PER_CATEGORY[category] % 3
        cards = []

        for i in range(rows):
            if i+1 != rows: #not on final row yet
                for challenge in ALL_CHALLENGES
### LEFT OFF HERE ###

    finalTemplate = """
{% include 'baseHeadNoLogin.html' %}
<div class="container">
    {head}
    <div class="row my-5">
        <div class="col-sm mx-3">
            <div class="card px-3" style="width: 18rem;">
                <div class="card-body">
                  <h5 class="card-title">Challenge Name</h5>
                  <p class="card-text">500</p>
                </div>
                <a href="" data-bs-toggle="modal" data-bs-target="#exampleModal" class="stretched-link"></a>
            </div>
        </div>
        <div class="col-sm mx-3"></div>
        <div class="col-sm mx-3"></div>
    </div>

  {modal}
  {modal}
  {modal}

</div>
</body>
</html>   
"""
