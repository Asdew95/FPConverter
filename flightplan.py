class Waypoint:

    def __init__(self, ident: str, latitude: float, longitude: float, \
            sidstar=False, altitude=None):
        self.ident = ident
        self.latitude = latitude
        self.longitude = longitude
        self.sidstar = sidstar
        self.altitude = altitude


class Runway:

    def __init__(self, airport: str, runway: str, sid=None, star=None):
        self.airport = airport
        self.runway = runway
        self.sid = None
        self.star = None


class Flightplan:

    def __init__(self, departure: Runway, destination: Runway, cruise_altitude=0,
            route=[]):
        self.departure = departure
        self.destination = destination
        self.cruise_altitude = cruise_altitude
        self.route = route
