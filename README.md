# Vehicle Routing Optimization Application

## Project Description

This application solves the Vehicle Routing Problem (VRP) using a genetic algorithm. It allows users to optimize delivery routes for multiple vehicles, starting from Kraków and visiting various cities in Poland while respecting vehicle capacity constraints.

## Key Features

- Genetic algorithm-based route optimization
- Interactive GUI for parameter configuration
- Visualization of optimal routes on an interactive map
- Detailed route and distance calculations
- Capacity-constrained vehicle routing

## System Requirements

- Python 3.8+
- Windows / macOS / Linux

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/vehicle-routing-problem.git
cd vehicle-routing-problem
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Dependencies

- NumPy: Numerical computations
- Tkinter: GUI framework
- Folium: Interactive map visualization
- GeoPy: Geographical calculations

## Running the Application

```bash
python vehicle_routing_gui.py
```

## Application Parameters

### Optimization Parameters

- **Number of Vehicles**: 1-5 vehicles
- **Vehicle Capacity**: 100-5000 units
- **Generations**: 50-1000 iterations
- **Population Size**: 50-500 individuals
- **Mutation Rate**: 0.0-1.0

### Optimization Process

1. Input city demands and locations
2. Configure optimization parameters
3. Run genetic algorithm
4. Visualize optimal routes on map

## Project Structure

- `cities_data.py`: City location and demand data
- `vehicle_routing_gui.py`: Main application interface
- `vehicle_routing_optimization.py`: Genetic algorithm implementation
- `vehicle_routing_visualization.py`: Route mapping and visualization

## Algorithm Details

- Uses genetic algorithm for route optimization
- Considers vehicle capacity constraints
- Minimizes total route distance
- Ensures all cities are visited
- Starts and ends routes in Kraków

## Visualization Features

- Interactive map with route visualization
- Color-coded routes
- Detailed route information sidebar
- Distance and demand calculations
