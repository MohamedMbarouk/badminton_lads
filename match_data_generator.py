#Aim is to read player data from a csv, apply a formula for winning/losing, and then saving this data into a new file
#We will start with very crude relational data before moving on to more redined possible outcomes

#Importing required libs
import pandas as pd
from os import path
import numpy as np
from scipy.stats import norm

#Defining the function that will calculate the influence height has on the overall score
def height_influence(pl1_h,pl2_h):
    #The influence via height will be calculated by assuming there is an ideal height, and heights on either side of that tail off via a normal distribution
    #Defining the centralised height that I believe represents the ideal height of a player for this game (i.e. 190 cm)
    height_centre = 190
    height_sigma = 1
    #Creation of a normal distribution# Create the normal distribution
    height_distribution = norm(loc=height_centre, scale=height_sigma)
    #Defining the "normalised" value of a given height in terms of this distribution
    pl1_h_norm = height_distribution.pdf(pl1_h)
    pl2_h_norm = height_distribution.pdf(pl2_h)
    heght_factor = pl1_h_norm - pl2_h_norm
    return(heght_factor)

#Defining the function that will calculate the influence weight has on the overall score
def weight_influence(pl1_w,pl2_w):
    #The influence via weight will be calculated by assuming there is an ideal weight, and weights on either side of that tail off via a normal distribution
    #Defining the centralised height that I believe represents the ideal height of a player for this game (i.e. 85 kg)
    weight_centre = 85
    weight_sigma = 1
    #Creation of a normal distribution
    height_distribution = norm(loc=weight_centre, scale=weight_sigma)
    #Defining the "normalised" value of a given height in terms of this distribution
    pl1_w_norm = height_distribution.pdf(pl1_w)
    pl2_w_norm = height_distribution.pdf(pl2_w)
    weight_factor = pl1_w_norm - pl2_w_norm
    return(weight_factor)

#Defining the function that will calculate the influence age has on the overall score
def age_influence(pl1_age,pl2_age):
    #The influence via age will be calculated by assuming there is an ideal age, and weights on either side of that tail off via a normal distribution
    #Defining the centralised height that I believe represents the ideal height of a player for this game (i.e. 26 years old)
    age_centre = 26
    age_sigma = 1
    #Creation of a normal distribution
    age_distribution = norm(loc=age_centre, scale=age_sigma)
    #Defining the "normalised" value of a given height in terms of this distribution
    pl1_age_norm = age_distribution.pdf(pl1_age)
    pl2_age_norm = age_distribution.pdf(pl2_age)
    age_factor = pl1_age_norm - pl2_age_norm
    return(age_factor)

#Defining the function that will calculate the influence experience has on the overall score
def experience_influence(pl1_experience,pl2_experience):
    #The influence via age will be calculated by taking the log of values and then finding their difference (finding log of division)
    #This is mostly just to introduce more relations for the model to play with than sums or products
    experience_factor = np.log(pl1_experience/pl2_experience)
    return(experience_factor)

#Defining the function that will calculate the influence historic wins has on the overall score
def historic_wins_influence(pl1_historic_wins,pl2_historic_wins):
    #The influence via historic wins will be calculated by taking the log of values and then finding their difference (finding log of division)
    #This is mostly just to introduce more relations for the model to play with than sums or products
    historic_wins_factor = np.log(pl1_historic_wins/pl2_historic_wins)
    return(historic_wins_factor)

#Defining the function that will calculate the influence historic wins has on the overall score
def reaction_time_influence(pl1_reaction_time,pl2_reaction_time):
    #The influence via historic wins will be calculated by taking the log of values and then finding their difference (finding log of division)
    #This is mostly just to introduce more relations for the model to play with than sums or products
    reaction_time_factor = (pl1_reaction_time - pl2_reaction_time)/1000
    return(reaction_time_factor)

#Defining the function that will calculate the influence play_frequency wins has on the overall score
def play_freq_influence(pl1_play_freq,pl2_play_freq):
    #Random formula just to kep making this example interesting. Can be be refined later
    reaction_time_factor = np.power(pl1_play_freq, (pl1_play_freq + 1 - pl2_play_freq))
    return(reaction_time_factor)

