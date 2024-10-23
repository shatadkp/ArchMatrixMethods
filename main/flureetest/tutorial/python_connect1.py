import csv
# final version that works , converts csv to ttl
# Define prefixes
prefixes = {
    '': 'http://api.stardog.com/',  # Using the empty prefix for your namespace
    'owl': 'http://www.w3.org/2002/07/owl#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#'
}

# Function to format URIs
def format_uri(name):
    name = name.strip()
    if not name:
        return None  # Return None for empty names to handle missing data
    if ':' in name:
        prefix, local = name.split(':', 1)
        if prefix in prefixes:
            return f'{prefix}:{local.strip().replace(" ", "_")}'
        else:
            # If the prefix is not defined, treat the whole name as an IRI
            return f'<{name.strip()}>'
    else:
        # Use the empty prefix ':' for names without a specified prefix
        return f':{name.strip().replace(" ", "_")}'

# Map predicates to property URIs and data types
literal_predicates = {
    'has altitude value': (':has_altitude_value', 'xsd:double'),
    'has boolean value': (':has_boolean_value', 'xsd:boolean'),
    'has date value': (':has_date_value', 'xsd:date'),
    'has datetime value': (':has_datetime_value', 'xsd:dateTime'),
    'has decimal value': (':has_decimal_value', 'xsd:decimal'),
    'has double value': (':has_double_value', 'xsd:double'),
    'has integer value': (':has_integer_value', 'xsd:integer'),
    'has latitude value': (':has_latitude_value', 'xsd:double'),
    'has longitude value': (':has_longitude_value', 'xsd:double'),
    'has text value': (':has_text_value', None)
}

# Read CSV file
triples = []
with open('extended_tripletsgd7.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Read header
    for row in reader:
        if len(row) < 3:
            continue  # Skip incomplete rows
        subject, predicate, obj = row[:3]
        triples.append((subject.strip(), predicate.strip(), obj.strip()))

# Prepare data structures
classes = set()
individuals = set()
subclasses = []
triples_ttl = []

# Process triples
for s, p, o in triples:
    s_formatted = format_uri(s)
    p_formatted = p.strip()
    o_formatted = format_uri(o)
    if p_formatted == 'rdf:type':
        if s_formatted and o_formatted:
            # The subject is an individual, the object is a class
            individuals.add(s)
            classes.add(o)
            triples_ttl.append(f"{s_formatted} rdf:type {o_formatted} .")
        else:
            # Handle missing subject or object
            print(f"Warning: Incomplete rdf:type triple with subject '{s}' and object '{o}'")
    elif p_formatted == 'subclass of':
        if s_formatted and o_formatted:
            classes.add(s)
            classes.add(o)
            subclasses.append(f"{s_formatted} rdfs:subClassOf {o_formatted} .")
        else:
            # Handle missing subject or object
            print(f"Warning: Incomplete 'subclass of' triple with subject '{s}' and object '{o}'")
    elif p_formatted in literal_predicates:
        # Handle literals
        property_uri, datatype = literal_predicates[p_formatted]
        if s_formatted:
            if datatype:
                triples_ttl.append(f"{s_formatted} {property_uri} \"{o}\"^^{datatype} .")
            else:
                triples_ttl.append(f"{s_formatted} {property_uri} \"{o}\" .")
        else:
            # Handle missing subject
            print(f"Warning: Missing subject for literal predicate '{p_formatted}' with object '{o}'")
    else:
        # Other properties
        if s_formatted and o_formatted:
            property_uri = f":{p_formatted.replace(' ', '_')}"
            triples_ttl.append(f"{s_formatted} {property_uri} {o_formatted} .")
        else:
            # Handle missing subject or object
            print(f"Warning: Incomplete triple with subject '{s}', predicate '{p_formatted}', and object '{o}'")

# Prepare prefixes in TTL format
ttl_prefixes = '\n'.join([f"@prefix {k}: <{v}> ." for k, v in prefixes.items()])

# Prepare class declarations
class_declarations = []
for cls in classes:
    cls_formatted = format_uri(cls)
    if cls_formatted:
        class_declarations.append(f"{cls_formatted} rdf:type owl:Class .")
    else:
        print(f"Warning: Missing class name for class '{cls}'")

# Combine all parts
ttl_content = '\n'.join([
    ttl_prefixes,
    '',
    '# Class Declarations',
    '\n'.join(class_declarations),
    '',
    '# Subclass Relationships',
    '\n'.join(subclasses),
    '',
    '# Triples',
    '\n'.join(triples_ttl)
])

# Write to TTL file
output_file = 'output_e7dsq1.ttl'
with open(output_file, 'w', encoding='utf-8') as ttl_file:
    ttl_file.write(ttl_content)

print(f"TTL file has been generated as '{output_file}'.")
