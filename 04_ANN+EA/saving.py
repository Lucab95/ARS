import os
import numpy as np

def create_directory(dir_name):  # function to create directories required if they don't exist
    try:
        os.mkdir(dir_name)
    except OSError:
        print("Creation of the directory %s failed" % dir_name)
    else:
        print("Successfully created the directory %s " % dir_name)


# Saves the model in a txt file
def save_model_weight(epoch, pop, weights1, weights2):
    name = "gen" + str(epoch) + " " + str(pop)
    np.savetxt(("Save\\" + name + "-w1.txt"), weights1, fmt="%s")
    np.savetxt(("Save\\" + name + "-w2.txt"), weights2, fmt="%s")


# Saves the score in a txt file
def save_model_score(epoch, score, collisions, population_size):
    scores = []
    print(score)

    for i in range(population_size - 1):
        string = "Robot: " + str(i) + " score: "  # str(score[i]) + " collision avoided "# + str(collision[i]) +"\n"
        scores.append(string)
    name = "gen" + str(epoch)
    # scores.append(score)
    np.savetxt(("Score\\" + name + "-score.txt"), scores, fmt="%s")


# Load a model from a txt file
def load_model(epoch, pop):
    try:
        name = "gen" + str(epoch) + " " + str(pop)
        w1 = np.loadtxt((("Save\\" + name + "-w1.txt")))
        w2 = np.loadtxt(("Save\\" + name + "-w2.txt"))
    except:
        print("The indicated model doesn't exist!")
        exit(1)
    return w1, w2
