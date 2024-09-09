# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///C:\Users\bryan\OneDrive - Dallas College\Documents\Manuela\Homework\Module10Challenge\sqlalchemy-challenge\SurfsUp\Resources\hawaii.sqlite")
#engine = create_engine("sqlite:///.../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

#Base.classes.keys()

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#my_data ={"":""}



#################################################
# Flask Routes
#################################################
@app.route("/")
def Home():
    """List all available api routes."""
    return(f"Welcome to Home Page")

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    start_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d').date() - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    sel = [Measurement.date, Measurement.prcp]

    year_data = session.query(*sel).filter(Measurement.date >= start_date, Measurement.date <= most_recent_date).all()

    precipitation_dict = {date: prcp for date, prcp in year_data}

    # Return Json representation of my dictionary
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    stations_collection = session.query(Stations.station).all()
    list_of_stations = [station[0] for station in stations_collection]

    return jsonify(list_of_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #Query the dates and temperature observations of the most-active station for the previous year of data.
    begin_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d').date() - dt.timedelta(days=365)
    twelve_months_data = session.query(Measurement.tobs).filter(Measurement.date >= begin_date, Measurement.date <= most_recent_date, Measurement.station == "USC00519281").all()
    active_data = [{'Date': date, 'Temperature': temp} for date, temp in twelve_months_data]

    #Return a JSON list of temperature observations for the previous year"
    return jsonify(active_data)

@app.route("/api/v1.0/<start>")
def start():
    #Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start range.
    try:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid start date format. Use YYYY-MM-DD."}), 400
    #For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    calculate = session.query(
        func.min(Measurement.tobs).label('TMIN'),
        func.avg(Measurement.tobs).label('TAVG'),
        func.max(Measurement.tobs).label('TMAX')).filter(Measurement.date >= start_date).all()
    #For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    calculation_results = results[0] if results else {"TMIN": None, "TAVG": None, "TMAX": None}
    
    return jsonify(calculation_results)

@app.route("/api/v1.0/<start>/<end>")
def start_end():

    #Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
    try:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')
        end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    if start_date > end_date:
        return jsonify({"error": "Start date must be before or equal to end date."}), 400

    #For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
    start_end = session.query(
        func.min(Measurement.tobs).label('TMIN'),
        func.avg(Measurement.tobs).label('TAVG'),
        func.max(Measurement.tobs).label('TMAX')
    ).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    #For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
    start_end_results = results[0] if results else {"TMIN": None, "TAVG": None, "TMAX": None}
    
    return jsonify(start_end_results)


if __name__ == '__main__':
    app.run(debug=True)