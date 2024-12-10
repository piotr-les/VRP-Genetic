import numpy as np
import random
import itertools
from typing import List, Dict, Tuple


class VehicleRoutingProblem:
    def __init__(
        self,
        cities_data: Dict[str, Tuple[float, float]],
        city_demands: Dict[str, int],
        num_vehicles: int = 5,
        vehicle_capacity: int = 1000,
    ):
        self.cities_data = cities_data
        self.city_demands = city_demands
        self.num_vehicles = num_vehicles
        self.vehicle_capacity = vehicle_capacity
        self.cities = list(cities_data.keys())
        self.total_demand = sum(city_demands.values())

        # Sprawdzenie poprawności parametrów
        if self.num_vehicles * self.vehicle_capacity < self.total_demand:
            raise ValueError(
                f"Łączna pojemność pojazdów ({self.num_vehicles * self.vehicle_capacity}) "
                f"jest mniejsza niż całkowite zapotrzebowanie miast ({self.total_demand})."
            )

        # Obliczenie macierzy odległości
        self.distance_matrix = self._calculate_distance_matrix()

    def _haversine_distance(
        self, coord1: Tuple[float, float], coord2: Tuple[float, float]
    ) -> float:
        """Obliczenie odległości między współrzędnymi geograficznymi"""
        from math import radians, sin, cos, sqrt, atan2

        R = 6371  # promień Ziemi w km
        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    def _calculate_distance_matrix(self) -> np.ndarray:
        """Utworzenie macierzy odległości między miastami"""
        matrix = np.zeros((len(self.cities), len(self.cities)))

        for i, city1 in enumerate(self.cities):
            for j, city2 in enumerate(self.cities):
                matrix[i][j] = self._haversine_distance(
                    self.cities_data[city1], self.cities_data[city2]
                )
        return matrix

    def _validate_solution(self, vehicle_routes: List[List[str]]) -> bool:
        """Sprawdzenie poprawności rozwiązania"""
        # Sprawdzenie, czy wszystkie miasta są obsłużone
        served_cities = set(itertools.chain(*vehicle_routes))
        if (
            len(served_cities) != len(self.cities) - 1
        ):  # -1 bo Kraków jako punkt startowy
            return False

        # Sprawdzenie ładowności i zapotrzebowania każdego pojazdu
        for route in vehicle_routes:
            route_demand = sum(self.city_demands[city] for city in route)
            if route_demand > self.vehicle_capacity:
                return False

        return True

    def _calculate_total_distance(self, vehicle_routes: List[List[str]]) -> float:
        """Obliczenie całkowitej długości tras, włączając powrót do Krakowa"""
        total_distance = 0
        for route in vehicle_routes:
            route_distance = 0
            current_city = "Kraków"

            for city in route:
                city_index = self.cities.index(city)
                current_index = self.cities.index(current_city)
                route_distance += self.distance_matrix[current_index][city_index]
                current_city = city

            # Dodanie odległości powrotu do Krakowa
            city_index = self.cities.index("Kraków")
            current_index = self.cities.index(current_city)
            route_distance += self.distance_matrix[current_index][city_index]

            total_distance += route_distance

        return total_distance

    def genetic_algorithm(
        self,
        population_size: int = 200,
        generations: int = 300,
        mutation_rate: float = 0.1,
    ) -> List[List[str]]:
        """Zaawansowany algorytm genetyczny dla VRP"""
        cities_to_serve = [city for city in self.cities if city != "Kraków"]

        def create_individual():
            """Losowe utworzenie rozwiązania"""
            # Losowy podział miast między pojazdy
            individual = [[] for _ in range(self.num_vehicles)]
            random.shuffle(cities_to_serve)

            for i, city in enumerate(cities_to_serve):
                vehicle_index = i % self.num_vehicles
                individual[vehicle_index].append(city)

            return individual

        def fitness(solution):
            """Ocena rozwiązania"""
            # Jeśli rozwiązanie niepoprawne, zwróć bardzo niską wartość
            if not self._validate_solution(solution):
                return float("-inf")

            # Im mniejsza całkowita odległość, tym lepiej (stąd negacja)
            return -self._calculate_total_distance(solution)

        # Inicjalizacja populacji
        population = [create_individual() for _ in range(population_size)]

        for generation in range(generations):
            # Selekcja, krzyżowanie, mutacja
            new_population = []

            for _ in range(population_size):
                # Selekcja turniejowa
                parent1 = max(
                    random.sample(population, min(3, len(population))), key=fitness
                )
                parent2 = max(
                    random.sample(population, min(3, len(population))), key=fitness
                )

                # Krzyżowanie - wymiana miast między trasami
                child = [route.copy() for route in parent1]

                # Losowa mutacja - przesunięcie miasta między trasami
                if random.random() < mutation_rate and self.num_vehicles > 1:
                    vehicle1, vehicle2 = random.sample(range(self.num_vehicles), 2)
                    if child[vehicle1] and child[vehicle2]:
                        city = child[vehicle1].pop(
                            random.randint(0, len(child[vehicle1]) - 1)
                        )
                        child[vehicle2].append(city)

                new_population.append(child)

            population = new_population

        # Zwrócenie najlepszego rozwiązania
        return max(population, key=fitness)
