from sklearn.svm._classes import LinearSVC
from sklearn.utils.validation import check_random_state


# funktion
a = check_random_state(seeed=None)                                  # should give an error
b = check_random_state(seed=None)

# constructor
lin: LinearSVC = LinearSVC(penlty='l1', loss='hinge')               # should give an error
lin: LinearSVC = LinearSVC(penalty='l1', loss='hinge')

# methode
lin.fit(x=[0.63, 0.09], Y=0.0)                                      # should give an error
lin.fit(X=[0.63, 0.09], y=0.0)