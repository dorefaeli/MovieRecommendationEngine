import random
import pandas as pd
import sys
import matplotlib.pyplot as plt
from enum import Enum


class Run(Enum):
    NORMAL = 1
    FIND_INPUT_SIZE = 2
    FIND_OUTPUT_SIZE = 3


inputSize = 5
outputSize = 4

# loads ratings and movies
ratings = pd.read_csv('dataset/ratings.csv')
movies = pd.read_csv('dataset/movies.csv')
# combines the ratings with the movies into one table
ratings = pd.merge(movies, ratings).drop(['genres', 'timestamp'], axis=1)
# creates a pivot table that represent for each user (row) the rating he gives to each movie (column)
userRatings = ratings.pivot_table(index=['userId'], columns=['title'], values='rating')
# fills zeros in the table where a certain user didn't rate a certain movie
userRatings = userRatings.dropna(thresh=10, axis=1).fillna(0, axis=1)
# compute pairwise correlation of columns using standard correlation coefficient
corrMatrix = userRatings.corr(method='pearson')


def get_similar(movie_name, movie_rating):
    similar_ratings = corrMatrix[movie_name] * (movie_rating - 2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings


# a function that gets a rating from the user
def inputRating(message):
    while True:
        try:
            user_input = int(input(message + ": "))
            if user_input > 5 or user_input < 1:
                raise ValueError
        except ValueError:
            print("Not a valid rating! Try again.")
            continue
        else:
            return user_input


# a functions that get an answer from the user for a yes\no question
def inputBoolean(message):
    while True:
        user_input = input(message + " Y/N: ")
        if user_input == 'y' or user_input == 'Y':
            return True
        elif user_input == 'n' or user_input == 'N':
            return False
        else:
            print("Not a valid answer! Try again.")


# a function that ask the user to rate random movies
def getUserRatings(num_of_movies_to_select):
    selected_movies = []
    while len(selected_movies) < num_of_movies_to_select:
        movie_name = corrMatrix.sample().T.columns[0]
        if movie_name in selected_movies:
            continue
        answer = inputBoolean('Do you know the movie "{}"?'.format(movie_name))
        if answer:
            selected_movies.append(movie_name)
    user_ratings = []
    for movie_name in selected_movies:
        movie_rating = (movie_name, inputRating('Please rate the movie "{}" from 1-5'.format(movie_name)))
        user_ratings.append(movie_rating)
    return user_ratings


# a function that prints the k best results of the movie recommendation system
def printBestK(user_ratings, k):
    similar_movies = pd.DataFrame()
    for movie, rating in user_ratings:
        similar_movies = similar_movies.append(get_similar(movie, rating), ignore_index=True)

    # TODO remove movies that were selected and show only k
    recommendations = list(similar_movies.sum().sort_values(ascending=False).head(20).index)
    movies_the_user_rated = [name for name, rating in user_ratings]
    final_list = [movie_name for movie_name in recommendations if movie_name not in movies_the_user_rated]
    for i in range(min(k, len(final_list))):
        print("{}. {}".format(i+1, final_list[i]))
    return


# a main function for a "Normal" run of the program
def main():
    printBestK(user_ratings=getUserRatings(inputSize), k=outputSize)
    return


# a main function for a run of the program that is meant to find
# the optimal number of user selections that should be passed to the algorithm
def mainForLearningInputSize():
    print("Finding the optimal number of user selections that should be passed to the algorithm")
    number_of_users = 0
    ratings_by_input_length = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    while True:
        number_of_users += 1
        user_ratings = getUserRatings(5)
        for i in range(1, 6):
            printBestK(random.choices(user_ratings, k=i), outputSize)
            ratings_by_input_length[i] += inputRating('Please rate the list of movies from 1-5')
        if not inputBoolean("Do you want to test another person?"):
            break
    for list_length in ratings_by_input_length.keys():
        ratings_by_input_length[list_length] /= number_of_users

    # Finds the best length and notify the user with print and a graph
    best_list_length = max(ratings_by_input_length, key=ratings_by_input_length.get)
    print("The highest rated list length is: {}".format(best_list_length))
    plt.bar(*zip(*ratings_by_input_length.items()))
    plt.xlabel("Number of selections passed to the algorithm")
    plt.ylabel("Users average rating")
    plt.show()


# a main function for a run of the program that is meant to find
# the optimal number of recommendations that the algorithm should give
def mainForLearningOutputSize():
    print("Finding the optimal number of recommendations that the algorithm should give")
    number_of_users = 0
    ratings_by_output_length = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    while True:
        number_of_users += 1
        user_ratings = getUserRatings(inputSize)
        for i in range(1, 11):
            printBestK(user_ratings, i)
            ratings_by_output_length[i] += inputRating('Please rate the list of movies from 1-5')
        if not inputBoolean("Do you want to test another person?"):
            break
    for list_length in ratings_by_output_length.keys():
        ratings_by_output_length[list_length] /= number_of_users

    # Finds the best length and notify the user with print and a graph
    best_list_length = max(ratings_by_output_length, key=ratings_by_output_length.get)
    print("The highest rated list length is: {}".format(best_list_length))
    plt.bar(*zip(*ratings_by_output_length.items()))
    plt.xlabel("Number of movies recommended to the user")
    plt.ylabel("Users average rating")
    plt.show()


if __name__ == '__main__':
    run_type = Run.NORMAL
    if len(sys.argv) > 1:
        try:
            if len(sys.argv) < 3 or (sys.argv[1] == '?' and sys.argv[2] == '?'):
                raise ValueError
            if sys.argv[1] != '?':
                inputSize = int(sys.argv[1])
                run_type = Run.FIND_OUTPUT_SIZE
            if sys.argv[2] != '?':
                outputSize = int(sys.argv[2])
                if run_type == Run.FIND_OUTPUT_SIZE:
                    run_type = Run.NORMAL
                else:
                    run_type = Run.FIND_INPUT_SIZE
        except ValueError:
            print("invalid arguments")
            exit(1)
    if run_type == Run.NORMAL:
        main()
    elif run_type == Run.FIND_INPUT_SIZE:
        mainForLearningInputSize()
    elif run_type == Run.FIND_OUTPUT_SIZE:
        mainForLearningOutputSize()
