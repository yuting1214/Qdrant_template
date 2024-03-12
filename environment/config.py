from configparser import ConfigParser

def config(section='localdb', filename='./environment/database.ini'):
    # Create a parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)

    # Get section, default to localdb
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            if section == 'flask_redis':
                key_name = param[0].upper()
            else:
                key_name = param[0]
            value = param[1]
            if value.lower() == 'none':
                value = None
            db[key_name] = value
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db

def config_uri(section='railwaydb', filename='./environment/database.ini'):
    # Create a parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)

    # Get section, default to localdb
    if parser.has_section(section):
        params = parser.items(section)
        db = {param[0]: param[1] for param in params}
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    # Construct the URI connection string
    if 'database' in db: # postgresql
        db_uri = f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
    else:
        db_uri = f"mongodb://{db['user']}:{db['password']}@{db['host']}:{db['port']}/"

    return db_uri