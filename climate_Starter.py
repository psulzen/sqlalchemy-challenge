import numpy as np
import pandas as pd
import datetime as dt
from flask import request

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


# DBSession = sessionmaker(bind=engine) 
# session = DBSession()

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

connect_args={'check_same_thread':False},

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Exploratory Climate Analysis

# first_row = session.query(Measurement).first()
# first_row.__dict__

####################################
# initializes Flask app
####################################
app = Flask(__name__)


########################################################################
# Define route for homepage with list of all routes
########################################################################



@app.route("/")
def homepage():

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    connect_args={'check_same_thread':False},

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)

    # We can view all of the classes that automap found
    Base.classes.keys()

    # Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station

    # Create our session (link) from Python to the DB
    session = Session(engine)

    return(
        f"These are the available API routes to choose from: <br>"
        f"<br/>"
        f"Precipitation info<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Station info<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature Observation info<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Temperature data for a given date<br/>"
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"<br/>"
        f"Temperature data over a date range<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
    )

########################################################################
# Define route for precipitation with results of precipitation query
########################################################################

@app.route("/api/v1.0/precipitation")
def precipitation():

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    connect_args={'check_same_thread':False},

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)

    # We can view all of the classes that automap found
    Base.classes.keys()

    # Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station

    # Create our session (link) from Python to the DB
    session = Session(engine)

    precipitation_result = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= "2016-08-24", Measurement.date <= "2017-08-23").\
    all()

    precipitation_out = [precipitation_result]
    
    return jsonify(precipitation_out)

########################################################################
# Define route for stations with results of station query
########################################################################

@app.route("/api/v1.0/stations")
def stations():

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    connect_args={'check_same_thread':False},

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)

    # We can view all of the classes that automap found
    Base.classes.keys()

    # Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station

    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations_result = session.query(Station.name, Station.station, Station.elevation).all()

    # creates JSONified list of dictionaries
    station_out = []
    for station in stations_result:
        row = {}
        row['name'] = station[0]
        row['station'] = station[1]
        row['elevation'] = station[2]
        station_out.append(row)
    return jsonify(station_out)

########################################################################
# Define route for tobs with results of total observations query
########################################################################

@app.route("/api/v1.0/tobs")
def tobs():

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    connect_args={'check_same_thread':False},

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)

    # We can view all of the classes that automap found
    Base.classes.keys()

    # Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station

    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations_result = session.query(Station.name, Station.station, Station.elevation).all()

    tobs_result = session.query(Station.name, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-24", Measurement.date <= "2017-08-23").\
        all()

    # creates JSONified list of dictionaries
    tobs_out = []
    for tobs in tobs_result:
        row = {}
        row["Station"] = tobs[0]
        row["Date"] = tobs[1]
#        row["Temperature"] = int(tobs[2])
        row["Temperature"] = tobs[2]
        tobs_out.append(row)

    return jsonify(tobs_out)

########################################################################
# Define route for date with results of date query
########################################################################

@app.route('/api/v1.0/<date>/')
def given_date(date):
    
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    connect_args={'check_same_thread':False},

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)

    # We can view all of the classes that automap found
    Base.classes.keys()

    # Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station

    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations_result = session.query(Station.name, Station.station, Station.elevation).all()


    date_results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= date).all()

    date_out = []
    for date in date_results:
        row = {}
        row['Start Date'] = date
        row['End Date'] = '2017-08-23'
        row['Average Temperature'] = date[0]
        row['Highest Temperature'] = date[1]
        row['Lowest Temperature'] =  date[2]

        date_out.append(row)

    return jsonify(date_out)


########################################################################
# Define route for date range with results of date query
########################################################################

@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):

    engine = create_engine("sqlite:///Resources/hawaii.sqlite")

    connect_args={'check_same_thread':False},

    # reflect an existing database into a new model
    Base = automap_base()
    # reflect the tables
    Base.prepare(engine, reflect=True)

    # We can view all of the classes that automap found
    Base.classes.keys()

    # Save references to each table
    Measurement = Base.classes.measurement
    Station = Base.classes.station

    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations_result = session.query(Station.name, Station.station, Station.elevation).all()


    range_out = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    ramge_list = []
    for result in range_out:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Average Temperature"] = result[0]
        row["Highest Temperature"] = result[1]
        row["Lowest Temperature"] = result[2]
        ramge_list.append(row)
    return jsonify(ramge_list)

if __name__ == '__main__':
    app.run(debug=True)