#Function that decides the probability that a certain player will beat their opponent, given the features of two players
def match_win_probability(pl1,pl2):
    #Creating a comparison between the features, along with how important that feature is to the overall score

    #Computing the influence the height will have on player 1's win using the dedicated function for it
    height_factor = height_influence(pl1[1],pl2[1])
    #Height impacts the likelihood of winning pretty highly positive so we will make this difference 0.75x
    height_weight = 0.75
    height_impact = (height_factor*height_weight)

    #Computing the influence the height will have on player 1's win using the dedicated function for it
    weight_factor = weight_influence(pl1[2],pl2[2])
    #Height impacts the likelihood of winning pretty highly positive so we will make this difference 0.4x
    weight_weight = 0.4
    weight_impact = (weight_factor*weight_weight)

    #Computing the influence the age will have on player 1's win using the dedicated function for it
    age_factor = age_influence(pl1[3],pl2[3])
    #Age impacts the likelihood of winning pretty mid because players have been chosen to have healthy age ranges hence we'll make it 0.15x
    age_weight = 0.15
    age_impact = (age_factor*age_weight)

    #Computing the influence the experience will have on player 1's win using the dedicated function for it
    experience_factor = age_influence(pl1[4],pl2[4])
    #Experience impacts the likelihood of winning pretty highly so we will multiply it by 1x
    experience_weight = 1
    experience_impact = experience_factor * experience_weight

    #Dominant Hand and Gender are irrelevant to the probability that someone wins so these wont even be factored in

    #Computing the influence the historic win ratio will have on player 1's win using the dedicated function for it
    historic_wins_factor = historic_wins_influence(pl1[7],pl2[7])
    #Historic wins is a strong indicator of a current win so lets make it 0.85
    historic_wins_weight = 0.85
    historic_wins_impact = historic_wins_factor * historic_wins_weight

    #Computing the influence the reaction time will have on player 1's win using the dedicated function for it
    reaction_time_factor = reaction_time_influence(pl1[8],pl2[8])
    #Historic wins is a mid level influence so lets give it 0.60
    reaction_time_weight = 0.60
    reaction_time_impact = reaction_time_factor * reaction_time_weight

    #Computing the play frequency has on player 1's win using the dedicated function for it
    play_freq_factor = play_freq_influence(pl1[9],pl2[9])
    #Historic wins is a mid level influence so lets give it 0.60
    play_freq_weight = 0.60
    play_freq_impact = play_freq_factor * play_freq_weight


    #Defining the final formula to decide a win or not
    win_probability_array = [height_impact,weight_impact,age_impact,experience_impact,historic_wins_impact,reaction_time_impact, play_freq_impact]
    win_probability = np.sum(win_probability_array)

    #Defining the data that will be stored in the match data file
    match_data_for_file = [[pl1[0],pl2[0],win_probability]]

    #Creating a DataFrame to store this data into a file
    df = pd.DataFrame(match_data_for_file, columns=['Player 1','Player 2','Probability of Win for Player 1'])
    #Naming the file to save total player data
    DIR = '/Users/mohamed.alzarai/Desktop/Git/badminton_lads'
    file_path = path.join(DIR,'match_data.csv')
    #Writing the data to the file
    df.to_csv(file_path,index="False")

pl1 = ['A0', 180, 57, 18, 8, 'left', 'male', 0.1395379285251439, 161.4971057029045, 0.7406677446676758, 5, 111.73877665258833, 18.43843639370541, '20/20']
pl2 = ['B0', 145, 63, 25, 16, 'left', 'male', 0.7160196129224035, 520.7949841541415, 0.41951982096165874, 4, 121.78531367751818, 26.188609133556533, '20/20']

#match_win_probability(pl1,pl2)
match_win_probability(pl1,pl2)

'''feature_options = ["Name","Height", "Weight", "Age", "Experience", "Dominant_hand", "Gender", "Historic Win Ratio", "Reaction Time",
                   "Play Frequency", "Athleticism", "Serve Speed","Court Coverage", "Vision"]'''
'''feature_options = ["Play Frequency", "Athleticism", "Serve Speed","Court Coverage", "Vision"]'''