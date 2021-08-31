# Movie Recommendation Engine

This program gives a user a recommendation for several movies based on movies he has seen before and how he rates them

###The programs require the packages `pandas` and `matplotlib`

## "Normal" run

A "Normal" run consists of the user entering several movies and receiving recommendations  
To run the program enter:
> python main.py

## "Learning" run

A "Learning" run consists of several users entering movies and receiving recommendations, then rating the
recommendation they received, at the end of the run the program let the user know what is the best value for the
parameter and shows a graph of the possible values and there average rating  
### To run the program and test the optimal input size enter '?' as argument followed by an output size, for example:
> python main.py ? 5

### To run the program and test the optimal output size enter as argument an input size followed by '?', for example:
> python main.py 5 ?

## "Normal" run with custom parameters

You can also pass the wanted parameters to the program as parameters,
for example to run the program with input size of 6 and output size of 7 enter:
> python main.py 6 7

## Additional information
This project is a cooperation with Noa, check out her GitHub [here](https://github.com/Noabbo).  
For more information, contact us on [dorefaeli@gmail.com](mailto:dorefaeli@gmail.com).  
This project is base on a different GitHub project that can be found [here](https://github.com/codeheroku/Introduction-to-Machine-Learning/blob/master/Collaborative%20Filtering/Movie%20Lens%20Collaborative%20Filtering.ipynb).