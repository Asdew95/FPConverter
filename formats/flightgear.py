import xml.dom.minidom as md

from flightplan import Flightplan, Waypoint

def create_waypoint_element(doc, waypoint, n=None, wp_type="navaid", icao=None,
        departure=False, arrival=False):
    wp = doc.createElement("wp")
    
    if n != None:
        wp.setAttribute("n", str(n))

    if departure:
        dep_element = doc.createElement("departure")
        dep_element.setAttribute("type", "bool")
        dep_element.appendChild(doc.createTextNode("true"))
        wp.appendChild(dep_element)

    if arrival:
        arr_element = doc.createElement("arrival")
        arr_element.setAttribute("type", "bool")
        arr_element.appendChild(doc.createTextNode("true"))
        wp.appendChild(arr_element)

    if icao != None:
        icao_element = doc.createElement("icao")
        icao_element.setAttribute("type", "string")
        icao_element.appendChild(doc.createTextNode(icao))
        wp.appendChild(icao_element)

    if waypoint.altitude != None:
        altitude_element = doc.createElement("altitude-ft")
        altitude_element.setAttribute("type", "double")
        altitude_element.appendChild(doc.createTextNode( \
                str(waypoint.altitude)))
        wp.appendChild(altitude_element)
        alt_restrict_element = doc.createElement("alt-restrict")
        alt_restrict_element.setAttribute("type", "string")
        alt_restrict_element.appendChild(doc.createTextNode("at"))
        wp.appendChild(alt_restrict_element)

    type_element = doc.createElement("type")
    type_element.setAttribute("type", "string")
    type_element.appendChild(doc.createTextNode(wp_type))
    wp.appendChild(type_element)

    ident_element = doc.createElement("ident")
    ident_element.setAttribute("type", "string")
    ident_element.appendChild(doc.createTextNode(waypoint.ident))
    wp.appendChild(ident_element)

    if waypoint.latitude != None:
        latitude_element = doc.createElement("lat")
        latitude_element.setAttribute("type", "double")
        latitude_element.appendChild(doc.createTextNode(str(waypoint \
                .latitude)))
        wp.appendChild(latitude_element)

    if waypoint.longitude != None:
        longitude_element = doc.createElement("lon")
        longitude_element.setAttribute("type", "double")
        longitude_element.appendChild(doc.createTextNode(str(waypoint \
                .longitude)))
        wp.appendChild(longitude_element)

    return wp

def export_fp(flightplan: Flightplan) -> str:
    doc = md.Document()
    property_list = doc.createElement("PropertyList")
    doc.appendChild(property_list)

    version = doc.createElement("version")
    version.setAttribute("type", "int")
    version.appendChild(doc.createTextNode("2"))
    property_list.appendChild(version)

    departure = doc.createElement("departure")
    
    departure_airport = doc.createElement("airport")
    departure_airport.setAttribute("type", "string")
    departure_airport.appendChild(doc.createTextNode(
        flightplan.departure.airport))
    departure.appendChild(departure_airport)
    
    departure_runway = doc.createElement("runway")
    departure_runway.setAttribute("type", "string")
    departure_runway.appendChild(doc.createTextNode(
        flightplan.departure.runway))
    departure.appendChild(departure_runway)

    property_list.appendChild(departure)

    destination = doc.createElement("destination")
    
    destination_airport = doc.createElement("airport")
    destination_airport.setAttribute("type", "string")
    destination_airport.appendChild(doc.createTextNode(
        flightplan.destination.airport))
    destination.appendChild(destination_airport)
    
    destination_runway = doc.createElement("runway")
    destination_runway.setAttribute("type", "string")
    destination_runway.appendChild(doc.createTextNode(
        flightplan.destination.runway))
    destination.appendChild(destination_runway)

    property_list.appendChild(destination)

    route = doc.createElement("route")

    tmp_wp = Waypoint(flightplan.departure.runway, None, None)
    route.appendChild(create_waypoint_element(doc, tmp_wp,
        wp_type="runway", icao=flightplan.departure.airport,
        departure=True))
    
    n = 1
    for waypoint in flightplan.route:
        if waypoint.ident not in ("TOD", "TOC"):
            route.appendChild(create_waypoint_element(doc, waypoint, n=n))
        else:
            route.appendChild(create_waypoint_element(doc, waypoint, n=n,
                wp_type="basic"))
        n += 1

    tmp_wp = Waypoint(flightplan.destination.runway, None, None)
    route.appendChild(create_waypoint_element(doc, tmp_wp,
        wp_type="runway", icao=flightplan.destination.airport,
        arrival=True))

    property_list.appendChild(route)

    return doc.toprettyxml()

