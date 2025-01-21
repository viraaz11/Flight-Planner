from flight import Flight

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """ 
        self.m = len(flights)
        self.n = 0
        for flight in flights:
            self.n = max(self.n, flight.start_city, flight.end_city)
        self.n += 1
        self.cities = [[] for i in range(self.n)]
        for i in flights:
            self.cities[i.start_city].append(i)
    
    class Flights_modified:
        def __init__(self, flight, previous):
            self.flight = flight
            self.flight_no=flight.flight_no
            self.start_city=flight.start_city
            self.departure_time=flight.departure_time
            self.end_city=flight.end_city
            self.arrival_time=flight.arrival_time
            self.fare=flight.fare
            self.previous=previous

    class Heap:    
        def __init__(self, comparison_function, init_array):
            self.compare=comparison_function
            self.data=init_array
            for i in range(len(init_array)-1,-1,-1):
                self.downheap(i)
            
        def upheap(self, index):
            parent = (index - 1) // 2
            if index > 0 and self.compare(self.data[index], self.data[parent]):
                self.data[index], self.data[parent] = self.data[parent], self.data[index]
                self.upheap(parent)
        
        def downheap(self, index):
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            smallest = index
            if left_child < len(self.data) and self.compare(self.data[left_child], self.data[smallest]):
                smallest = left_child
            if right_child < len(self.data) and self.compare(self.data[right_child], self.data[smallest]):
                smallest = right_child
            if smallest != index:
                self.data[index], self.data[smallest] = self.data[smallest], self.data[index]
                self.downheap(smallest)
            
        def insert(self, value):
            self.data.append(value)
            self.upheap(len(self.data) - 1)
        
        def extract(self):
            if len(self.data) == 0:
                return None
            if len(self.data) == 1:
                return self.data.pop()
            top_value = self.data[0]
            self.data[0] = self.data.pop()
            self.downheap(0)        
            return top_value
        
        def top(self):
            if len(self.data) == 0:
                return None
            return self.data[0]
        
    class Queue:
        def __init__(self,m):
            self._val=[None]*m
            self.front=-1
            self.size=0
        def push(self, element):
            if self.size==len(self._val):
                raise ValueError("Queue is full")
            avail=(self.front+self.size)%len(self._val)
            self._val[avail]=element
            self.size+=1
        def empty(self):
            return self.size == 0
        def pop(self):
            if self.empty():
                raise ValueError("Queue is empty")
            element=self._val[self.front]
            self._val[self.front]=None
            self.front=(self.front+1)%len(self._val)
            self.size-=1
            return element
        def frnt(self):
            if self.empty():
                raise ValueError("Queue is empty")
            return self._val[self.front]
        
    def comparison(self, a, b):
        if a[0] == b[0]:
            return a[1].arrival_time < b[1].arrival_time
        return a[0] < b[0]
    
    def comparison2(self, a, b):
        if a[0] == b[0]:
            return a[1] < b[1]
        return a[0] < b[0]
    
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        least_flights = []
        if start_city == end_city: return []
        for city in self.cities:
            city.sort(key=lambda x: x.arrival_time)
        start_flight_candidates = [i for i in self.cities[start_city] if (i.departure_time >= t1 and i.arrival_time <= t2)]
        
        min_time = float("inf")
        min_flights = float("inf")
        for i in start_flight_candidates:
            visited = [False] * (self.m + 1)
            q = self.Queue(self.m)
            curr_flight = None
            q.push((self.Flights_modified(i, None), 1))
            while q.size > 0:
                flight, depth = q.pop()
                visited[flight.flight_no] = True
                if flight.end_city == end_city:
                    if min_flights > depth or (min_flights == depth and flight.arrival_time < min_time):
                        curr_flight = flight
                        min_time = flight.arrival_time
                        min_flights = depth
                    break
                for j in self.cities[flight.end_city]:
                    if not visited[j.flight_no] and j.arrival_time <= t2 and j.departure_time >= flight.arrival_time + 20:
                        visited[j.flight_no] = True
                        q.push((self.Flights_modified(j, flight), depth + 1))
            if curr_flight is not None:
                least_flights = []
                while curr_flight is not None:
                    least_flights.append(curr_flight.flight)
                    curr_flight = curr_flight.previous
        return least_flights[::-1]
        
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        cheapest_route = []
        if start_city == end_city:
            return []
        min_fare = float('inf')
        
        start_flight_candidates = [i for i in self.cities[start_city] if (i.departure_time >= t1 and i.arrival_time <= t2)]
        for i in start_flight_candidates:
            fares = [float('inf')] * (self.m + 1)
            curr_flight = None
            pq = self.Heap(self.comparison, [])
            pq.insert((i.fare, self.Flights_modified(i, None)))
            while pq.top() is not None:
                fare, flight = pq.extract()
                if flight.end_city == end_city:
                    if fare < min_fare:
                        curr_flight = flight
                        min_fare = fare
                    break
                for j in self.cities[flight.end_city]:
                    if fare + j.fare < fares[j.flight_no] and j.arrival_time <= t2 and j.departure_time >= flight.arrival_time + 20:
                        fares[j.flight_no] = fare + j.fare
                        pq.insert((fares[j.flight_no], self.Flights_modified(j, flight)))            
            if curr_flight is not None:
                cheapest_route=[]
                while curr_flight is not None:
                    cheapest_route.append(curr_flight.flight)
                    curr_flight = curr_flight.previous
            
        return cheapest_route[::-1]
        
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """        
        least_cheapest_route = []
        if start_city == end_city:
            return []
        min_depth = float('inf')
        min_fare = float('inf')
        start_flight_candidates = [i for i in self.cities[start_city] if (i.departure_time >= t1 and i.arrival_time <= t2)]
        for i in start_flight_candidates:
            fares = [(float("inf"),float('inf'))] * (self.m + 1)
            curr_flight = None
            pq = self.Heap(self.comparison2, [])
            pq.insert((1, i.fare, self.Flights_modified(i, None)))
            while pq.top() is not None:
                depth, fare, flight = pq.extract()
                if flight.end_city == end_city:
                    if depth < min_depth or (depth == min_depth and fare < min_fare):
                        curr_flight = flight
                        min_fare = fare
                        min_depth = depth
                    break
                for j in self.cities[flight.end_city]:
                    if ((depth + 1 , fare + j.fare) < fares[j.flight_no]) and j.arrival_time <= t2 and j.departure_time >= flight.arrival_time + 20:
                        fares[j.flight_no] = (depth + 1 , fare + j.fare)
                        pq.insert((depth + 1, fares[j.flight_no][1], self.Flights_modified(j, flight)))            
            if curr_flight is not None:
                least_cheapest_route=[]
                while curr_flight is not None:
                    least_cheapest_route.append(curr_flight.flight)
                    curr_flight=curr_flight.previous

        return least_cheapest_route[::-1]