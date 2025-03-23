from flask import Flask, request, jsonify, session
from flask_cors import CORS
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-key")
CORS(app)

# the AJAX request will be sent to this route, and the flask will send back the initial starting values
@app.route("/start_game", methods=["POST"])
def start_game():
    # get the data from the frontend
    data = request.json 

    # get the individual costs for each choice they made
    apartment_cost = data.get("apartment", 600)
    internet_cost = data.get("internet", 60)

    # create the json data
    session['state'] = {
        "balance": 5000,
        "happiness": 100,
        "day": 1,
        "round": 1,
        "fixed_expenses": {
            "apartment": apartment_cost,
            "internet": internet_cost
        },
        "log": []
    }

    # return the json data
    return jsonify({"state": session['state']})


# this route is called when the user clicks the next button
@app.route("/next_round")
def next_round():
    state = session.get("state", {})

    # variable expenses (expected)
    food_choices = [
        {"label": "Cook at home", "cost": 15, "happiness": 0},
        {"label": "Eat out", "cost": 30, "happiness": 1},
        {"label": "Leftovers", "cost": 7, "happiness": -1}
    ]

    entertainment_choices = [
        {"label": "Stream a movie", "cost": 10, "happiness": 0},
        {"label": "Stay at home", "cost": 0, "happiness": -1},
        {"label": "Go out with your friends", "cost": 20, "happiness": 1}
        
    ]

    transport_choices = [
        {"label": "Public Transport", "cost": 10, "happiness": 0},
        {"label": "Bike Around", "cost": 5, "happiness": -1},
        {"label": "Take An Uber", "cost": 15, "happiness": 1}
    ]


    # variable expenses (random events)

    RANDOM_EVENTS = [
        {
            "type": "energy",
            "options": [
                {"label": "Lower Heat", "cost": 15, "happiness": -5},
                {"label": "Keep it Comfortable", "cost": 0, "happiness": 0},
                {"label": "Crank it Up", "cost": 20, "happiness": 5}
            ]
        },
        {
            "type": "grocery",
            "options": [
                {"label": "Warehouse Bulk Buy", "cost": 100, "happiness": 0},
                {"label": "Normal Shopping", "cost": 50, "happiness": 0},
                {"label": "Fancy Organic", "cost": 80, "happiness": 5}
            ]
        },
        {
            "type": "social",
            "options": [
                {"label": "Fancy Dinner", "cost": 75, "happiness": 10},
                {"label": "Skip Dinner", "cost": 0, "happiness": -5},
                {"label": "Host a Potluck", "cost": 20, "happiness": 5}
            ]
        }
    ]

    # select an event randomly
    random_event = random.choice(RANDOM_EVENTS)


    
    return jsonify({
        "day": state.get("day", 1),
        "balance": state.get("balance", 0),
        "happiness": state.get("happiness", 0),
        "choices": {
            "food" : food_choices,
            "entertainment": entertainment_choices,
            "transport": transport_choices
        },
        "random_event": random_event
    })

# every time the user makes the choice, the js will call this route to update the game stats (happiness, balance, etc) based on the choice 
@app.route("/submit_choice", methods=["POST"])
def submit_choice():
    # get the user's selected choice (like what they clicked)
    data = request.json
    choice = data.get("choice")
    state = session.get("state")

    # update the game state based on the user's choice        
    state["happiness"] += choice.get("happiness", 0)
    state["day"] += 3
    state["round"] += 1
    total_cost = choice.get("cost", 0)

    # subtract the fixed expenses every 3 rounds 
    if state["round"] % 3 == 0:
        total_cost += sum(state["fixed_expenses"].values())

    state["balance"] -= total_cost


    # return the updated game state to the user's choice
    session["state"] = state
    return jsonify(state)


if __name__ == "__main__":
    app.run(debug=True)
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port)


    
