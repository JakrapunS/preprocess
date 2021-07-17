
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
import requests_with_caching
import json
def get_movies_from_tastedive(name):
    parameters = {"q": name, "type": "movies", "limit": 5}
    tastedive_response = requests_with_caching.get("https://tastedive.com/api/similar", params=parameters)
    py_data = json.loads(tastedive_response.text)
    return py_data



def extract_movie_titles(list):
    titles =[]
    movies = list["Similar"]["Results"]
    for x in movies:
        titles.append(x['Name'])
    return titles

def get_related_titles(titles):
    related_titles=[]
    for x in titles:
        info = get_movies_from_tastedive(x)
        temp_title = extract_movie_titles(info)
        for y in temp_title:
            if y not in related_titles:
                related_titles.append(y)
    return(related_titles)

def get_movie_data(title):
    parameters = {"t": title, 'r': 'json'}
    response = requests_with_caching.get("http://www.omdbapi.com/", params=parameters)
    result = json.loads(response.text)
    return result  

def get_movie_rating(movie):
    score = 0
    for x in movie['Ratings']:
        if x['Source'] == 'Rotten Tomatoes':
            score = int(x['Value'].replace('%',''))
            return score
        else:
            score=0
    return score

def get_sorted_recommendations(list):
    related_list = get_related_titles(list)
    zip_list = []
    for x in related_list:
        rating = get_movie_rating(get_movie_data(x))
        if (x,rating) not in zip_list:
            zip_list.append((x,rating))
   
    zip_list = sorted(zip_list, key = lambda t: t[0])
    zip_list = sorted(zip_list, key = lambda t: t[1],reverse=True)        
    
    ziplist2 = []
    for x in zip_list:
        ziplist2.append(x[0])
    
    return ziplist2
    


get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

