# 1. import Flask
from flask import Flask, jsonify
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def main():
    """Lists all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

    @app.route("/api/v1.0/precipitation")
def precipitation():
    """Precipitation List"""
    
    print("Precipitation api request")

    last_date_query = Session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    #change to string
    last_date_string = late_date_query[0][0]
    last_date = datetime.datetime.strptime(last_date_string, "%Y-%m-%d")
    begining_date = last_date - datetime.timedelta(366)

    #getprcp amounts
    prcp_datas = Session.query(func.strftime("%Y-%m-%d", Measurement.date), Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= begining_date).all()
    
    #Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_dict = {}
    for a in prcp_datas:
        precipitation_dict[a[0]] = a[1]

    return jsonify(precipitation_dict)

    @app.route("/api/v1.0/stations")
def stations():
    """Station List"""

    print("Station api request")

    station_data = Session.query(Station).all()
    station_list = []
    
#Return a JSON list of stations from the dataset.
    for station in station_data:
        station_dict = {}
        station_dict["id"] = station.id
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_dict["latitude"] = station.latitude
        station_dict["longitude"] = station.longitude
        station_dict["elevation"] = station.elevation
        stations_list.append(station_dict)

    return jsonify(station_list)

    @app.route("/api/v1.0/tobs")
def tobs():
    """List of temp observations for previous year"""

    print("Tobs api request")
    
    last_date_query = Session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    #change to string
    last_date_string = late_date_query[0][0]
    last_date = datetime.datetime.strptime(last_date_string, "%Y-%m-%d")
    begining_date = last_date - datetime.timedelta(366)

    #get temperature measurements for last year
    temp_datas = Session.query(Measurement).\
        filter(func.strftime("%Y-%m-%d", Measurement.date) >= begining_date).all()

    #create list of dictionaries (one for each observation)
    tobs_list = []
    for temp in temp_datas:
        tobs_dict = {}
        tobs_dict["date"] = temp.date
        tobs_dict["station"] = temp.station
        tobs_dict["tobs"] = temp.tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range."""

    print("Start date and end date api request")

    temps =calc_temps(start, end)

    startend_list = []
    startend_dict = {'start_date': start, 'end_date': end}
    startend_list.append(date_dict)
    startend_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
    startend_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
    startend_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})

    return jsonify(return_list)

#code to actually run
if __name__ == "__main__":
    app.run(debug = True)