#import
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def home():
    return (
        f'Available routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/&lt;start&gt; in YYYY-MM-DD format<br/>' 
        f'/api/v1.0/&lt;start&gt;/&lt;end&gt; in YYYY-MM-DD format<br/>')

@app.route("/api/v1.0/precipitation")
def precip():
    """Return a list of precipitations from last year"""
    past_year = dt.date(2017,8,23)- dt.timedelta(days=365)
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= past_year).all()
    precip = {date: prcp for date, prcp in query}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    station_query = session.query(Measurement.station).group_by(Measurement.station).all()
    stn = list(np.ravel(station_query))
    return jsonify(stn)

@app.route("/api/v1.0/tobs")
def temperature():
#     """Query the dates and temperature observations of the most active station for the last year of data.
#     Return a JSON list of temperature observations (TOBS) for the previous year."""
    past_year = dt.date(2017,8,23)- dt.timedelta(days=365)
    temp_obs = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= past_year).filter(Measurement.station == 'USC00519281').all()
    temp = {date: tobs for date, tobs in temp_obs}
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def start(start=None):
#    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start range.
#    Calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date."""
    trip_start=session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    start_dict = list(np.ravel(trip_start))
    return jsonify(start_dict)


@app.route("/api/v1.0/<start>/<end>")
# """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
#    Calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive."""
def calc_temps(start, end):
    t = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(t)


if __name__=="__main__":
    app.run(debug=True)