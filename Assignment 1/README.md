# Assignment 1 - Movie Reccomendation System

Partner - Ryan Berardi

Grade: 97.07/120 (81%)

## Error in our project: 
The problem with get_genre_rating is not that it returns a dictionary (the grading script handles this case), but because of the incorrect for loop:

`for movie in genre_dict[genre] and movie_averages:`

In this case you are iterating through all the keys in movie_averages, which is not what we want. Instead, we should be iterating through only genre_dict[genre].

After fixing this, the test cases for genre_popularity pass, but the implementation of get_user_genre is still incorrect. Since you are calling get_genre_rating here, you should filter the genre_to_movies to only the genres and movies that the user has rated. With this fixed, the recommend_movies test cases also pass, so you got credit for those as well.
