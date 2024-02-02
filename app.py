# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home Route
@app.route("/")
def home():
    """List all api routes."""
    return (
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/<start><br/>"
        "/api/v1.0/<start>/<end><br/>"
    )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    most_recent = dt.date(2017, 8, 23)
    query_date = most_recent - dt.timedelta(days=365)
    data_table = session.query(measurement.date, measurement.prcp).filter(measurement.date >= query_date).all()
    session.close()
    precipitation_list = []
    for date, prcp in data_table:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation_list)

# Station Route
@app.route("/api/v1.0/stations")
def stn():
    session = Session(engine)
    station_table = session.query(station.id, station.station).all()
    session.close()
    station_list = []
    for id, station in station_table:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_list.append(station_dict)

    return jsonify(station_list)
    
# Tobs Route
@app.route("/api/v1.0/tobs")
def temp():
    session = Session(engine)
    most_active_id = session.query(measurement.station, func.count(measurement.station)).\
        order_by(func.count(measurement.station).desc()).\
        group_by(measurement.station).first()[0]
    most_recent_date = dt.date(2017, 8, 18)
    first_date = most_recent_date - dt.timedelta(days=365)
    temperature_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == most_active_id).\
        filter(measurement.date >= first_date).all()
    session.close()
    temp_list = []
    for date, tobs in temperature_data:
        temperature_dict = {}
        temperature_dict["date"] = date
        temperature_dict["tobs"] = tobs
        temp_list.append(temperature_dict)

    return jsonify(temp_list)


# Start Route 
@app.route("/api/v1.0/<start>")
def start(starting_date):
    session = Session(engine)
    # Convert starting_date from string to datetime object if necessary
    # starting_date = dt.datetime.strptime(starting_date, '%Y-%m-%d').date()
    
    data_description = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= starting_date).all()
    session.close()
    start_list = []
    for min, max, avg in data_description:
        start_dict = {}
        start_dict['min'] = min
        start_dict['max'] = max
        start_dict['avg'] = avg
        start_list.append(start_dict)

    return jsonify(start_list)


# End Route
@app.route("/api/v1.0/<start>/<end>")
def end(starting_date, ending_date):
    session = Session(engine)
    # Convert starting_date and ending_date from string to datetime objects if necessary
    # starting_date = dt.datetime.strptime(starting_date, '%Y-%m-%d').date()
    # ending_date = dt.datetime.strptime(ending_date, '%Y-%m-%d').date()

    data_description1 = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= starting_date).\
        filter(measurement.date

if __name__ == '__main__':
    app.run(debug=True)
