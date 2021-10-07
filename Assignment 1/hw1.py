def read_ratings_data(f):
    rating_list = {}
    for line in open(f):
        movie, rating, _ = line.split('|')
        if movie not in rating_list:
            rating_list[movie.strip()] = list()
        rating_list[movie.strip()].append(rating.strip())
    return rating_list

def read_movie_genre(f):
    genre_list = {}
    for line in open(f):
        genre,_,movie = line.split('|')
        genre_list[movie.strip()] = genre.strip()
    return genre_list

def create_genre_dict(genre_list):
    genre_to_movie = {}
    for movie in genre_list:
        genre = genre_list[movie]
        if genre not in genre_to_movie:
            genre_to_movie[genre] = list()
        genre_to_movie[genre].append(movie)
    return genre_to_movie

def calculate_average_rating(rating_list):
    average_rating = {}
    for movie in rating_list:
        sum = 0.0
        len = 0.0
        for num in rating_list[movie]:
            sum += float(num)
            len += 1
        average_rating[movie] = sum / len
    return average_rating

def get_popular_movies(movie_averages, n = 10):
    topn = {}
    m = 0
    if len(movie_averages) < n:
        n = len(movie_averages)
    
    topn = dict(sorted(movie_averages.items(), key = lambda movie: movie[1], reverse = True)[:n])
    return topn
    
def filter_movies(movie_averages, threshold = 3):
    great_filter = {}
    for movie in movie_averages:
        if movie_averages[movie] > threshold:
            great_filter[movie] = movie_averages[movie]
    return great_filter

def get_popular_in_genre(genre, genre_dict, movie_averages, n=5):
    movie_list = genre_dict[genre]
    topn = {}
    if len(movie_list) < n:
        n = len(movie_list)
    for movie in movie_list:
        topn[movie] = movie_averages[movie]
    return get_popular_movies(topn, n)

def get_genre_rating(genre, genre_dict, movie_averages):
    genre_rating = {}
    avg = 0
    num_movies = 0
    for movie in genre_dict[genre] and movie_averages:
        avg += movie_averages[movie]
        num_movies += 1
    avg = avg / num_movies
    genre_rating[genre] = avg
    return genre_rating

def genre_popularity(genre_dict, movie_averages, n = 5):
    genre_avg_unsorted = {}
    popular_genres = {}
    if(len(genre_dict) < n):
        n = len(genre_dict)
    for genre in genre_dict:
        avg = get_genre_rating(genre, genre_dict, movie_averages)
        genre_avg_unsorted.update(avg)
    popular_genres = dict(sorted(genre_avg_unsorted.items(), key = lambda genre: genre[1])[:n])
    return popular_genres

def read_user_ratings(f):
    rating_by_user = {}
    for line in open(f):
        movie, rating, uid = line.split('|')
        if not uid.strip() in rating_by_user:
            rating_by_user[uid.strip()] = [(movie.strip(), rating.strip())]
        else:
            rating_by_user[uid.strip()].append((movie.strip(), rating.strip()))
    return rating_by_user

def get_user_genre(uid, rating_by_user, genre_list):
    genre_to_movie = create_genre_dict(genre_list)
    movie_rating_tuple = rating_by_user[uid]
    movie_to_rating = {}
    user_genre = {}
    genres = {}
    for movie, rating in movie_rating_tuple:
        movie_to_rating[movie] = float(rating)
    for genre in genre_to_movie:
        rating = get_genre_rating(genre, genre_to_movie, movie_to_rating)
        user_genre.update(rating)
    genres = dict(sorted(user_genre.items(), key = lambda genre: genre[1], reverse = True)[:1])
    return genres
        
def recommend_movies(uid, rating_by_user, genre_list, average_rating):
    top_genre_dict = get_user_genre(uid, rating_by_user, genre_list)
    top_genre = ""
    for genre in top_genre_dict:
        top_genre = genre
    movie_rating_tuple_list = rating_by_user[uid]
    movie_to_rating = {}
    unseen_in_genre = {}
    for movie, rating in movie_rating_tuple_list:
        movie_to_rating[movie] = float(rating)
    for movie in average_rating:
        if genre_list[movie] == top_genre and movie not in movie_to_rating:
            unseen_in_genre[movie] = average_rating[movie]
    return dict(sorted(unseen_in_genre.items(), key = lambda movie: movie[1], reverse = True)[:3])
        
def main():
    rating_dict = read_ratings_data("movieRatingSample.txt")
    genre_list = read_movie_genre("genreMovieSample.txt")
    movie_averages = calculate_average_rating(rating_dict)
    #print(get_popular_movies(movie_averages))
    genre_dict = create_genre_dict(genre_list)
    #print(genre_popularity(genre_dict, movie_averages))
    rating_by_user = read_user_ratings("movieRatingSample.txt")
    #print(get_user_genre('1',rating_by_user,genre_list))
    print(recommend_movies('1',rating_by_user, genre_list, movie_averages))
if __name__ == "__main__":
    main()