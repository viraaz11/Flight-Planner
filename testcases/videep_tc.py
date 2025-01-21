import random
from typing import List, Tuple, Dict
from flight import Flight
from planner import Planner
import time
from datetime import datetime
import sys
from collections import defaultdict

class EnhancedFlightPlannerTester:
    def __init__(self):
        self.MAX_FLIGHTS_PER_CITY = 100
        random.seed(42)
        self.test_results = defaultdict(list)
        self.total_tests = 0
        self.passed_tests = 0

    def print_loading_bar(self, progress: float, width: int = 50):
        """Display a loading bar with percentage."""
        filled = int(width * progress)
        bar = '█' * filled + '░' * (width - filled)
        sys.stdout.write(f'\r[{bar}] {progress * 100:.1f}% ')
        sys.stdout.flush()

    def print_colored(self, text: str, color: str):
        """Print colored text in terminal."""
        colors = {
            'green': '\033[92m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'end': '\033[0m'
        }
        print(f"{colors.get(color, '')}{text}{colors['end']}")

    def generate_test_flights(self, num_cities: int, num_flights: int, max_time: int, max_fare: int,
                              connectivity: float = 0.3, time_distribution: str = 'uniform') -> List[Flight]:
        """Generate test flights with enhanced parameters."""
        flights = []
        flights_per_city = defaultdict(int)

        # Create city pairs based on connectivity
        city_pairs = []
        for i in range(num_cities):
            for j in range(num_cities):
                if i != j and random.random() < connectivity:
                    city_pairs.append((i, j))

        attempts = 0
        while len(flights) < num_flights and attempts < num_flights * 3:
            attempts += 1

            if not city_pairs:  # Regenerate pairs if exhausted
                continue

            start_city, end_city = random.choice(city_pairs)

            if (flights_per_city[start_city] >= self.MAX_FLIGHTS_PER_CITY or
                    flights_per_city[end_city] >= self.MAX_FLIGHTS_PER_CITY):
                continue

            # Generate time based on distribution
            if time_distribution == 'peak_hours':
                # Simulate morning (0-200) and evening (500-700) peak hours
                peak = random.choice(['morning', 'evening'])
                if peak == 'morning':
                    departure_time = random.randint(0, 200)
                else:
                    departure_time = random.randint(500, 700)
            elif time_distribution == 'clustered':
                # Create clusters of flights
                cluster_center = random.randint(0, max_time - 200)
                departure_time = cluster_center + random.randint(-50, 50)
            else:  # uniform
                departure_time = random.randint(0, max_time - 100)

            # Flight duration based on distance (assuming cities are arranged in a grid)
            base_duration = 20 + abs(end_city - start_city) * 10
            duration = base_duration + random.randint(-10, 10)
            arrival_time = departure_time + duration

            if arrival_time > max_time:
                continue

            # Fare based on duration and random factor
            base_fare = duration * random.uniform(0.8, 1.2)
            fare = min(max_fare, int(base_fare + random.randint(-20, 20)))

            flights.append(Flight(len(flights), start_city, departure_time, end_city, arrival_time, fare))
            flights_per_city[start_city] += 1
            flights_per_city[end_city] += 1

        return flights

    def validate_route(self, route: List[Flight], start_city: int, end_city: int, t1: int, t2: int) -> Tuple[bool, str]:
        """Enhanced route validator with detailed checks."""
        if not route:
            return True, "Empty route"

        # Basic validation
        validation_checks = [
            (route[0].start_city == start_city,
             f"Invalid start city. Expected: {start_city}, Got: {route[0].start_city}"),
            (route[-1].end_city == end_city, f"Invalid end city. Expected: {end_city}, Got: {route[-1].end_city}"),
            (route[0].departure_time >= t1, f"Departure too early. Min: {t1}, Got: {route[0].departure_time}"),
            (route[-1].arrival_time <= t2, f"Arrival too late. Max: {t2}, Got: {route[-1].arrival_time}")
        ]

        for condition, message in validation_checks:
            if not condition:
                return False, message

        # Check for duplicate flights
        flight_numbers = [f.flight_no for f in route]
        if len(flight_numbers) != len(set(flight_numbers)):
            return False, "Route contains duplicate flights"

        # Validate connections
        for i in range(len(route) - 1):
            curr_flight, next_flight = route[i], route[i + 1]

            # Check city connectivity
            if curr_flight.end_city != next_flight.start_city:
                return False, f"Disconnected route between flights {curr_flight.flight_no} and {next_flight.flight_no}"

            # Check connection time
            connection_time = next_flight.departure_time - curr_flight.arrival_time
            if connection_time < 20:
                return False, f"Insufficient connection time ({connection_time} min) between flights {curr_flight.flight_no} and {next_flight.flight_no}"

        return True, "Valid route"

    def generate_test_scenarios(self) -> List[Dict]:
        """Generate diverse test scenarios."""
        return [
            # Basic test cases
            {"num_cities": 5, "num_flights": 20, "max_time": 200, "max_fare": 100,
             "connectivity": 0.3, "time_distribution": "uniform"},

            # Large network tests
            {"num_cities": 20, "num_flights": 100, "max_time": 1000, "max_fare": 500,
             "connectivity": 0.2, "time_distribution": "uniform"},

            # Peak hour tests
            {"num_cities": 10, "num_flights": 50, "max_time": 800, "max_fare": 300,
             "connectivity": 0.4, "time_distribution": "peak_hours"},

            # Clustered flights
            {"num_cities": 8, "num_flights": 40, "max_time": 400, "max_fare": 250,
             "connectivity": 0.5, "time_distribution": "clustered"},

            # High connectivity tests
            {"num_cities": 6, "num_flights": 30, "max_time": 300, "max_fare": 200,
             "connectivity": 0.8, "time_distribution": "uniform"},

            # Low connectivity tests
            {"num_cities": 15, "num_flights": 60, "max_time": 600, "max_fare": 400,
             "connectivity": 0.1, "time_distribution": "uniform"},

            # Edge case: Minimal network
            {"num_cities": 3, "num_flights": 10, "max_time": 100, "max_fare": 50,
             "connectivity": 0.5, "time_distribution": "uniform"},

            # Edge case: Dense small network
            {"num_cities": 4, "num_flights": 50, "max_time": 200, "max_fare": 150,
             "connectivity": 0.9, "time_distribution": "clustered"},

            # Stress test: Large sparse network
            {"num_cities": 25, "num_flights": 80, "max_time": 1200, "max_fare": 600,
             "connectivity": 0.15, "time_distribution": "uniform"},

            # Stress test: Many short-duration flights
            {"num_cities": 12, "num_flights": 70, "max_time": 400, "max_fare": 350,
             "connectivity": 0.6, "time_distribution": "clustered"}
        ]

    def run_test(self, planner: Planner, start_city: int, end_city: int, t1: int, t2: int,
                 test_name: str) -> Tuple[bool, float, str]:
        """Run a single test with timing."""
        start_time = time.time()

        try:
            if test_name == "least_flights_earliest":
                route = planner.least_flights_earliest_route(start_city, end_city, t1, t2)
                is_valid, message = self.validate_route(route, start_city, end_city, t1, t2)

            elif test_name == "cheapest":
                route = planner.cheapest_route(start_city, end_city, t1, t2)
                is_valid, message = self.validate_route(route, start_city, end_city, t1, t2)

            elif test_name == "least_flights_cheapest":
                route = planner.least_flights_cheapest_route(start_city, end_city, t1, t2)
                is_valid, message = self.validate_route(route, start_city, end_city, t1, t2)

        except Exception as e:
            return False, time.time() - start_time, f"Exception occurred: {str(e)}"

        return is_valid, time.time() - start_time, message

    def run_comprehensive_tests(self):
        """Run comprehensive test suite with detailed reporting."""
        print("\n🛫 Starting Enhanced Flight Planner Tests 🛬")
        print("=" * 80)

        test_scenarios = self.generate_test_scenarios()
        total_tests = len(test_scenarios) * 3 * 10  # scenarios * methods * time_ranges
        current_test = 0

        test_methods = ["least_flights_earliest", "cheapest", "least_flights_cheapest"]
        time_ranges = [
            lambda mt: (0, mt),  # Full range
            lambda mt: (mt // 2, mt),  # Later half
            lambda mt: (0, mt // 2),  # Earlier half
            lambda mt: (mt // 4, mt // 2),  # Middle section
            lambda mt: (0, mt // 4),  # Early section
            lambda mt: (3 * mt // 4, mt),  # Late section
            lambda mt: (mt // 3, 2 * mt // 3),  # Middle third
            lambda mt: (mt // 10, mt),  # Most of range
            lambda mt: (0, 9 * mt // 10),  # Most of range from start
            lambda mt: (mt // 4, 3 * mt // 4),  # Middle half
        ]

        start_time = time.time()

        for scenario_idx, scenario in enumerate(test_scenarios, 1):
            print(f"\n📊 Test Scenario {scenario_idx}/{len(test_scenarios)}")
            print(f"Parameters: {scenario}")

            flights = self.generate_test_flights(**scenario)
            planner = Planner(flights)

            for time_range in time_ranges:
                t1, t2 = time_range(scenario["max_time"])

                for start_city in range(min(4, scenario["num_cities"])):
                    for end_city in range(min(4, scenario["num_cities"])):
                        if start_city == end_city:
                            continue

                        for method in test_methods:
                            current_test += 1
                            self.print_loading_bar(current_test / total_tests)

                            success, elapsed, message = self.run_test(
                                planner, start_city, end_city, t1, t2, method
                            )

                            self.test_results[method].append({
                                'success': success,
                                'elapsed': elapsed,
                                'message': message,
                                'scenario': scenario
                            })

                            if success:
                                self.passed_tests += 1
                            self.total_tests += 1

        # Final Statistics
        total_time = time.time() - start_time
        print("\n\n📈 Test Results Summary")
        print("=" * 80)
        print(f"Total Tests Run: {self.total_tests}")
        print(f"Tests Passed: {self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests / self.total_tests) * 100:.2f}%")
        print(f"Total Time: {total_time:.2f} seconds")

        # Detailed Method Statistics
        print("\n📊 Method-wise Statistics")
        print("=" * 80)
        for method in test_methods:
            results = self.test_results[method]
            successes = sum(1 for r in results if r['success'])
            avg_time = sum(r['elapsed'] for r in results) / len(results)
            print(f"\n{method}:")
            print(f"  Success Rate: {(successes / len(results)) * 100:.2f}%")
            print(f"  Average Time: {avg_time * 1000:.2f}ms")

            # Show some failure messages if any
            failures = [r for r in results if not r['success']]
            if failures:
                print("  Sample Failures:")
                for f in failures:  # Show first 3 failures
                    print(f"    - {f['message']}")

        print("\n✨ Testing Complete ✨")


if __name__ == "__main__":
    tester = EnhancedFlightPlannerTester()
    tester.run_comprehensive_tests()