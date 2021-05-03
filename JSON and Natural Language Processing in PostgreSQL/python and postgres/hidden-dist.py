# Keep this file separate

# https://www.pg4e.com/code/hidden-dist.py


# %load_ext sql
# %config SqlMagic.autocommit=False
# %sql postgresql://pg4e_be9e729093:pg4e_p_d5fab7440699124@pg.pg4e.com:5432/pg4e_be9e729093
# %sql SELECT 1 as "Test"

def secrets():
    return {"host": "",
            "port": 0,
            "database": "",
            "user": "",
            "pass": ""}

def elastic() :
    return {"host": "",
            "prefix" : "",
            "port": 0,
            "scheme": "https",
            "user": "",
            "pass": ""}

def readonly():
    return {"host": "",
            "port": 0,
            "database": "",
            "user": "",
            "pass": ""}

# Return a psycopg2 connection string

# import hidden
# secrets = hidden.readonly()
# sql_string = hidden.psycopg2(hidden.readonly())

# 'dbname=pg4e_data user=pg4e_data_read password=pg4e_p_d5fab7440699124 host=pg.pg4e.com port=5432'

def psycopg2(secrets) :
     return ('dbname='+secrets['database']+' user='+secrets['user']+
        ' password='+secrets['pass']+' host='+secrets['host']+
        ' port='+str(secrets['port']))

# Return an SQLAlchemy string

# import hidden
# secrets = hidden.readonly()
# sql_string = hidden.alchemy(hidden.readonly())

# postgresql://pg4e_data_read:pg4e_p_d5fab7440699124@pg.pg4e.com:5432/pg4e_data

def alchemy(secrets) :
    return ('postgresql://'+secrets['user']+':'+secrets['pass']+'@'+secrets['host']+
        ':'+str(secrets['port'])+'/'+secrets['database'])
