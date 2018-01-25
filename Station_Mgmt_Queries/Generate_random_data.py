import random
import string
import datetime

word_file = "/usr/share/dict/words"
WORDS = open(word_file).read().splitlines()

stations = []
programs = []
schedule = []

def station_name():
    name = random.choice(['W', 'K'])
    for i in xrange(3):
        name += random.choice(string.letters).upper()
    return name

def gen_station_table():
    s_count = 12
    first_line = 'INSERT INTO stations(station_id, station_name, location_id, server, active) VALUES'
    print first_line
    while s_count > 0:
        s_id = random.randint(10000, 99999)
        name = station_name()
        location_id = random.randint(1, 9)
        server = random.choice(['serv1', 'serv2', 'serv3'])
        l = s_id, name, location_id, server, 1
        ll = list(l)
        stations.append(ll)
        if s_count > 1:
            print l, ','
        else: print l, ';'
        s_count -= 1

def gen_programming_table():
    prog_count = 30
    first_line = 'INSERT INTO programs(program_id, program_name) VALUES'
    print first_line
    while prog_count > 0:
        prog_id = random.randint(1000000, 9999999)
        prog_name = random.choice(WORDS).upper() + ' ' + random.choice(['SHOW', 'TODAY', 'TONIGHT', 'LIVE', 'IN THE MORNING', 'IN CHARGE', 'IN THE MIDDLE', 'INTO DARKNESS']).upper()
        l = prog_id, prog_name
        ll = list(l)
        programs.append(ll)
        if prog_count > 1:
            print l, ','
        else: print l, ';'
        prog_count -= 1

def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def assign_programming():
    s_ids = []
    a_count = len(programs)
    first_line = 'INSERT INTO programs_2_stations(station_id, program_id) VALUES'
    print first_line
    for s in stations:
        s_ids.append(s[0])
    for p in programs:
        l = p[0], random.choice(s_ids)
        ll = list(l)
        schedule.append(ll)
        if a_count > 1:
            print l, ','
        else: print l, ';'
        a_count -= 1

def random_schedule():
    line_count = 40
    first_line = 'INSERT INTO schedule(event_id, prog_id, start_time_UTC, end_time_UTC) VALUES'
    print first_line
    while line_count > 0:
        event_id = random.randint(100000000, 999999999)
        prog_ids = []
        for p in programs:
            prog_ids.append(p[0])
        prog_id = random.choice(prog_ids)
        start_time_UTC = random_date(datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=100)).replace(second=0, microsecond=0)
        end_time_UTC = start_time_UTC +  datetime.timedelta(minutes=random.choice([30, 60]))
        l = event_id, prog_id, str(start_time_UTC), str(end_time_UTC)
        if line_count > 1:
            print l, ','
        else: print l, ';'
        line_count -= 1

def create_all_tables():
    create_stations = 'CREATE TABLE IF NOT EXISTS stations (\
                      station_id INT(5) NOT NULL,\
                      station_name VARCHAR(45),\
                      location_id INT(2),\
                      server VARCHAR(45),\
                      active BIT ) ;'
    create_locations = 'CREATE TABLE IF NOT EXISTS locations (\
                          location_id INT(5) NOT NULL,\
                          location_name VARCHAR(45) ) ;'
    create_programs = 'CREATE TABLE IF NOT EXISTS programs (\
                      program_id INT(5) NOT NULL,\
                      program_name VARCHAR(45) ) ;'
    create_schedule = 'CREATE TABLE IF NOT EXISTS schedule (\
                      event_id INT(9) NOT NULL,\
                      prog_id INT(9) NOT NULL,\
                      start_time_UTC DATETIME,\
                      end_time_UTC DATETIME  ) ;'
    programs_2_stations = 'CREATE TABLE IF NOT EXISTS programs_2_stations (\
                      station_id INT(5) NOT NULL,\
                      program_id INT(5) NOT NULL ) ;'
    print create_stations, create_locations, create_programs, create_schedule, programs_2_stations

def insert_locations():
    print "INSERT INTO locations(location_id, location_name) VALUES\
            (1, 'Kings Landing'),\
            (2, 'Winterfell'),\
            (3, 'Casterly Rock'),\
            (4, 'The Eyrie'),\
            (5, 'Greywater Watch'),\
            (6, 'Sunspear'),\
            (7, 'Braavos'),\
            (8, 'Meereen'),\
            (9, 'Castle Black') ;"

create_all_tables()
insert_locations()
gen_station_table()
gen_programming_table()
assign_programming()
random_schedule()
