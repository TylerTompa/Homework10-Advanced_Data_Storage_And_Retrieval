# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# 1. import Flask
from flask import Flask, jsonify

engine = create_engine("sqlite:///Data/hawaii.sqlite")
conn = engine.connect()


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
    "Welcome to my weather data page!</br></br>"
    "Available directories</br>"
    "/api/v1.0/precipitation</br>"
    "/api/v1.0/stations</br>"
    "/api/v1.0/tobs</br>"
    "/api/v1.0/<start></br>"
    "/api/v1.0/<start>/<end>")

# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation_data_last_12_months = session.query(Measurement.date, Measurement.prcp) \
    .filter(Measurement.date.between("2016-08-23", "2017-08-23"))

    precepdict = {date : prcp for date, prcp in precipitation_data_last_12_months}
    return jsonify(precepdict)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station)
    stations_list = [station for station in stations]
    return jsonify(stations_list)

# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    dates_temperatures = session.query(Measurement.date, Measurement.tobs).filter(func.strftime("%Y-%m-%d", Measurement.date) >= "2016-08-23").filter(func.strftime("%Y-%m-%d", Measurement.date) <= "2017-08-23").all()

    dates_temperatures_dict = [temperature for date, temperature in dates_temperatures]
    return jsonify(dates_temperatures_dict)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
# @app.route("/api/v1.0/<start>")
# def start():


# @app.route("api/v1.0/<start>/<end>")


# In[ ]:


if __name__ == "__main__":
    app.run(debug=True)

