#!/usr/bin/python3
import time
import sys


# Multi-line string variable for the main program menu.
MAIN_MENU = (
'''======================================================================
\tEnter 1 to Search for a Movie Title and See its Cast
\tEnter 2 to Search for an Actor/Actress and See their Movies
\tEnter anything else to exit.
======================================================================
Please type an option from the list above:
>>> ''')

# Filename for the IMDB database
# IMDB_FILE = 'imdb_data.tsv'
IMDB_FILE = 'imdb_data_sample.tsv'

def main():
    """Main program execution function.

    This is already written for you and should not be be modified.
    """
    # Two dict objects will serve as efficient data structures for look ups
    titles_index = {}
    actors_index = {}
    start = time.time()
    rows = build_indexes(titles_index, actors_index)
    print('Indexed {:,} rows from {} in {:,.2f}s'.format(
        rows, IMDB_FILE, time.time() - start))
    memory_used = sys.getsizeof(titles_index) + sys.getsizeof(actors_index)
    print('Using {:,.2f}MB of memory'.format(memory_used / 2 ** 20))

    # Stay in the loop until an invalid action is received.
    while True:
        action = input(MAIN_MENU)
        if action == '1':
            search_for_title(titles_index)
        elif action == '2':
            movies_for_actor(actors_index)
        else:
            print('"{}" is not a valid action. Goodbye!'.format(action))
            break


def build_indexes(titles_index, actors_index):
    """Processes IMDB_FILE and populates two dict data structures.

    Args:
        titles_index: Dict data structure keyed by title values from IMDB_FILE
        actors_index: Dict data structure keyed by actor values from IMDB_FILE
    Returns:
        Number of rows read from IMDB_FILE
    """
    line_count = 1

    f = open(IMDB_FILE)

    for line in f:
        line = line.rstrip()
        data =  line.split('\t')
        year = int(data[0])
        title = data[1]
        f_name = data[2]
        l_name = data[3]
        gender = data[4]
        char = data[5]
        name = f_name+" "+l_name
        title_key = title.lower()
        exists = titles_index.get(title_key)
        if exists is not None:
            cast_list = titles_index[title_key][2]
            new_cast_list = [{"name":name},{"gender":gender},{"character":char}]
            cast_list.append(new_cast_list)
            titles_index[title_key][2] = cast_list
        else:
            titles_index[title_key] = [{"year":year},{"title":title},[[{"name":name},{"gender":gender},{"character":char}]]]

        name_key = name.lower()
        exists = actors_index.get(name_key)
        if exists is not None:
            movies_list = actors_index[name_key]
            new_movie_list = [{"year":year},{"title":title},{"character":char}]
            movies_list.append(new_movie_list)
            actors_index[name_key]=movies_list
        else:
            actors_index[name_key] = [[{"year":year},{"title":title},{"character":char}]]

        line_count += 1

    return line_count


def sort_by_name(data):
    """Helper function to be passed to the sort() method for titles_index values.
    
    Args:
        data: dict object
    Return:
        data['name'] Value
    """
    for key in sorted(data.keys()):
        return data['name']


def sort_by_year(data):
    """Helper function to be passed to the sort() method for actors_index values.

    Args:
        data: dict object
    Return:
        data['year'] Value
    """
    for key in sorted(data.keys()):
        return data['year']


def search_for_title(titles_index):
    """Lookup and print the actors/actresses from a movie by title.

    Args:
        titles_index: Dict data structure keyed by title
    """
    u_title = input("Type a movie title: ")
    rest_q = input("Do you want gender restriction ? (yes/no): ")
    gender_rest = None
    if rest_q == "yes":
        rest_q = input("Type of gender restriction ? (male/female): ")
        gender_rest = rest_q.lower()


    title_key = u_title.lower()
    value = titles_index.get(title_key)
    if value is not None:
        year = value[0]["year"]
        title = value[1]["title"]
        print  ('"{}" was released in {}'.format(title,year))
        for cast_list in value[2]:
            name = cast_list[0]["name"]
            gender = cast_list[1]["gender"]
            if gender_rest is not None and gender.lower() != gender_rest:
                continue

            char = cast_list[2]["character"]
            print  ('{} played the character "{}"'.format(name,char))
    else:
        print  ('Sorry, "{}" could not be found'.format(u_title))









def movies_for_actor(actors_index):
    """Lookup and print the movies that an actor/actress starred in.

    Args:
        actors_index: Dict data structure keyed by year
    """
    u_actor = input("Type an actor or actress name: ")
    actor_key = u_actor.lower()
    value = actors_index.get(actor_key)
    if value is not None:

        for cast_list in value:
            year = cast_list[0]["year"]
            title = cast_list[1]["title"]
            char = cast_list[2]["character"]
            print('Played "{}" in {} ({})'.format(char,title,year))

    else:
        print('Sorry, "{}" could not be found'.format(u_actor))



main()
