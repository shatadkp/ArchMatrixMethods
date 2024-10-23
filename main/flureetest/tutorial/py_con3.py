import csv
import random
import datetime

def generate_random_time(base_value=12000, percentage=5):
    """Generate a random integer within ±percentage% of base_value."""
    delta = base_value * percentage / 100
    return int(random.uniform(base_value - delta, base_value + delta))

def extract_max_id(prefix, triplets):
    """Extract the maximum numeric ID for entities starting with the given prefix."""
    ids = []
    for row in triplets:
        if row[0].startswith(prefix):
            parts = row[0].split()
            if parts[-1].isdigit():
                ids.append(int(parts[-1]))
    return max(ids) if ids else 0

def random_date(start_year=2024, end_year=2024):
    """Generate a random date within the specified year range."""
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + datetime.timedelta(days=random_days)

us_airport_codes = [
    'ATL', 'LAX', 'ORD', 'DFW', 'DEN', 'JFK', 'SFO', 'LAS', 'MCO', 'SEA',
    'EWR', 'CLT', 'PHX', 'MIA', 'IAH', 'BOS', 'MSP', 'FLL', 'DTW', 'PHL'
]

used_flight_numbers = set()

def generate_unique_flight_number():
    """Generate a unique flight number."""
    while True:
        flight_number = random.randint(100, 999)
        if flight_number not in used_flight_numbers:
            used_flight_numbers.add(flight_number)
            return flight_number

def add_flights_to_aircraft(triplets, aircraft_id, num_flights, counters):
    """Add new flights to an existing aircraft."""
    new_triplets = []
    # Get the engine associated with the aircraft
    engine = None
    for triplet in triplets:
        if triplet[0] == aircraft_id and triplet[1] == 'has continuant part':
            engine = triplet[2]
            break
    if engine is None:
        print(f"No engine found for aircraft {aircraft_id}. Skipping.")
        return new_triplets

    for _ in range(num_flights):
        counters['flight_counter'] += 1
        counters['engine_op_counter'] += 1
        counters['temporal_interval_counter'] += 1
        counters['temporal_interval_identifier_counter'] += 1
        counters['flight_data_counter'] += 1

        flight_id = f'act of flight {counters["flight_counter"]}'
        engine_op_id = f'act of engine operation {counters["engine_op_counter"]}'
        temporal_interval_id = f'temporal interval {counters["temporal_interval_counter"]}'
        temporal_interval_identifier_id = f'temporal interval identifier {counters["temporal_interval_identifier_counter"]}'
        flight_data_id = f'flight data {counters["flight_data_counter"]}'

        # Assign unique IDs for designative information content entities
        designative_info_entity_flight_id = f'designative information content entity {counters["designative_info_entity_counter"]}'
        counters['designative_info_entity_counter'] += 1  # Increment counter
        designative_info_entity_engine_op_id = f'designative information content entity {counters["designative_info_entity_counter"]}'
        counters['designative_info_entity_counter'] += 1  # Increment counter

        # Generate new IBEs
        counters['ibe_counter'] += 1
        ibe_actual_time_id = f'information bearing entity {counters["ibe_counter"]}'
        counters['ibe_counter'] += 1
        ibe_flight_name_id = f'information bearing entity {counters["ibe_counter"]}'
        counters['ibe_counter'] += 1
        ibe_engine_op_name_id = f'information bearing entity {counters["ibe_counter"]}'

        # Generate random actual operation time
        actual_operation_time = generate_random_time()

        # Generate random flight details
        origin_airport = random.choice(us_airport_codes)
        destination_airport = random.choice([code for code in us_airport_codes if code != origin_airport])
        flight_date = random_date()
        flight_number = generate_unique_flight_number()

        # Flight name format: AN{FlightNumber}-{Origin}-{Destination}-{Date}
        flight_name = f'AN{flight_number}-{origin_airport}-{destination_airport}-{flight_date.strftime("%Y%m%d")}'

        # Engine operation name format: EO-{Date}-{RandomNumber}
        engine_op_random_number = random.randint(1, 999)
        engine_op_name = f'EO-{flight_date.strftime("%Y%m%d")}-{engine_op_random_number:03d}'

        # Add triplets
        new_triplets.extend([
            [flight_id, 'rdf:type', 'Act of Flight'],
            [aircraft_id, 'participates in', flight_id],
            ['customer 1', 'agent in', flight_id],
            [engine_op_id, 'rdf:type', 'Act of Artifact Employment'],
            [engine, 'participates in', engine_op_id],
            [flight_id, 'has process part', engine_op_id],
            [engine_op_id, 'occurs on', temporal_interval_id],
            [temporal_interval_id, 'rdf:type', 'Temporal Interval'],
            [temporal_interval_identifier_id, 'rdf:type', 'Temporal Interval Identifier'],
            [temporal_interval_identifier_id, 'describes', temporal_interval_id],
            [temporal_interval_identifier_id, 'generically depends on', ibe_actual_time_id],
            [ibe_actual_time_id, 'rdf:type', 'Information Bearing Entity'],
            [ibe_actual_time_id, 'uses measurement unit', 'Second Measurement Unit'],
            [ibe_actual_time_id, 'has integer value', str(actual_operation_time)],
            [flight_data_id, 'rdf:type', 'Descriptive Information Content Entity'],
            [flight_data_id, 'has continuant part', temporal_interval_identifier_id],
            [designative_info_entity_flight_id, 'rdf:type', 'Designative Information Content Entity'],
            [designative_info_entity_flight_id, 'generically depends on', ibe_flight_name_id],
            [designative_info_entity_flight_id, 'designates', flight_id],
            [ibe_flight_name_id, 'rdf:type', 'Information Bearing Entity'],
            [ibe_flight_name_id, 'has text value', flight_name],
            [designative_info_entity_engine_op_id, 'rdf:type', 'Designative Information Content Entity'],
            [designative_info_entity_engine_op_id, 'generically depends on', ibe_engine_op_name_id],
            [designative_info_entity_engine_op_id, 'designates', engine_op_id],
            [ibe_engine_op_name_id, 'rdf:type', 'Information Bearing Entity'],
            [ibe_engine_op_name_id, 'has text value', engine_op_name],
        ])

    return new_triplets

