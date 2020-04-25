from flask import Flask,jsonify

app = Flask(__name__)

@app.route("/")
def climate():
    return (f'Welcome to Hawaii')

@app.route("/api/v1.0/precipitation")
def precip():
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= past_year).all()
    precip = {date: prcp for date, prcp in query}
    return jsonify(precip)


