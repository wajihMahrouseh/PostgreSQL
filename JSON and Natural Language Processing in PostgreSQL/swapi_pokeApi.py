
# python3 swapi_pokeApi.py
# Pulls data from the https://pokeapi.co/ API and puts it into our pokeapi table

import psycopg2
import hidden
import requests
import json
import re


# Load the secrets
secrets = hidden.secrets()

conn = psycopg2.connect(host=secrets['host'],
        port=secrets['port'],
        database=secrets['database'],
        user=secrets['user'],
        password=secrets['pass'],
        connect_timeout=3)

cur = conn.cursor()

defaulturl = 'https://pokeapi.co/api/v2/pokemon/1'

print('If you want to restart the spider, run')
print('DROP TABLE IF EXISTS pokeapi CASCADE;')
print(' ')
sql = 'DROP TABLE IF EXISTS pokeapi CASCADE;'
cur.execute(sql)
conn.commit()


sql = '''
CREATE TABLE IF NOT EXISTS pokeapi
(
  id serial,
  body JSONB
  );
'''
print(sql)
cur.execute(sql)
conn.commit()


count = 0
fail = 0
for num in range(100):
    url = f'https://pokeapi.co/api/v2/pokemon/{num + 1}/'
    print(url)
    text = "None"
    try:
        print('=== Url is', url)
        response = requests.get(url)
        text = response.text
        #print('=== Text is', text)
        count = count + 1
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except Exception as e:
        print("Unable to retrieve or parse page",url)
        print("Error",e)
        fail = fail + 1
        if fail > 5 : break
        continue
    # TODO: Add try/except Once we figure out what goes wrong
    js = json.loads(text)

    # Look through all of the "linked data" for other urls to retrieve
    links = ['abilities', 'forms', 'game_indices', 'moves', 'species', 'states', 'types']

    abilities = js.get('abilities')
    forms = js.get('forms')
    game_indices = js.get('game_indices')
    held_item = js.get('held_item')
    moves = js.get('moves')
    species = js.get('species')
    stats = js.get('stats')
    types = js.get('types')

    for stuff_abilities in abilities:
        url = stuff_abilities['ability']['url']
        x = re.findall('^https://.*\/([0-9]|[0-9][0-9]|100)\/$', url)
        if len(x) != 0:
            print(url)
            sql = 'INSERT INTO pokeapi (body) VALUES ( %s );'
            cur.execute(sql, (text, ))

    for stuff_forms in forms:
        url = stuff_forms['url']
        x = re.findall('^https://.*\/([0-9]|[0-9][0-9]|100)\/$', url)
        if len(x) != 0:
            print(url)
            sql = 'INSERT INTO pokeapi (body) VALUES ( %s );'
            cur.execute(sql, (text, ))

    for stuff_game_indices in game_indices:
        url = stuff_game_indices['version']['url']
        x = re.findall('^https://.*\/([0-9]|[0-9][0-9]|100)\/$', url)
        if len(x) != 0:
            print(url)
            sql = 'INSERT INTO pokeapi (body) VALUES ( %s );'
            cur.execute(sql, (text, ))
    if held_item != None:
        
        for stuff_held_item in held_item:
            url = stuff_held_item['item']['url']
            x = re.findall('^https://.*\/([0-9]|[0-9][0-9]|100)\/$', url)
            if len(x) != 0:
                print(url)
                sql = 'INSERT INTO pokeapi (body) VALUES ( %s );'
                cur.execute(sql, (text, ))


        for stuff_held_item in held_item:
            stuff_h = stuff_held_item['version_details']
            for stuff in stuff_h:
                url = stuff['version']
            x = re.findall('^https://.*\/([0-9]|[0-9][0-9]|100)\/$', url)
            if len(x) != 0:
                print(url)
                sql = 'INSERT INTO pokeapi (body) VALUES ( %s );'
                cur.execute(sql, (text, ))


        for stuff_held_item in held_item:
            stuff_h = stuff_held_item['version_details']
            for stuff in stuff_h:
                url = stuff['url']
            x = re.findall('^https://.*\/([0-9]|[0-9][0-9]|100)\/$', url)
            if len(x) != 0:
                print(url)
                sql = 'INSERT INTO pokeapi (body) VALUES ( %s );'
                cur.execute(sql, (text, ))

    for stuff_moves in moves:
        url = stuff_moves['move']['url']
        x = re.findall('^https://.*\/([0-9]|[0-9][0-9]|100)\/$', url)
        if len(x) != 0:
            print(url)
            sql = 'INSERT INTO pokeapi (body) VALUES ( %s );'
            cur.execute(sql, (text, ))


    for stuff_moves in moves:
        stuff_moves = stuff_moves['version_group_details']
        for stuff in stuff_moves:
            url = stuff['move_learn_method']['url']

        x = re.findall('^https://.*\/([0-9]|[0-9][0-9]|100)\/$', url)
        if len(x) != 0:
            print(url)
            sql = 'INSERT INTO pokeapi (body) VALUES ( %s );'
            cur.execute(sql, (text, ))


    for stuff_moves in moves:
        stuff_moves = stuff_moves['version_group_details']
        for stuff in stuff_moves:
            url = stuff['version_group']['url']

        x = re.findall('^https://.*\/([0-9]|[0-9][0-9]|100)\/$', url)
        if len(x) != 0:
            print(url)
            sql = 'INSERT INTO pokeapi (body) VALUES ( %s );'
            cur.execute(sql, (text, ))

    
    url = species['url']
    x = re.findall('^https://.*\/([0-9]|[0-9][0-9]|100)\/$', url)
    if len(x) != 0:
        print(url)
        sql = 'INSERT INTO pokeapi (body) VALUES ( %s );'
        cur.execute(sql, (text, ))    


    for stuff_states in stats:
        url = stuff_states['stat']['url']
        x = re.findall('^https://.*\/([0-9]|[0-9][0-9]|100)\/$', url)
        if len(x) != 0:
            print(url)
            sql = 'INSERT INTO pokeapi (body) VALUES ( %s );'
            cur.execute(sql, (text, ))



    for stuff_types in types:
        url = stuff_types['type']['url']
        x = re.findall('^https://.*\/([0-9]|[0-9][0-9]|100)\/$', url)
        if len(x) != 0:
            print(url)
            sql = 'INSERT INTO pokeapi (body) VALUES ( %s );'
            cur.execute(sql, (text, ))



    conn.commit()
    print(count, 'loaded...')



print(' ')
print(f'Loaded {count} documents')

print('Closing database connection...')
conn.commit()
cur.close()
