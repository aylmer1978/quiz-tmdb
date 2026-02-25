import requests
import random
import re

TMDB_API_KEY = "c61eb536bd77694588bb8ed6e2d43357"
BASE_URL = "https://api.themoviedb.org/3"

def is_latin(text):
    # Checks if text contains only Latin characters, numbers, punctuation, and common symbols.
    # This regex allows:
    # \u0000-\u007F: Basic Latin (ASCII)
    # \u0080-\u00FF: Latin-1 Supplement (Western European)
    # \u0100-\u017F: Latin Extended-A
    # \u0180-\u024F: Latin Extended-B
    # And keeps spaces, punctuation, etc.
    return bool(re.match(r'^[\u0000-\u024F\s\d\W]*$', text))

def get_random_popular_movie_page():
    # TMDB has many pages of popular movies. Pick a random page (1-50) to get variety
    return random.randint(1, 50)

def fetch_popular_movies():
    page = get_random_popular_movie_page()
    url = f"{BASE_URL}/movie/popular?api_key={TMDB_API_KEY}&language=es-ES&page={page}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        # Filter out movies with non-Latin titles
        latin_results = [m for m in results if is_latin(m.get('title', ''))]
        return latin_results
    return []

def fetch_popular_people():
    page = random.randint(1, 50)
    url = f"{BASE_URL}/person/popular?api_key={TMDB_API_KEY}&language=es-ES&page={page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def fetch_person_details(person_id):
    """Fetch details of a person including their profile photo."""
    url = f"{BASE_URL}/person/{person_id}?api_key={TMDB_API_KEY}&language=es-ES"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_person_movie_credits(person_id):
    """Fetch movie credits for a person (actor/director)."""
    url = f"{BASE_URL}/person/{person_id}/movie_credits?api_key={TMDB_API_KEY}&language=es-ES"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Filter cast movies with Latin titles
        cast = [m for m in data.get('cast', []) if is_latin(m.get('title', ''))]
        # Filter crew movies with Latin titles
        crew = [m for m in data.get('crew', []) if is_latin(m.get('title', ''))]
        return {'cast': cast, 'crew': crew}
    return {'cast': [], 'crew': []}

