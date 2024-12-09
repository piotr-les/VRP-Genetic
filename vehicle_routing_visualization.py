import folium
import random
from cities_data import cities_data, city_demands
from vehicle_routing_optimization import ImprovedVehicleRoutingProblem


def visualize_routes(cities_data, routes):
    """Wizualizacja tras na mapie Polski"""
    # Centrum mapy - Kraków
    m = folium.Map(location=[50.0647, 19.9450], zoom_start=6)

    # Kolory dla różnych tras
    colors = ["red", "blue", "green", "purple", "orange"]

    # Dodanie Krakowa jako punktu startowego
    folium.Marker(
        [50.0647, 19.9450],
        popup="Kraków - Punkt startowy",
        icon=folium.Icon(color="black", icon="home"),
    ).add_to(m)

    for i, route in enumerate(routes):
        # Trasa z Krakowa przez miasta do Krakowa (pełna pętla)
        route_coords = (
            [cities_data["Kraków"]]
            + [cities_data[city] for city in route]
            + [cities_data["Kraków"]]
        )

        # Rysowanie linii trasy
        folium.PolyLine(
            route_coords,
            color=colors[i],
            weight=2,
            opacity=0.8,
            popup=f"Trasa pojazdu {i+1}",
        ).add_to(m)

        # Dodanie markerów dla miast na trasie z numeracją kolejności
        for j, city in enumerate(route, 1):
            folium.Marker(
                cities_data[city],
                popup=f"{city} (Pojazd {i+1}, Kolejność: {j})",
                tooltip=f"{city} - Kolejność: {j}",
                icon=folium.Icon(color=colors[i], icon="info-sign"),
            ).add_to(m)

    # Zapis mapy
    m.save("vehicle_routing_map.html")
    return m
