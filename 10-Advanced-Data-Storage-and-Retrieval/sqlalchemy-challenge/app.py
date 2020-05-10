import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

import datetime as dt

from flask import Flask, jsonify

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
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """All available api routes."""
    return (
        f"Available Climate App Routes:<br/>"
        f'<a href="/api/v1.0/precipitation">Precipitation Data</a><br/>'
        f'<a href="/api/v1.0/stations">Stations Data</a><br/>'
        f'<a href="/api/v1.0/tobs">Temperature Data</a><br/>' 
        f'<a href="/api/v1.0/<start>">Historical Data Start Date Only</a><br/>'
        f'<a href="/api/v1.0/<start/<end>>">Historical Data Start and End Dates</a><br/>'       
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Connect to the session
    session = Session(bind = engine)

    sel = [Measurement.date, func.sum(Measurement.prcp)]

    prcp_data = session.query(*sel).group_by(Measurement.date).all()

    # Disconnect to the session
    session.close()
    
    prcp_dict = {}

    for i in prcp_data:
        prcp_dict[i[0]] = i[1]

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

    
    # Disconnect to the session
    session.close()

    # Convert list of tuples to list
    # tobs_data = list(np.ravel(tobs_data))

    return jsonify(last_year)

if __name__ == '__main__':
    app.run(debug=True)
