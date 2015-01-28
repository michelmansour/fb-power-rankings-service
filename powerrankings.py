from flask import Flask, request, jsonify, abort
from fbpowerrankings import WeeklyRankings, SeasonRankings

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, world!"


def rankings(request, powerRankings):
    if (not request.json or
            'username' not in request.json or
            'password' not in request.json):
        abort(400)
    username = request.json['username']
    password = request.json['password']

    powerRankings.loginESPN(username, password)
    rankings = powerRankings.powerRankings()

    return jsonify({'rankings': rankings}), 200


def lowerBetter(request):
    if request.json:
        return request.json['lowerBetterCategories']
    else:
        abort(400)


@app.route(
    '/powerrankings/weekly/<string:leagueId>/<string:seasonId>/<int:weekNumber>',
    methods=['POST'])
def weeklyRankings(leagueId, seasonId, weekNumber):
    return rankings(request, WeeklyRankings(leagueId, seasonId,
                                            lowerBetter(request),
                                            weekNumber))


@app.route('/powerrankings/season/<string:leagueId>/<string:seasonId>',
           methods=['POST'])
def seasonRankings(leagueId, seasonId):
    return rankings(request, SeasonRankings(leagueId, seasonId,
                                            lowerBetter(request)))


if __name__ == '__main__':
    app.run(debug=True)
