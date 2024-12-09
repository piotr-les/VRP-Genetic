import sys
import traceback
from cities_data import cities_data, city_demands
from vehicle_routing_optimization import ImprovedVehicleRoutingProblem
from vehicle_routing_visualization import visualize_routes


import tkinter as tk
from tkinter import ttk, messagebox
import sys
import traceback


class VRPOptimizationApp:
    def __init__(self, master):
        self.master = master
        master.title("Optymalizator Tras Pojazdów")

        # Liczba pojazdów
        tk.Label(master, text="Liczba pojazdów:").grid(row=0, column=0)
        self.vehicles_spin = tk.Spinbox(master, from_=1, to=10, width=10)
        self.vehicles_spin.grid(row=0, column=1)

        # Ładowność pojazdu
        tk.Label(master, text="Ładowność pojazdu:").grid(row=1, column=0)
        self.capacity_spin = tk.Spinbox(master, from_=100, to=5000, width=10)
        self.capacity_spin.grid(row=1, column=1)

        # Liczba generacji
        tk.Label(master, text="Liczba generacji:").grid(row=2, column=0)
        self.generations_spin = tk.Spinbox(master, from_=50, to=1000, width=10)
        self.generations_spin.grid(row=2, column=1)

        # Przycisk optymalizacji
        optimize_button = tk.Button(
            master, text="Optymalizuj Trasy", command=self.optimize_routes
        )
        optimize_button.grid(row=3, column=0, columnspan=2)

        # Obszar wyników
        self.results_text = tk.Text(master, height=20, width=50)
        self.results_text.grid(row=4, column=0, columnspan=2)

    def optimize_routes(self):
        try:

            # Pobranie parametrów
            num_vehicles = int(self.vehicles_spin.get())
            vehicle_capacity = int(self.capacity_spin.get())
            generations = int(self.generations_spin.get())

            # Utworzenie problemu VRP
            vrp = ImprovedVehicleRoutingProblem(
                cities_data,
                city_demands,
                num_vehicles=num_vehicles,
                vehicle_capacity=vehicle_capacity,
            )

            # Uruchomienie algorytmu genetycznego
            best_routes = vrp.genetic_algorithm(
                population_size=100, generations=generations
            )

            # Wizualizacja tras
            visualize_routes(cities_data, best_routes)

            # Przygotowanie wyników
            results = "Optymalne trasy dla pojazdów:\n\n"
            total_distance = 0

            for i, route in enumerate(best_routes, 1):
                results += f"Pojazd {i}:\n"
                results += " -> ".join(["Kraków"] + route) + "\n\n"

                route_distance = 0
                current_city = "Kraków"
                current_demand = 0

                for city in route:
                    current_demand += city_demands[city]
                    city_index = list(cities_data.keys()).index(city)
                    current_index = list(cities_data.keys()).index(current_city)
                    route_distance += vrp.distance_matrix[current_index][city_index]
                    current_city = city

                total_distance += route_distance
                results += f"Trasa pojazdu {i}: {route_distance:.2f} km, zapotrzebowanie: {current_demand}\n"

            results += f"\nŁączna długość tras: {total_distance:.2f} km"

            # Wyświetlenie wyników
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, results)

        except Exception as e:
            error_msg = (
                f"Błąd podczas optymalizacji:\n{str(e)}\n\n{traceback.format_exc()}"
            )
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, error_msg)


def main():
    root = tk.Tk()
    app = VRPOptimizationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
