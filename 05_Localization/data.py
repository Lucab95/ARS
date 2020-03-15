import math

#######################################################
############### GAME PROPERTIES #######################
SIZE_SCREEN = width, height = 700, 790
DUST_SIZE = 400
COLOR_SCREEN = 255,255,255
COLOR_WALLS = 90, 90, 255
COLOR_SENSORS = 255, 90, 255
MAX_DISTANCE_SENSOR = 50
MAX_VELOCITY = [100, 50]
MOTION_STEP = [5, 0.2]
ROBOT_RADIUS = 35
DELTA_T = 0.15
FPS = 200  # Frames per second
ROBOT_DRIVE = True
ROBOT_POSITION = [300, 300, math.radians(0)]
#######################################################
################# GA PROPERTIES #######################
CROSSOVER_PROBABILITY = 0.5
MUTATION_PROBABILITY = 0.05
MUTATION_P_STEP = 5.0
MANTAIN_PARENTS = True

POPULATION_SIZE = 50
PARENTS_NUMBER = int(POPULATION_SIZE / 5)
GENETIC_EPOCHS = 50
MAP_STEPS = 10000000000000000

LOAD = False
LOAD_EPOCH = 49

SCORE_INCIDENCE = 0.9
AVOID_COLLISIONS_INCIDENCE = 1-SCORE_INCIDENCE
#######################################################
################# NNA PROPERTIES ######################
INPUTS_SIZE = 13
HIDDEN_LAYER_SIZE = int(2*INPUTS_SIZE)
OUTPUTS_SIZE = 2
#######################################################
############### OTHER PROPERTIES ######################
SAVING_DIRECTORY, SCORE_DIRECTORY, IMAGES_DIRECTORY, BEST_DIRECTORY = "Save", "Score", "Images", "Best"
#######################################################