def fetch_movie_credits(movie_id):
    """Fetch cast and crew for a movie."""
    url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=es-ES"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_movie_details(movie_id):
    """Fetch detailed information about a movie including budget."""
    url = f"{BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&language=es-ES"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def generate_question():
    """
    Generates a random question.
    Types of questions:
    1. Guess the release year of a movie.
    2. Guess the popularity of a movie (higher/lower? - maybe too hard, let's stick to multiple choice facts).
    3. Which movie has this overview?
    4. Who is this actor? (if we had images, but text only for now: "Which actor is known for...")
    
    Let's start with: "In what year was [Movie] released?"
    """
    
    # Decide question type
    q_type = random.choice(['release_date', 'vote_average', 'actor_movie', 'director_movie', 'budget'])
    
    movies = fetch_popular_movies()
    if not movies:
        return None
    
    target_movie = random.choice(movies)
    
    if q_type == 'release_date':
        if 'release_date' not in target_movie or not target_movie['release_date']:
            return generate_question() # Retry
            
        correct_year = target_movie['release_date'].split('-')[0]
        question_text = f"¿En qué año se estrenó la película '{target_movie['title']}'?"
        
        # Generate options
        options = {correct_year}
        while len(options) < 5:
            # Generate random years around the correct one
            fake_year = str(int(correct_year) + random.randint(-5, 5))
            options.add(fake_year)
            
        options_list = list(options)
        random.shuffle(options_list)
        
        return {
            "question": question_text,
            "options": options_list,
            "answer": correct_year,
            "type": "release_date"
        }
        
    elif q_type == 'vote_average':
        # Question: Which movie has a rating of X? (Might be ambiguous)
        # Better: What is the rating of [Movie]?
        rating = target_movie.get('vote_average', 0)
        question_text = f"¿Cuál es la valoración (0-10) de la película '{target_movie['title']}' en TMDB?"
        
        correct_rating = f"{rating:.1f}"
        options = {correct_rating}
        
        while len(options) < 5:
            fake_rating = f"{random.uniform(1, 10):.1f}"
            options.add(fake_rating)
            
        options_list = list(options)
        random.shuffle(options_list)
        
        return {
            "question": question_text,
            "options": options_list,
            "answer": correct_rating,
            "type": "vote_average"
        }
    
    elif q_type == 'actor_movie':
        # Question: In which movie does this actor appear?
        people = fetch_popular_people()
        if not people:
            return generate_question()
        
        # Find an actor with a profile photo and movie credits
        actor = None
        actor_movies = None
        for _ in range(10):  # Try up to 10 actors
            candidate = random.choice(people)
            if not candidate.get('profile_path'):
                continue
            
            credits = fetch_person_movie_credits(candidate['id'])
            cast_movies = credits.get('cast', [])
            # Filter movies with Latin titles
            latin_movies = [m for m in cast_movies if is_latin(m.get('title', ''))]
            
            if latin_movies:
                actor = candidate
                actor_movies = latin_movies
                break
        
        if not actor or not actor_movies:
            return generate_question()
        
        correct_movie = random.choice(actor_movies)
        question_text = f"¿En qué película aparece {actor['name']}?"
        
        # Generate options
        options = {correct_movie['title']}
        all_movies = fetch_popular_movies()
        
        while len(options) < 5 and all_movies:
            fake_movie = random.choice(all_movies)
            if fake_movie['title'] != correct_movie['title']:
                options.add(fake_movie['title'])
        
        if len(options) < 5:
            return generate_question()
        
        options_list = list(options)
        random.shuffle(options_list)
        
        return {
            "question": question_text,
            "options": options_list,
            "answer": correct_movie['title'],
            "type": "actor_movie",
            "image_url": actor.get('profile_path')
        }
    
    elif q_type == 'director_movie':
        # Question: Which movie did this director direct?
        movies = fetch_popular_movies()
        if not movies:
            return generate_question()
        
        # Find a movie with a director who has a profile photo
        director = None
        director_movie = None
        
        for _ in range(10):  # Try up to 10 movies
            candidate_movie = random.choice(movies)
            credits = fetch_movie_credits(candidate_movie['id'])
            
            if not credits:
                continue
            
            crew = credits.get('crew', [])
            directors = [c for c in crew if c.get('job') == 'Director']
            
            if directors:
                candidate_director = directors[0]
                # Fetch director details to get photo
                director_details = fetch_person_details(candidate_director['id'])
                
                if director_details and director_details.get('profile_path'):
                    director = director_details
                    director_movie = candidate_movie
                    break
        
        if not director or not director_movie:
            return generate_question()
        
        question_text = f"¿Qué película ha dirigido {director['name']}?"
        
        # Generate options
        options = {director_movie['title']}
        all_movies = fetch_popular_movies()
        
        while len(options) < 5 and all_movies:
            fake_movie = random.choice(all_movies)
            if fake_movie['title'] != director_movie['title']:
                options.add(fake_movie['title'])
        
        if len(options) < 5:
            return generate_question()
        
        options_list = list(options)
        random.shuffle(options_list)
        
        return {
            "question": question_text,
            "options": options_list,
            "answer": director_movie['title'],
            "type": "director_movie",
            "image_url": director.get('profile_path')
        }
    
    elif q_type == 'budget':
        # Question: Which movie has this budget?
        movies = fetch_popular_movies()
        if not movies:
            return generate_question()
        
        # Find a movie with a budget > 0
        target_movie = None
        for _ in range(20):  # Try up to 20 movies
            candidate = random.choice(movies)
            details = fetch_movie_details(candidate['id'])
            
            if details and details.get('budget', 0) > 1000000:  # At least 1 million
                target_movie = details
                break
        
        if not target_movie:
            return generate_question()
        
        budget = target_movie['budget']
        budget_formatted = f"${budget:,}"
        
        question_text = f"¿Qué película tiene un presupuesto de {budget_formatted}?"
        
        # Generate options with similar budgets
        options = {target_movie['title']}
        all_movies = fetch_popular_movies()
        
        while len(options) < 5 and all_movies:
            fake_movie = random.choice(all_movies)
            if fake_movie['title'] != target_movie['title']:
                options.add(fake_movie['title'])
        
        if len(options) < 5:
            return generate_question()
        
        options_list = list(options)
        random.shuffle(options_list)
        
        return {
            "question": question_text,
            "options": options_list,
            "answer": target_movie['title'],
            "type": "budget"
        }

    return None
