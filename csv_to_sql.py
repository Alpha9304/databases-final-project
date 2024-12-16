import csv

input_csv_file = "gun_ranges.csv"
output_sql_file = "insert_ranges.sql"

def map_yes_no(val):
    if not val or val.strip() == '':
        return 'NULL'
    val_lower = val.strip().lower()
    if val_lower == 'yes':
        return "'Y'"
    elif val_lower == 'no':
        return "'N'"
    return 'NULL'

def map_indoor_outdoor(facility_list):
    indoors = "'N'"
    for item in facility_list:
        item_lower = item.strip().lower()
        if 'indoor' in item_lower:
            indoors = "'Y'"
            break
    return indoors

def parse_facility_details(facility_detail_str):
    if not facility_detail_str:
        return "'N'", "'N'", "'N'", "'N'", "'N'"
    facility_items = [x.strip() for x in facility_detail_str.split(',') if x.strip()]
    indoors = map_indoor_outdoor(facility_items)
    members_only = "'Y'" if any('members only' in f.lower() for f in facility_items) else "'N'"
    public_events = "'Y'" if any('public events' in f.lower() for f in facility_items) else "'N'"
    membership_available = "'Y'" if any('membership available' in f.lower() for f in facility_items) else "'N'"
    handicap_accessible = "'Y'" if any('handicap accessible' in f.lower() for f in facility_items) else "'N'"
    return indoors, members_only, public_events, membership_available, handicap_accessible

def split_columns(column_data):
    if not column_data or column_data.strip() == '':
        return []
    return [val.strip() for val in column_data.split(',') if val.strip()]

def clean_up_str(s):
    """
    Returns a properly escaped SQL string, preserving leading/trailing spaces 
    that are deliberately added to differentiate duplicates.
    """
    if s is None or s == '':
        return 'NULL'
    if s.strip() == '':
        return 'NULL'
    return "'" + s.replace("'", "''") + "'"

seen_addresses = set()

with open(input_csv_file, mode='r', encoding='utf-8-sig') as csvfile, open(output_sql_file, mode='w', encoding='utf-8') as sqlfile:
    reader = list(csv.DictReader(csvfile))
    total_rows = len(reader)
    for i, row in enumerate(reader, 1):
        rid_str = row.get('id', '').strip()
        if not rid_str:
            continue
        try:
            rid = int(rid_str)
        except ValueError:
            continue
        
        # Extract fields from CSV
        name = row.get('name', '')
        address = row.get('street_address', '')
        state = row.get('state', '')
        city = row.get('city', '')
        zipcode = row.get('zipcode', '')
        phone_str = row.get('phone_number', '')
        nssf = row.get('nssf_member', '')
        facility_detail = row.get('facility_detail', '')
        service = row.get('service', '')
        shooting_available = row.get('shooting_avaliable', '')
        distance_str = row.get('distance', '')
        competition_str = row.get('competition', '')
        website = row.get('website', '')

        try:
            phone = int(phone_str)
        except ValueError:
            phone = 0

        if not address.strip():
            continue
        
        while address in seen_addresses:
            address = ' ' + address
        seen_addresses.add(address)
        nssf_member_mapped = map_yes_no(nssf)
        email_escaped = clean_up_str(website)
        name_escaped = clean_up_str(name)
        address_escaped = clean_up_str(address)
        state_escaped = clean_up_str(state)
        city_escaped = clean_up_str(city)
        zipcode_escaped = clean_up_str(zipcode)
        
        sqlfile.write(
            f"INSERT INTO gun_range (rid, name, phone, nssf_member, email, address) "
            f"VALUES ({rid}, {name_escaped}, {phone}, {nssf_member_mapped}, {email_escaped}, {address_escaped});\n"
        )
        sqlfile.write(
            f"INSERT INTO location (address, state, postcode, city, country) "
            f"VALUES ({address_escaped}, {state_escaped}, {zipcode_escaped}, {city_escaped}, 'USA');\n"
        )
        
        indoors, members_only, public_events, membership_available, handicap_accessible = parse_facility_details(facility_detail)
        sqlfile.write(
            f"INSERT INTO facility_details (frid, indoors, members_only, public_events, membership_available, handicap_accessible) "
            f"VALUES ({rid}, {indoors}, {members_only}, {public_events}, {membership_available}, {handicap_accessible});\n"
        )
        
        gun_types = split_columns(shooting_available)
        for gt in gun_types:
            gt_escaped = clean_up_str(gt)
            sqlfile.write(f"INSERT INTO gun_type (gid, type) VALUES ({rid}, {gt_escaped});\n")
        
        distances = split_columns(distance_str)
        for d in distances:
            d_escaped = clean_up_str(d)
            sqlfile.write(f"INSERT INTO distance (did, amount) VALUES ({rid}, {d_escaped});\n")
        
        competitions = split_columns(competition_str)
        for c in competitions:
            c_escaped = clean_up_str(c)
            sqlfile.write(f"INSERT INTO competition (rcid, competition_type) VALUES ({rid}, {c_escaped});\n")
        
        other_opts = split_columns(service)
        for opt in other_opts:
            opt_escaped = clean_up_str(opt)
            sqlfile.write(f"INSERT INTO other_options (orid, option_type) VALUES ({rid}, {opt_escaped});\n")
        
        sqlfile.write("\n")
