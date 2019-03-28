# Here we GO! Let's see how much I can F*** this up.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# Let's make an engine and connect to some shit. 
engine = create_engine("sqlite:///Homework/Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our link from this script to Hawaii
# Thank god long distance charges are a thing of the past (mostly)
session = Session(engine)

#################################################
# Flask Setup
#################################################
# name our application. Given that this HW made me wanna drink a gallon of wine...
torture = Flask(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# HOME ROUTE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@torture.route("/")
def welcome():
    return (
        f"Puppies are much better than homework as a general.<br/>"
        f"Root canals are better than this homework fur sure. <br/><br/>"
        f"But here are some routes that may be of interest to you:<br/>"
        f"Want to see the precipitation in the past year, then clicky on over to:<br/>"
        f"\t/api/v1.0/precipitation<br/><br/>"
        f"Check out the stations we be samplin' from:<br/>"
        f"\t/api/v1.0/stations<br/><br/>"
        f"Sometimes it's nice to know the temperatures. Take a look here:<br/>"
        f"\t/api/v1.0/tobs<br/><br/>"
        f"Interested in knowing the minimum, maximum, and average temperatures? Then just enter add a date at the end\
            and we'll show you that data from that date onward (e.g. /api/v1.0/2011-01-01):<br/>"
        f"\t/api/v1.0/<start><br/><br/>"
        f"Planning a trip and want to see the minimum, maximum, and average temperatures during that season?\
            Just enter a date range and get the data (e.g. /api/v1.0/2011-01-01/2012-12-12):<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# It's raining men route
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@torture.route("/api/v1.0/precipitation")
def precipitation():
    latest = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    final = dt.datetime.strptime(latest[0], '%Y-%m-%d')
    last12= final - dt.timedelta(days = 365)
# WHO THOUGHT DATETIME INSIDE DATETIME IS A LEGIT WAY TO NAME THINGS?

    date_prec = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date.desc()).filter(Measurement.date > last12).\
            filter(Measurement.prcp != None).all()

    # Convert list of tuples into normal list
    # date = [row[0] for row in date_prec]
    # prec = [row[1] for row in date_prec]

    d = {key: value for (key, value) in date_prec}
# (grumph is clearly a better naming system. at least its emotionally descriptive)
    return jsonify(d)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# who doin' those measurements route
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@torture.route("/api/v1.0/stations")
def stations():
    station_count = session.query(Station.station, Station.name).distinct(Station.station).all()
    d2 = {key: value for (key, value) in station_count}
    return jsonify(d2)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# It's getting hott in herr route
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@torture.route("/api/v1.0/tobs")
def temp():
    latest = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    final = dt.datetime.strptime(latest[0], '%Y-%m-%d')
    last12= final - dt.timedelta(days = 365)

    date_tobs = session.query(Measurement.date, Measurement.tobs).\
        order_by(Measurement.date.desc()).\
    filter(Measurement.date > last12).filter(Measurement.tobs != None).all()

    d3 = {key: value for (key, value) in date_tobs}
    return jsonify(d3)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Starting from <date> route
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@torture.route("/api/v1.0/<start>")
def start(start):
    st_date = dt.datetime.strptime(start, '%Y-%m-%d')

    min_max = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), \
        func.avg(Measurement.tobs)).filter(Measurement.date >= st_date).all()
    print(min_max)
    d4 = {"min": min_max[0][0], "max": min_max[0][1], "avg": min_max[0][2]} 
# (grumph is clearly a better naming system. at least its emotionally descriptive)
    return jsonify(d4)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Vacation planning route 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@torture.route("/api/v1.0/<start>/<end>")
def range(start, end):
    st_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    st_end = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), \
        func.avg(Measurement.tobs)).filter(Measurement.date >= st_date).\
            filter (Measurement.date <= end_date).first()
    print(st_end)
    d5 = {"min": st_end[0], "max": st_end[1], "avg": st_end[2]} 

    return jsonify(d5)

# don't show them haters any of my shit!
if __name__ == '__main__':
    torture.run(debug=False)
# And Scene. 