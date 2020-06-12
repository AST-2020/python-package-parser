# import sklearn.k_means
# from sklearn import k_means
from sklearn import calibration

calibration.CalibratedClassifierCV()


def func1(parameter1, parameter2=None):
    pass

dict = {
    "function":
        {
            "sklearn.k_means":
                {
                    "kmeans_func":
                        ["1", "2", "3", "4"]
                }
        }
    ,
    "method":
        {
            "sklearn.k_means":
                {
                    "kmeans_class": {
                        "kmeans_method":  [1, 2, 3, 4]
                    }


                }
        }
    }

