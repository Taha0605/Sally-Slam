import numpy as np


def warmUpExercise():   
    A = np.eye(5)
    A[:, 0] += 2
    return A

grader = warmUpExercise()
print(grader)
