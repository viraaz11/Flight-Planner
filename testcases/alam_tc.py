import random
from flight import Flight
from planner import Planner

random.seed(10)
adj_map_flights = {}
mem = {}

def generate_random_flights(num_cities, num_flights, max_time, max_fare):
    flights = []
    for i in range(num_flights):
        start_city = random.randint(0, num_cities - 1)
        end_city = random.randint(0, num_cities - 1)
        while end_city == start_city:
            end_city = random.randint(0, num_cities - 1)
        departure_time = random.randint(0, max_time)
        arrival_time = departure_time + random.randint(20, 100)
        fare = random.randint(10, max_fare)
        flights.append(Flight(i, start_city, departure_time, end_city, arrival_time, fare))
    return flights


def generate_all_possible_routes(start_city, end_city, t1, t2):
    if (start_city, end_city) in mem:
        return mem[(start_city, end_city)]
    
    all_routes = []
    def dfs(current_city, current_route, current_time):
        if current_city == end_city:
            all_routes.append(list(current_route))
            return

        for flight in adj_map_flights[current_city]:
            if not current_route:
                if flight.departure_time >= t1 and flight.arrival_time <= t2:
                    current_route.append(flight)
                    dfs(flight.end_city, current_route, flight.arrival_time)
                    current_route.pop()
            else:
                if flight.departure_time >= current_time + 20 and flight.arrival_time <= t2:
                    current_route.append(flight)
                    dfs(flight.end_city, current_route, flight.arrival_time)
                    current_route.pop()

    dfs(start_city, [], t1)
    mem[(start_city, end_city)] = all_routes
    return all_routes


def validate_least_flights_earliest(planner, start_city, end_city, t1, t2):
    all_routes = generate_all_possible_routes(start_city, end_city, t1, t2)
    route = planner.least_flights_earliest_route(start_city, end_city, t1, t2)

    if all_routes == []:
        if route == []:
            return True
        else:
            print("Validation failed: Planner returned a route where none should exist.")
            print(f'start:{start_city}, end:{end_city}')
            print('your route:', [f.flight_no for f in route])
            return False
    
    if route == []:
        print("Validation failed: Planner returned no route while atleast one route exists.")
        print(f'start:{start_city}, end:{end_city}')
        print('one possible route:', [f.flight_no for f in route])
        return False

    num_flights = len(route)
    arrival_time = route[-1].arrival_time

    for alt_route in all_routes:
        if len(alt_route) < num_flights or (len(alt_route) == num_flights and alt_route[-1].arrival_time < arrival_time):
            print("Validation failed: Found a route with fewer flights or earlier arrival.")
            print(f'start:{start_city}, end:{end_city}')
            print('alternative route:', [f.flight_no for f in alt_route])
            print('your route:', [f.flight_no for f in route])
            return False

    return True


def validate_cheapest_route(planner, start_city, end_city, t1, t2):
    all_routes = generate_all_possible_routes(start_city, end_city, t1, t2)
    route = planner.cheapest_route(start_city, end_city, t1, t2)

    if all_routes == []:
        if route == []:
            return True
        else:
            print("Validation failed: Planner returned a route where none should exist.")
            print([f.flight_no for f in route])
            return False
    
    if route == []:
        print("Validation failed: Planner returned no route while atleast one route exists.")
        print(f'start:{start_city}, end:{end_city}')
        print('one possible route:', [f.flight_no for f in route])
        return False

    min_cost = sum(f.fare for f in route)

    for alt_route in all_routes:
        if sum(f.fare for f in alt_route) < min_cost:
            print("Validation failed: Found a route with a cheaper cost.")
            print('alt_route:', [f.flight_no for f in alt_route], ', cost:', sum(f.fare for f in alt_route))
            print('your route:', [f.flight_no for f in route], ', cost:', min_cost)
            return False
    
    return True


def validate_least_flights_cheapest(planner, start_city, end_city, t1, t2):
    all_routes = generate_all_possible_routes(start_city, end_city, t1, t2)
    route = planner.least_flights_cheapest_route(start_city, end_city, t1, t2)

    if all_routes == []:
        if route == []:
            return True
        else:
            print("Validation failed: Planner returned a route where none should exist.")
            print([f.flight_no for f in route])
            return False
    
    if route == []:
        print("Validation failed: Planner returned no route while atleast one route exists.")
        print(f'start:{start_city}, end:{end_city}')
        print('one possible route:', [f.flight_no for f in route])
        return False

    num_flights = len(route)
    min_cost = sum(f.fare for f in route)

    for alt_route in all_routes:
        if (len(alt_route) < num_flights) or (len(alt_route) == num_flights and sum(f.fare for f in alt_route) < min_cost):
            print("Validation failed: Found a route with fewer flights or cheaper cost.")
            print('alt_route:', [f.flight_no for f in alt_route], ', cost:', sum(f.fare for f in alt_route))
            print('your route:', [f.flight_no for f in route], ', cost:', min_cost)
            return False
    
    return True


def check_problem_1(planner, t1, t2, num_cities):
    for start_city in range(num_cities):
        for end_city in range(num_cities):
            if end_city == start_city: continue
            
            if not validate_least_flights_earliest(planner, start_city, end_city, t1, t2):
                print(f'Failed on problem 1: {start_city=} and {end_city=}')
                return
            
    print('Passed Problem 1')


def check_problem_2(planner, t1, t2, num_cities):
    for start_city in range(num_cities):
        for end_city in range(num_cities):
            if end_city == start_city: continue

            if not validate_cheapest_route(planner, start_city, end_city, t1, t2):
                print(f'Failed on problem 2: {start_city=} and {end_city=}')
                return
    
    print('Passed Problem 2')


def check_problem_3(planner, t1, t2, num_cities):
    for start_city in range(num_cities):
        for end_city in range(num_cities):
            if end_city == start_city: continue

            if not validate_least_flights_cheapest(planner, start_city, end_city, t1, t2):
                print(f'Failed on problem 3: {start_city=} and {end_city=}')
                return
    
    print('Passed Problem 3')


def run_tests():
    num_cities = 10
    num_flights = 100
    max_time = 500
    max_fare = 300
    flights = generate_random_flights(num_cities, num_flights, max_time, max_fare)

    for flight in flights:
        if flight.start_city not in adj_map_flights:
            adj_map_flights[flight.start_city] = []
        if flight.end_city not in adj_map_flights:
            adj_map_flights[flight.end_city] = []
        adj_map_flights[flight.start_city].append(flight)   
    
    planner = Planner(flights)

    t1 = 0
    t2 = max_time

    check_problem_1(planner, t1, t2, num_cities)
    check_problem_2(planner, t1, t2, num_cities)
    check_problem_3(planner, t1, t2, num_cities)


if __name__ == "__main__":
    run_tests()
