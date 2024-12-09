import sys
import traceback
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import os

from cities_data import cities_data, city_demands
from vehicle_routing_optimization import VehicleRoutingProblem
from vehicle_routing_visualization import visualize_routes


class VRPOptimizationApp:
    def __init__(self, master):
        self.master = master
        master.title("Optymalizator Tras Pojazdów")
        master.geometry("500x600")  # Zwiększony rozmiar okna

        # Ramka dla parametrów
        params_frame = tk.LabelFrame(master, text="Parametry Optymalizacji")
        params_frame.pack(padx=10, pady=10, fill="x")

        # Liczba pojazdów
        tk.Label(params_frame, text="Liczba pojazdów:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.vehicles_spin = tk.Spinbox(params_frame, from_=1, to=10, width=10)
        self.vehicles_spin.delete(0, tk.END)
        self.vehicles_spin.insert(0, "5")
        self.vehicles_spin.grid(row=0, column=1, padx=5, pady=5)

        # Ładowność pojazdu
        tk.Label(params_frame, text="Ładowność pojazdu:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.capacity_spin = tk.Spinbox(params_frame, from_=100, to=5000, width=10)
        self.capacity_spin.delete(0, tk.END)
        self.capacity_spin.insert(0, "1000")
        self.capacity_spin.grid(row=1, column=1, padx=5, pady=5)

        # Liczba generacji
        tk.Label(params_frame, text="Liczba generacji:").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.generations_spin = tk.Spinbox(params_frame, from_=50, to=1000, width=10)
        self.generations_spin.delete(0, tk.END)
        self.generations_spin.insert(0, "75")
        self.generations_spin.grid(row=2, column=1, padx=5, pady=5)

        # Przyciski
        buttons_frame = tk.Frame(master)
        buttons_frame.pack(padx=10, pady=10, fill="x")

        optimize_button = tk.Button(
            buttons_frame, text="Optymalizuj Trasy", command=self.optimize_routes
        )
        optimize_button.pack(side="left", expand=True, padx=5)

        show_map_button = tk.Button(
            buttons_frame, text="Pokaż Mapę", command=self.show_map, state="disabled"
        )
        show_map_button.pack(side="left", expand=True, padx=5)
        self.show_map_button = show_map_button

        # Obszar wyników
        results_frame = tk.LabelFrame(master, text="Wyniki Optymalizacji")
        results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.results_text = tk.Text(results_frame, height=20, width=50, wrap=tk.WORD)
        self.results_text.pack(padx=5, pady=5, fill="both", expand=True)

        # Scrollbar dla wyników
        scrollbar = tk.Scrollbar(results_frame, command=self.results_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.results_text.config(yscrollcommand=scrollbar.set)

        # Zmienna do przechowywania najlepszych tras
        self.best_routes = None

    def optimize_routes(self):
        try:
            # Wyłączenie przycisku mapy
            self.show_map_button.config(state="disabled")

            # Pobranie parametrów
            num_vehicles = int(self.vehicles_spin.get())
            vehicle_capacity = int(self.capacity_spin.get())
            generations = int(self.generations_spin.get())

            # Utworzenie problemu VRP
            vrp = VehicleRoutingProblem(
                cities_data,
                city_demands,
                num_vehicles=num_vehicles,
                vehicle_capacity=vehicle_capacity,
            )

            # Uruchomienie algorytmu genetycznego
            self.best_routes = vrp.genetic_algorithm(
                population_size=100, generations=generations
            )

            # Przygotowanie wyników
            results = "Optymalne trasy dla pojazdów:\n\n"
            total_distance = 0

            for i, route in enumerate(self.best_routes, 1):
                results += f"Pojazd {i}:\n"
                full_route = ["Kraków"] + route + ["Kraków"]
                results += " -> ".join(full_route) + "\n\n"

                route_distance = 0
                current_city = "Kraków"
                current_demand = 0

                for city in route:
                    current_demand += city_demands[city]
                    city_index = list(cities_data.keys()).index(city)
                    current_index = list(cities_data.keys()).index(current_city)
                    route_distance += vrp.distance_matrix[current_index][city_index]
                    current_city = city

                # Dodanie dystansu powrotu do Krakowa
                city_index = list(cities_data.keys()).index("Kraków")
                current_index = list(cities_data.keys()).index(current_city)
                route_distance += vrp.distance_matrix[current_index][city_index]

                total_distance += route_distance
                results += f"Trasa pojazdu {i}: {route_distance:.2f} km, zapotrzebowanie: {current_demand}\n"

            results += f"\nŁączna długość tras: {total_distance:.2f} km"

            # Wyświetlenie wyników
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, results)

            # Włączenie przycisku mapy
            self.show_map_button.config(state="normal")

        except Exception as e:
            error_msg = (
                f"Błąd podczas optymalizacji:\n{str(e)}\n\n{traceback.format_exc()}"
            )
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, error_msg)

    def show_map(self):
        if self.best_routes is None:
            messagebox.showwarning("Uwaga", "Najpierw przeprowadź optymalizację!")
            return

        try:
            # Wizualizacja tras
            visualize_routes(cities_data, self.best_routes)

            # Próba otwarcia mapy w domyślnej przeglądarce
            map_path = os.path.join(os.getcwd(), "vehicle_routing_map.html")
            webbrowser.open(f"file://{map_path}")

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można wyświetlić mapy: {str(e)}")


def main():
    root = tk.Tk()
    app = VRPOptimizationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
