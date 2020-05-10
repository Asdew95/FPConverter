import xml.dom.minidom as md

from flightplan import Flightplan, Runway, Waypoint

def import_fp(fp: str):
    ofp = md.parseString(fp).getElementsByTagName("OFP")[0]
    
    origin = ofp.getElementsByTagName("origin")[0]
    departure = Runway(origin.getElementsByTagName("icao_code")[0] \
            .childNodes[0].nodeValue, origin \
            .getElementsByTagName("plan_rwy")[0].childNodes[0].nodeValue)
    
    dest_xml = ofp.getElementsByTagName("destination")[0]
    destination = Runway(dest_xml.getElementsByTagName("icao_code")[0] \
            .childNodes[0].nodeValue, dest_xml \
            .getElementsByTagName("plan_rwy")[0].childNodes[0].nodeValue)

    navlog = ofp.getElementsByTagName("navlog")[0] \
            .getElementsByTagName("fix")
    
    route = []
    for fix in navlog:
        # Skip SIDs and STARs
        if fix.getElementsByTagName("is_sid_star")[0].childNodes[0] \
                .nodeValue == "1":
            continue

        ident = fix.getElementsByTagName("ident")[0].childNodes[0] \
                .nodeValue
        latitude = fix.getElementsByTagName("pos_lat")[0].childNodes[0] \
                .nodeValue
        longitude = fix.getElementsByTagName("pos_long")[0].childNodes[0] \
                .nodeValue
        altitude = int(fix.getElementsByTagName("altitude_feet")[0] \
                .childNodes[0].nodeValue)

        waypoint = Waypoint(ident, latitude, longitude, altitude=altitude)
        route.append(waypoint)

    initial_cruise_altitude = int(ofp.getElementsByTagName("general")[0] \
            .getElementsByTagName("initial_altitude")[0].childNodes[0] \
            .nodeValue)

    flightplan = Flightplan(departure, destination,
            cruise_altitude=initial_cruise_altitude, route=route)
    return flightplan
