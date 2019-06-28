# import Flask and other tools
from flask import Flask, jsonify

import datetime as dt
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#creating app
app = Flask(__name__)

#routes
@app.route("/")
def home():
    print("Server receieved a request for home page")
    return (f"Welcome to my Hawaii rain app!<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/start/end<br/>")

@app.route("/api/v1.0/precipitation")
def prep():
    print("Server receieved a request for precipitation page")



    # Perform a query to retrieve the data and precipitation scores
    data = session.query(Measurement.date, Measurement.prcp).all()
    
    #  * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    dict_data = dict(data)
    
    session.close()

    return jsonify(dict_data)


@app.route("/api/v1.0/stations")
def stations():
    print("Server receieved a request for stations page")

    # Query the stations
    list_stations = session.query(Station.station).all()
    
    #convert the query to a list
    test = list(np.ravel(list_stations))

    session.close()
    
    # Return a JSON list of stations from the dataset.
    return jsonify(test)

@app.route("/api/v1.0/tobs")
def date_and_temp():
    print("Server receieved a request for dates and temp page")

    # Calculate the date 1 year ago from the last data point in the database
    last_12_months = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    date_temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > last_12_months).all()
    
    #  * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    dict_date_temp = dict(date_temp)
    
    session.close()

    return jsonify(dict_date_temp)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    print("Server receieved a request for start temp page")

    #Query using given start date
    start_mx_mn_av_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter( Measurement.date >= start).all()
    #return list(np.ravel(start_mx_mn_av_temp))
    #Convert results to a dictionary
    dict_start = list(np.ravel(start_mx_mn_av_temp))
    #dict_start = dict(start_mx_mn_av_temp)
    
    return jsonify(dict_start)
    #return results
    #return jsonify(dict_start)

    #Close session
    session.close()

    

@app.route("/api/v1.0/<start>/<end>")
def start_end_temp(start, end):
    print("Server receieved a request for start and end temp page")

    #Query using given start date
    start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    #Convert results to a dictionary
    dict_start_end = list(np.ravel(start_end))
    

    return jsonify(dict_start_end)

    #Close session
    session.close()

if __name__ == "__main__":
    app.run(debug=True)