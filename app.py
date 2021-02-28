import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_end<br/>"

    )


@app.route("/api/v1.0/names")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all passengers
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/stations")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(Station.id, Station.name, Station.elevation, Station.latitude, Station.longitude).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_stations = []
    for id, name, elevation, latitude, longitude in results:
        station_dict = {}
        station_dict["id"] = id
        station_dict["name"] = name
        station_dict["elevation"] = elevation
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        all_stations.append(station_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return date and precipitation"""
    # Query precipitation 
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictionary from the row data and append to a list prcp
    all_measurements = []
    for date, prcp  in results:
        measurement_dict = {}
        measurement_dict[date] = prcp
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return date and temperature"""
    # Query precipitation 
    results = session.query( Measurement.date, Measurement.tobs).\
    filter(Measurement.station == Station.station).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= '2016-08-23').all()
    session.close()

    # Create a dictionary from the row data and append to a list of tobs
    all_tobs = []
    for date, tobs  in results:
        measurement_dict = {}
        measurement_dict[date] = tobs
        all_tobs.append(measurement_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/start_date")
def start_date():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start_date = '2011-01-31'
    end_date = '2011-12-31'
    """Return date and temperature"""
    # Query precipitation 
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of min, max and avg temp
    all_tobs = []
    for TMIN, TAVG, TMAX in results:
        measurement_dict = {}
        measurement_dict["minimum"] = TMIN
        measurement_dict["average"] = TAVG
        measurement_dict["maximum"] = TMAX

        all_tobs.append(measurement_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/start_end")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start_date = '2010-01-01'
    end_date = '2017-12-01'
    """Return date and temperature"""
    # Query precipitation 
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of  min, max and avg temp
    all_tobs = []
    for TMIN, TAVG, TMAX in results:
        measurement_dict = {}
        measurement_dict["minimum"] = TMIN
        measurement_dict["average"] = TAVG
        measurement_dict["maximum"] = TMAX

        all_tobs.append(measurement_dict)

    return jsonify(all_tobs)

if __name__ == '__main__':
    app.run(debug=True)