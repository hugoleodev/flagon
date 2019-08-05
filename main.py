from flagon import Flagon

app = Flagon()


@app.route("/")
def home(request, response):
    response.text = "Minha Home"

    return response


@app.route("/users")
class UsersResource:
    def get(self, request, response):
        response.text = "GET Users"

    def post(self, request, response):
        response.text = "POST Users"
