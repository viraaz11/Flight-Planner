import time
from flight import Flight
from planner import Planner

def load_test_cases_from_file(filename):
    test_cases = []
    with open(filename, 'r') as file:
        num_test_cases = int(file.readline().strip())  # Number of test cases
        
        for _ in range(num_test_cases):
            n = int(file.readline().strip())  # Number of flights for this test case
            flights = []
            
            # Read each flight's data
            for _ in range(n):
                flight_data = file.readline().strip().split()
                flight_no = int(flight_data[0])
                start_city = int(flight_data[1])
                departure_time = int(flight_data[2])
                end_city = int(flight_data[3])
                arrival_time = int(flight_data[4])
                fare = int(flight_data[5])
                flights.append(Flight(flight_no, start_city, departure_time, end_city, arrival_time, fare))
            
            # Read the start city, end city, t1, and t2 after flights data
            start_city, end_city, t1, t2 = map(int, file.readline().strip().split())
            test_cases.append((flights, start_city, end_city, t1, t2))
    
    return test_cases
def format_route(route):
    """Helper function to format the route for easy reading."""
    if not route:
        return "No route found"
    return [flight.flight_no for flight in route]  # Return array of flight numbers for debug
import time

def compare_outputs(output_file, model_file):
    with open(output_file, 'r') as out_f, open(model_file, 'r') as model_f:
        output_lines = out_f.readlines()
        model_lines = model_f.readlines()

    if len(output_lines) != len(model_lines):
        print("The number of lines in the output does not match the model output.")
        print(f"Output lines: {len(output_lines)}, Model lines: {len(model_lines)}")
        return

    current_test_case = None

    for idx, (out_line, model_line) in enumerate(zip(output_lines, model_lines)):
        out_line = out_line.strip()
        model_line = model_line.strip()

        if out_line.startswith("Test Case"):
            current_test_case = out_line  # Track the current test case
        elif out_line != model_line:
            # Determine the route number and reformat the output for printing
            if out_line.startswith("Route 1:"):
                route_number = 1
                out_line = f"FlightCount - {out_line.split(',')[0].split()[-1]}, ArrivalTime - {out_line.split(',')[-1]}"
                model_line = f"FlightCount - {model_line.split(',')[0].split()[-1]}, ArrivalTime - {model_line.split(',')[-1]}"
            elif out_line.startswith("Route 2:"):
                route_number = 2
                out_line = f"Fare - {out_line.split()[-1]}"
                model_line = f"Fare - {model_line.split()[-1]}"
            elif out_line.startswith("Route 3:"):
                route_number = 3
                out_line = f"FlightCount - {out_line.split(',')[0].split()[-1]}, Fare - {out_line.split(',')[-1]}"
                model_line = f"FlightCount - {model_line.split(',')[0].split()[-1]}, Fare - {model_line.split(',')[-1]}"
            else:
                route_number = "Unknown"

            # Print mismatch details
            print("😔😞 Your output does not match the correct output.")
            print(f"\n* Mismatch in {current_test_case}")
            print(f"    Your Output: Route {route_number}: {out_line}")
            print(f"    Expected Output: Route {route_number}: {model_line}")
            print(f"Your Route {route_number} function is incorrect.\n")
            return  # Stop after finding the first mismatch

    print("All test cases match the expected output !!!. 😊🥳 \n")

def main():
    # Load test cases from file
    test_cases = load_test_cases_from_file('fli1000.txt')
    
    # Open output file
    with open('output.txt', 'w') as output_file:
        start_time2 = time.time()
        for i, (flights, start_city, end_city, t1, t2) in enumerate(test_cases, start=1):
            # Create a flight planner instance
            flight_planner = Planner(flights)
            
            # Route 1: Least Flights, Earliest Arrival
            start_time = time.time()
            route1 = None
            try: 
                route1 = flight_planner.least_flights_earliest_route(start_city, end_city, t1, t2)
            except:
                route1 = flight_planner.least_flights_ealiest_route(start_city, end_city, t1, t2)
            route1_time = time.time() - start_time
            route1_flights_count = len(route1) if route1 else 0
            route1_arrival_time = route1[-1].arrival_time if route1 else "No route"
            #print(f"Route 1 Time: {route1_time:.4f}")
            
            # Route 2: Cheapest Route
            start_time = time.time()
            route2 = flight_planner.cheapest_route(start_city, end_city, t1, t2)
            route2_time = time.time() - start_time
            route2_total_cost = sum(flight.fare for flight in route2)
            #print(f"Route 2 Time: {route2_time:.4f}")
            
            # Route 3: Least Flights, Cheapest Route
            start_time = time.time()
            route3 = flight_planner.least_flights_cheapest_route(start_city, end_city, t1, t2)
            route3_time = time.time() - start_time
            route3_flights_count = len(route3)
            route3_total_cost = sum(flight.fare for flight in route3)
            #print(f"Route 3 Time: {route3_time:.4f}")
            
            # Write output in the specified format, including test case number
            print(f"Test Case {i} Processing ...\n")
            output_file.write(f"Test Case {i} :\n")
            output_file.write(f"Route 1: {route1_flights_count}, {route1_arrival_time}\n")
            output_file.write(f"Route 2: {route2_total_cost}\n")
            output_file.write(f"Route 3: {route3_flights_count}, {route3_total_cost}\n\n")
        end_time2 = time.time()
        print(f"Total time taken by your code: {end_time2-start_time2}")

if __name__ == "__main__":
    main()
    compare_outputs('output.txt', 'model_output.txt')