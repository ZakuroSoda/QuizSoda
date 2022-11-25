import os



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

allChallenges = []

for category in os.listdir('./challenges'):
    for challenge in os.listdir(f'./challenges/{category}'):
        try:
            allChallenges.append(Challenge(
                category,
                challenge, 
                open(f'./challenges/{category}/{challenge}/DESCRIPTION', 'r').read(), 
                open(f'./challenges/{category}/{challenge}/FLAG', 'r').read(),
                int(open(f'./challenges/{category}/{challenge}/POINTS', 'r').read())
            ))
        except Exception as e:
            print(e)

