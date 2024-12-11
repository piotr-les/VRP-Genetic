import folium
from folium import plugins
from cities_data import cities_data, city_demands
from vehicle_routing_optimization import VehicleRoutingProblem


def calculate_route_distance(route, distance_matrix, cities):
    """Obliczenie dystansu dla danej trasy"""
    total_distance = 0
    current_city = "Kraków"

    for city in route:
        city_index = cities.index(city)
        current_index = cities.index(current_city)
        total_distance += distance_matrix[current_index][city_index]
        current_city = city

    # Dodanie odległości powrotu do Krakowa
    city_index = cities.index("Kraków")
    current_index = cities.index(current_city)
    total_distance += distance_matrix[current_index][city_index]

    return total_distance


def calculate_route_demand(route, city_demands):
    """Obliczenie zapotrzebowania dla danej trasy"""
    return sum(city_demands[city] for city in route)


def visualize_routes(cities_data, routes):
    """Wizualizacja tras na mapie Polski z zaawansowanym panelem bocznym"""
    # Centrum mapy - Kraków
    m = folium.Map(location=[50.0647, 19.9450], zoom_start=6)

    # Kolory dla różnych tras
    colors = ["red", "blue", "green", "purple", "orange"]

    # Przygotowanie VRP dla obliczenia odległości
    vrp = VehicleRoutingProblem(cities_data, city_demands)

    # Dodanie Krakowa jako punktu startowego
    folium.Marker(
        [50.0647, 19.9450],
        popup="Kraków - Punkt startowy",
        icon=folium.Icon(color="black", icon="home"),
    ).add_to(m)

    # Przygotowanie opisu tras
    routes_html = ""
    total_route_distance = 0

    for i, route in enumerate(routes):
        # Trasa z Krakowa przez miasta do Krakowa (pełna pętla)
        route_coords = (
            [cities_data["Kraków"]]
            + [cities_data[city] for city in route]
            + [cities_data["Kraków"]]
        )

        # Obliczenie dystansu trasy
        route_distance = calculate_route_distance(
            route, vrp.distance_matrix, vrp.cities
        )
        route_demand = calculate_route_demand(route, city_demands)
        total_route_distance += route_distance

        # Formatowanie opisu trasy
        full_route = ["Kraków"] + route + ["Kraków"]
        route_description = " → ".join(full_route)

        routes_html += f"""
        <div class="route-card" style="border-left: 5px solid {colors[i]}; margin-bottom: 10px; padding: 10px; background-color: #f9f9f9;">
            <div class="route-header" style="font-weight: bold; margin-bottom: 5px;">
                Pojazd {i+1}
            </div>
            <div class="route-details" style="font-size: 0.9em;">
                <div>Trasa: </br> {route_description}</div>
                <div>Dystans: {route_distance:.2f} km</div>
                <div>Zapotrzebowanie: {route_demand} jedn.</div>
            </div>
        </div>
        """

        plugins.AntPath(
            route_coords,
            color=colors[i],
            weight=4,
            opacity=0.8,
            dash_array=[10, 20],
            delay=1500,
        ).add_to(m)

        # Dodanie markerów dla miast na trasie z numeracją kolejności
        for j, city in enumerate(route, 1):
            folium.Marker(
                cities_data[city],
                popup=f"{city} (Pojazd {i+1}, Kolejność: {j})",
                tooltip=f"{city} - Kolejność: {j}",
                icon=folium.Icon(color=colors[i], icon="info-sign"),
            ).add_to(m)

    # Dodanie panelu bocznego z trasami
    sidebar_html = f"""
    <div style="
        position: fixed; 
        top: 10px; 
        right: 10px; 
        width: 300px; 
        height: calc(100% - 40px);
        background-color: white; 
        border: 2px solid #ccc; 
        z-index: 9999; 
        overflow-y: auto;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-radius: 5px;
    ">
        <h3 style="margin-bottom: 15px; text-align: center; border-bottom: 2px solid #333; padding-bottom: 10px;">
            Optymalizacja Tras
        </h3>
        {routes_html}
        <div style="text-align: center; margin-top: 15px; font-weight: bold; border-top: 1px solid #ccc; padding-top: 10px;">
            Całkowity dystans: {total_route_distance:.2f} km
        </div>
    </div>
    """

    m.get_root().html.add_child(folium.Element(sidebar_html))

    # Zapis mapy
    m.save("vehicle_routing_map.html")
    return m