def add_new_aircrafts(triplets, num_aircrafts, num_flights_per_aircraft, counters):
    """Add new aircrafts and their flights."""
    new_triplets = []

    for _ in range(num_aircrafts):
        counters['aircraft_counter'] += 1
        counters['engine_counter'] += 1
        counters['artifact_id_counter'] += 1

        aircraft_id = f'aircraft {counters["aircraft_counter"]}'
        engine_id = f'engine {counters["engine_counter"]}'
        # Reuse flight counters from the last one

        # Generate new IBEs
        counters['ibe_counter'] += 1
        ibe_aircraft_name_id = f'information bearing entity {counters["ibe_counter"]}'
        counters['ibe_counter'] += 1
        ibe_engine_name_id = f'information bearing entity {counters["ibe_counter"]}'

        # Generate literals
        aircraft_name = f'Boeing777_CL786{counters["aircraft_counter"]}'
        engine_name = f'PW306D1_ERT923{counters["engine_counter"]}'

        # Add aircraft and engine triplets
        new_triplets.extend([
            [aircraft_id, 'rdf:type', 'Aircraft'],
            ['customer 1', 'uses', aircraft_id],
            [aircraft_id, 'has continuant part', engine_id],
            [engine_id, 'rdf:type', 'Engine'],
            # Artifact identifier for aircraft
            [f'artifact identifier aircraft {counters["artifact_id_counter"]}', 'rdf:type', 'Artifact Identifier'],
            [f'artifact identifier aircraft {counters["artifact_id_counter"]}', 'generically depends on', ibe_aircraft_name_id],
            [f'artifact identifier aircraft {counters["artifact_id_counter"]}', 'designates', aircraft_id],
            [ibe_aircraft_name_id, 'rdf:type', 'Information Bearing Entity'],
            [ibe_aircraft_name_id, 'has text value', aircraft_name],
            # Artifact identifier for engine
            [f'artifact identifier engine {counters["engine_counter"]}', 'rdf:type', 'Artifact Identifier'],
            [f'artifact identifier engine {counters["engine_counter"]}', 'generically depends on', ibe_engine_name_id],
            [f'artifact identifier engine {counters["engine_counter"]}', 'designates', engine_id],
            [ibe_engine_name_id, 'rdf:type', 'Information Bearing Entity'],
            [ibe_engine_name_id, 'has text value', engine_name],
        ])

        # Add flights to the new aircraft
        flights_triplets = add_flights_to_aircraft(triplets + new_triplets, aircraft_id, num_flights_per_aircraft, counters)
        new_triplets.extend(flights_triplets)

    return new_triplets

def main():
    # Read the current triplets from the CSV file
    with open('output_tripletsU3_mod.csv', mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        triplets = [row for row in reader]

    # Ask the user for input
    num_new_aircrafts = int(input("Enter the number of new aircrafts to add: "))
    num_flights_per_new_aircraft = int(input("Enter the number of flights per new aircraft: "))
    num_new_flights_per_existing_aircraft = int(input("Enter the number of new flights to add to existing aircrafts: "))

    # Initialize counters based on existing IDs
    prefixes = {
        'ibe_counter': 'information bearing entity ',
        'artifact_id_counter': 'artifact identifier aircraft ',
        'engine_counter': 'engine ',
        'aircraft_counter': 'aircraft ',
        'flight_counter': 'act of flight ',
        'engine_op_counter': 'act of engine operation ',
        'temporal_interval_counter': 'temporal interval ',
        'temporal_interval_identifier_counter': 'temporal interval identifier ',
        'designative_info_entity_counter': 'designative information content entity ',
        'flight_data_counter': 'flight data ',
    }
    counters = {}
    for counter_name, prefix in prefixes.items():
        counters[counter_name] = extract_max_id(prefix, triplets)

    new_triplets = []

    # Add new flights to existing aircrafts
    existing_aircrafts = set()
    for row in triplets:
        if row[1] == 'rdf:type' and row[2] == 'Aircraft':
            existing_aircrafts.add(row[0])

    for aircraft_id in existing_aircrafts:
        flights_triplets = add_flights_to_aircraft(triplets + new_triplets, aircraft_id, num_new_flights_per_existing_aircraft, counters)
        new_triplets.extend(flights_triplets)

    # Add new aircrafts with their flights
    aircrafts_triplets = add_new_aircrafts(triplets + new_triplets, num_new_aircrafts, num_flights_per_new_aircraft, counters)
    new_triplets.extend(aircrafts_triplets)

    # Write the extended triplets to a new CSV file
    output_filename = 'extended_tripletsgd7.csv'
    with open(output_filename, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(triplets + new_triplets)

    print(f"Extended triplets have been written to '{output_filename}'.")

if __name__ == "__main__":
    main()
