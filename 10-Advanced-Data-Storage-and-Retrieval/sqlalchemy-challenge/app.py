import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

import datetime as dt

from flask import Flask, jsonify, render_template

# Setup Database
path = 'Resources/hawaii.sqlite'
engine = create_engine(f'sqlite:///{path}')

# Reflect an exsiting database
Base = automap_base()

# Reflect database tables
Base.prepare(engine, reflect = True)
Station = Base.classes.station
Measurement = Base.classes.measurement

# Flask begins
app = Flask(__name__, template_folder='')

# Flask Routes
@app.route("/")
def home():
   return render_template('/home.html')
# def welcome():
#     """All available api routes."""
#     return (
#         f'Available Climate App Routes:<br/>'
#         f'<a href="/api/v1.0/precipitation">Precipitation Data</a><br/>'
#         f'<a href="/api/v1.0/stations">Stations Data</a><br/>'
#         f'<a href="/api/v1.0/tobs">Temperature Data</a><br/>' 
#         f'Historical Temperature Average Data (Start Date Only) : /api/v1.0/start/YYYY-MM-DD <br/>'
#         f'Historical Temperature Average Data : /api/v1.0/start/YYYY-MM-DD/end/YYYY-MM-DD <br/>'
#         # f'<a href="/api/v1.0/<start>">Historical Data Start Date Only</a><br/>'
#         # f'<a href="/api/v1.0/<start/<end>>">Historical Data Start and End Dates</a><br/>'       
#     )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Connect to the session
    session = Session(bind = engine)

    sel = [Measurement.date, func.sum(Measurement.prcp)]

    prcp_data = session.query(*sel).group_by(Measurement.date).all()

    # Disconnect to the session
    session.close()
    
    prcp_dict = dict(prcp_data)

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():

    # Connect to the session
    session = Session(bind = engine)

    station_data = session.query(Station.name).all()
    
    # Disconnect to the session
    session.close()

    # Convert list of tuples to list
    station_data = list(np.ravel(station_data))

    return jsonify(station_data)


@app.route("/api/v1.0/tobs")
def tobs():

    # Connect to the session
    session = Session(bind = engine)

    # Find Last Year
    ## What is the latest date?
    max_date = session.query(func.max(Measurement.date)).first()
    max_date = max_date[0]
    max_date = dt.datetime.strptime(max_date, '%Y-%m-%d')
    last_year = max_date.year - 1

    # Find Most Active Station for the last year
    sel = [Measurement.station, func.count(Measurement.tobs)]

    most_active = session.query(*sel).\
                        group_by(Measurement.station).\
                        order_by(func.count(Measurement.tobs).desc()).first()

    most_active = most_active[0]

    # Find all tobs data from last year's most active station
    sel = [Measurement.date, Measurement.tobs]

    tobs_data = session.query(*sel).\
                        filter(func.strftime("%Y", Measurement.date) == str(last_year)).\
                        filter(Measurement.station == most_active).all()

    # Convert list of tuples to dictionary
    tobs_data_dict = dict(tobs_data)

    
    # Disconnect to the session
    session.close()

    return jsonify(tobs_data_dict)


@app.route(f"/api/v1.0/start/<start>")
def ave_temp_start_only(start):

    # Connect to the session
    session = Session(bind = engine)

    start = dt.datetime.strptime(start, '%Y-%m-%d')

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    output = session.query(*sel).filter(Measurement.date >= start).all()

    output_dict = {}

    output_dict['TMIN'] = output[0][0]
    output_dict['TAVG'] = output[0][1]
    output_dict['TMAX'] = output[0][2]

    # Disconnect to the session
    session.close()

    return jsonify(output_dict)

@app.route(f"/api/v1.0/start/<start>/end/<end>")
def ave_temp(start, end):

    # Connect to the session
    session = Session(bind = engine)

    start = dt.datetime.strptime(start, '%Y-%m-%d')
    end   = dt.datetime.strptime(end, '%Y-%m-%d')

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    output = session.query(*sel).filter(and_(Measurement.date >= start, Measurement.date < end)).all()

    output_dict = {}

    output_dict['TMIN'] = output[0][0]
    output_dict['TAVG'] = output[0][1]
    output_dict['TMAX'] = output[0][2]

    # Disconnect to the session
    session.close()

    return jsonify(output_dict)

    
if __name__ == '__main__':
    app.run(debug=True)
