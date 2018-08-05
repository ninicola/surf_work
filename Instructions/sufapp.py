import datetime as dt
import numpy as np
import pandas as pd

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect

from flask import Flask, jsonify
#################################################
#create dictionary base on the request
#################################################
#create create_engine
engine=create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables, means start mappig from engine
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
# date 1 year ago from today
year_ago = dt.date.today() - dt.timedelta(days=730)



# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
# date 1 year ago from today
year_ago = dt.date.today() - dt.timedelta(days=730)
year_ago
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the JSON representation of the dictionary"""
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    sel=[Measurement.date,
         Measurement.tobs]
    day_prcp=session.query(*sel).filter((Measurement.date>year_ago)).all()
    #create json Object
    pre_list=[]
    for result in day_prcp:
        row={}
        row['Date']=result[0]
        row['Temperature']=result[1]
        pre_list.append(row)

    return jsonify(pre_list)
@app.route("/api/v1.0/station")
def station():
    """Return the JSON for all the station information"""
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    sel_station=[Station.station,
                 Station.name,
                 Station.latitude,
                 Station.longitude,
                 Station.elevation]
    station_qu=session.query(*sel_station).all()
    #convert to json file
    station_list=[]
    for result in station_qu:
        row = {}
        row['name'] = result[0]
        row['station'] = result[1]
        row['latitude'] = result[2]
        row['longitude'] = result[3]
        row['elevation'] = result[4]
        station_list.append(row)

    return jsonify(station_list)
@app.route("/api/v1.0/tobs")
def tobs():
    """Return the JSON for all the temperature  fro past 12 month """
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    tobs_result=[Station.name,
                     Measurement.date,
                     Measurement.tobs]
    sel_tobs_result=session.query(*tobs_result).filter(Measurement.date>year_ago).all()
    #convert to json file
    station_tob_list=[]
    for result in sel_tobs_result:
        row = {}
        row['name']=result[0]
        row['date']=result[1]
        row['tobs']=result[2]
        station_tob_list.append(row)

    return jsonify(station_tob_list)

@app.route("/api/v1.0/<start_date>/<end_date>/")
def given_dates(start_date,end_date):
    """Return the JSON for max,avg and min of temperature  by date range"""
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    cal_sql=[Measurement.date,
             func.min(Measurement.tobs),
             func.avg(Measurement.tobs),
             func.max(Measurement.tobs)]
    cal_max_min_avg_result=session.query(*cal_sql).\
    filter(Measurement.date>=start_date,Measurement.date<=end_date).\
    group_by(Measurement.date).all()
    #convert to json object
    temp_comp=[]
    for result in cal_max_min_avg_result:
        row = {}
        row['Date']=result[0]
        row['Min Temperature']=result[1]
        row['Avg Temperature']=result[2]
        row['Max Temperature']=result[3]
        temp_comp.append(row)

    return jsonify(temp_comp)

@app.route("/api/v1.0/<give_date>/")
def given_date(give_date):
    """Return the JSON for max,avg and min of temperature  by date range"""
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    cal_sql=[Measurement.date,
             func.min(Measurement.tobs),
             func.avg(Measurement.tobs),
             func.max(Measurement.tobs)]
    cal_max_min_avg_result=session.query(*cal_sql).\
    filter(Measurement.date==give_date).\
    group_by(Measurement.date).all()
    #convert to json object
    temp_comp=[]
    for result in cal_max_min_avg_result:
        row = {}
        row['Date']=result[0]
        row['Min Temperature']=result[1]
        row['Avg Temperature']=result[2]
        row['Max Temperature']=result[3]
        temp_comp.append(row)

    return jsonify(temp_comp)

@app.route("/")
def welcome():
    return (
        f"Welcome to the List of all returnable API routes.<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Return temperature last year:<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"Return MAX,AVG and MIN temperature by date rage you given:<br/>"
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"Return MAX,AVG and MIN temperature by date you given:<br/>"




    )


if __name__ == "__main__":
    app.run(debug=True)
