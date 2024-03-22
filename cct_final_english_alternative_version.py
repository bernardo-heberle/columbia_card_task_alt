#!/usr/bin/env python
# coding: utf-8

# In[1]:


## Import Libraries

from graphics import *
from random import *
import pandas as pd
import numpy as np
from datetime import datetime
import os 
from time import sleep
import platform
from PIL import Image as Img

import pyautogui



'''

Function: adapt_image_size

Purpose: Create new images with size adapted to the screen size/ratio/resolution

Input: width and height of screen
-
Output: Saves resized images and returns the width and height ratios compared to 1920 x 1080 resolution

'''

def adapt_image_size(width, height):
    
    card_1 = Img.open('card1.png')
    card_2 = Img.open('card2.png')
    card_3 = Img.open('card3.png')
    card_4 = Img.open('card4.png')
    
    height_ratio = height/1080
    width_ratio = width/1920
    
    new_width = round(card_1.size[0] * width_ratio)
    new_height = round(card_1.size[1] * height_ratio)


    new_card_1 = card_1.resize((new_width, new_height))
    new_card_2 = card_2.resize((new_width, new_height))
    new_card_3 = card_3.resize((new_width, new_height))
    new_card_4 = card_4.resize((new_width, new_height))

    new_card_1.save("card1_resized.png")
    new_card_2.save("card2_resized.png")
    new_card_3.save("card3_resized.png")
    new_card_4.save("card4_resized.png")

    return width_ratio, height_ratio
    

    
## Getting Height and Width of Screen   

width, height = pyautogui.size()
    
## Defining Height and Width Ratio for resizing

width_ratio, height_ratio = adapt_image_size(width, height)


## Updating Height and Width of Screen

height = height - (100 * height_ratio)


## Defining location variable

x_midpoint = width/2
y_midpoint = height/2
small_font = 18
medium_font = 24
big_font = 36


## Creating Window

win = GraphWin("Columbia Card Task", width, height, autoflush=False)



def main():

    ## Write Title
    title = Text(Point(x_midpoint, height/15), "Columbia Card Task")
    title.setSize(big_font)
    title.draw(win)
    
    
    
    ## Set date to today
    date = datetime.date(datetime.now())
    
    ## Initialize List of all varariables to be stored
    master_list = []
    


    ## Get Rounds, user_id, filename, warm or cold version
    rounds_list = [[10, 30], [250, 750], [1, 3], [3]]
    user_id = get_user_id(win)
    file_name = file_name_maker(win)
    warm_or_cold_var = warm_or_cold(win)
    
 
    ## Practice Round
    demonstration_round(win)
    
    
    
    ## Make Rounds and Blocks
    rounds_and_blocks = create_rounds(rounds_list)
    
    ## Set Variables to rounds and Blocks
    blocks = rounds_list[3][0]
    rounds = blocks*8
    
    
    ## Draw Title
    title.draw(win)
    
    ## Prompt Task Beginning
    prompt_begin_task(win)
    
    
    
    ## Start Main loop for each round
    for round_number in range (0, rounds):
        
        
        ## Set current variables for the round
        current_gain_amount = rounds_and_blocks[round_number][0]
        current_loss_amount = rounds_and_blocks[round_number][1]
        current_amount_bad_cards = rounds_and_blocks[round_number][2]
        
        ## Create empty list for picked cards this round
        picked_cards = []
        
        ## Draw the cards for this round
        cards_list, undraw_list = make_cards(win)
        
        
        ## Display current round condition to user
        current_round_setup = round_setup(win, round_number, rounds_and_blocks)
        
        ## Set variable of pressing next round buttton to False
        next_round = False
        
        ## Loop for picking cards while next round button is not pressed   
        while not next_round:
            
            ## Get mouse click
            click = win.checkMouse()
            
            ## See if next round button is clicked
            next_round = finish_round_button(click)

            ## See which cards were picked and store them in a list with [When card was picked, Card location]
            if (click != None) & (warm_or_cold_var == "Warm"):
                picked_cards, card_selections = card_click(cards_list, click, picked_cards)
                         
            ## If round is cold, display ruler:
            elif (warm_or_cold_var == "Cold"):
            ## Run ruler function so user can pick amount of cards to turn
                storage_list = ruler()
                amount_of_picked_cards = storage_list[0]
                next_round = storage_list[1]
                
        
        
        
        
        ## Store round calculations: [amount of picked cards, When the loss card was selected, net result]    
        if warm_or_cold_var == "Warm":
            current_round_calculations = round_calculations(current_amount_bad_cards,current_loss_amount, current_gain_amount, picked_cards)
       
        if warm_or_cold_var == "Cold":
            current_round_calculations = round_calculations_cold(current_amount_bad_cards,current_loss_amount, current_gain_amount, amount_of_picked_cards)
            round_results = master_list_maker(user_id, date, (round_number + 1),current_gain_amount, 
                                              current_loss_amount, current_amount_bad_cards, 
                                              amount_of_picked_cards, current_round_calculations, 
                                              warm_or_cold_var)
            
        ## If warm version display warm feedback
        if warm_or_cold_var == "Warm":
            undraw_result_cards = warm_round_display(picked_cards, current_round_calculations[1], cards_list, current_gain_amount, current_loss_amount, win)
            round_results = master_list_maker(user_id, date, (round_number + 1),current_gain_amount,
                                              current_loss_amount, current_amount_bad_cards, picked_cards,
                                              current_round_calculations, warm_or_cold_var)
       
        master_list.append(round_results)
        
        ## Erase Round Setup
        current_round_setup[0].undraw()
        current_round_setup[1].undraw()
        current_round_setup[2].undraw()
        current_round_setup[3].undraw()
        
        ## Redraw Cards
        for i in range(32):
            undraw_list[i].undraw()
            
        if warm_or_cold_var == "Warm":
            for i in range(len(card_selections)):
                card_selections[i].undraw()
        if warm_or_cold_var == "Warm":   
            for i in range(len(undraw_result_cards)):
                undraw_result_cards[i].undraw
            
        cards_list, undraw_list = make_cards(win)
        

        
    ## Prompt Researcher
    prompt_researcher(win)
    
   
    ## Set White Background
    reset_window_roots(win)
    
    ## Draw Title
    title = Text(Point(x_midpoint, height/15), "Columbia Card Task")
    title.setSize(big_font)
    title.draw(win)
    

    ## Display results and select 3 random
    binary_list = results_display(master_list, win)
    
    ## Insert Binary list to master_list
    insert_list(binary_list, master_list)
    
    
    ## Store data in Pandas DataFrame  
    master_df = pd.DataFrame(master_list, columns = ["User_ID", "Date", "Round", "Gain", "Loss", "Amount_Loss_Cards", "Amount_Picked_Cards", "Bad_Card", "Net_Outcome", "Warm_or_Cold", "Selected_Final"])
    
    
    ## Reset Window
    reset_window_roots(win)
    
        
    ## Set Directory where file will be saved
    directory_name = "cct_output"
    create_directory(directory_name)
    
    ## Final prompt, display filename, directory, and exit button
    final_display(file_name, directory_name)
    
    
    if is_windows() == True:
        ## Write File with data
        master_df.to_csv(str(directory_name) + "\\" + str(file_name), index = False)
    else:
        master_df.to_csv(str(directory_name) + "/" + str(file_name), index = False)
    
    
'''

Function: get_rounds

Purpose: Get the user to specify the gain amount, loss amount, and quantity of loss cards in each 8 round interval

Input: Graphics Window

Output: List in the following format: [[gain_1, gain_2], [loss_1, loss_2], [prob_1, prob_2], [blocks]]

'''

def get_rounds(win):
    
    ## Prompt user to enter gain amount 1
    prompt_gain_1 = Text(Point(x_midpoint, height/3), "What do you want the gain amount 1 to be?")
    prompt_gain_1.setSize(medium_font)
    prompt_gain_1.draw(win)
    
    
    ## Get the gain amount 1
    get_gain_1 = Entry(Point (x_midpoint, height/2.5), 10)
    get_gain_1.setFill('white')
    get_gain_1.setSize(medium_font)
    get_gain_1.draw(win)
    next_button(win)
    
    ## Exception Handling, Keep getting input until an non-negative integer is inputed
    flag = exception_handler(get_gain_1.getText())
    flag_bad_num = False

    if (flag == False):
        if (int(get_gain_1.getText()) < 0):
            flag_bad_num = True
        
    while flag == True or flag_bad_num == True:
        flag_bad_num = False
        prompt_bad_input = Text(Point(x_midpoint, height/1.5), "Invalid Input: Input Must be a Non-Negative Integer")
        prompt_bad_input.setSize(big_font)
        prompt_bad_input.draw(win)
        next_button(win)
        flag = exception_handler(get_gain_1.getText())
        if (flag == False):
            if (int(get_gain_1.getText()) < 0):
                flag_bad_num = True
        prompt_bad_input.undraw()

    
    gain_1 = int(get_gain_1.getText())
    
    ## Clean Prompt
    prompt_gain_1.undraw()
    get_gain_1.undraw()
        
    
    
    ## Prompt user to enter loss amount 1
    prompt_loss_1 = Text(Point(x_midpoint, height/3), "What do you want the loss amount 1 to be?")
    prompt_loss_1.setSize(medium_font)
    prompt_loss_1.draw(win)
    

    ## Get the loss amount 1
    get_loss_1 = Entry(Point (x_midpoint, height/2.5), 10)
    get_loss_1.setFill('white')
    get_loss_1.setSize(medium_font)
    get_loss_1.draw(win)
    next_button(win)
    
    ## Exception Handling, Keep getting input until an non-negative integer is inputed
    flag = exception_handler(get_loss_1.getText())
    flag_bad_num = False
    
    if (flag == False):
        if (int(get_loss_1.getText()) < 0):
            flag_bad_num = True   
    
    while flag == True or flag_bad_num == True:
        flag_bad_num = False
        prompt_bad_input = Text(Point(x_midpoint, height/1.5), "Invalid Input: Input Must be a Non-Negative Integer")
        prompt_bad_input.setSize(big_font)
        prompt_bad_input.draw(win)
        next_button(win)
        flag = exception_handler(get_loss_1.getText())
        if (flag == False):
            if (int(get_loss_1.getText()) < 0):
                flag_bad_num = True
        prompt_bad_input.undraw()
        
    
    loss_1 = int(get_loss_1.getText())
    
    
    ## Clean Prompt
    prompt_loss_1.undraw()
    get_loss_1.undraw()
    

    ## Prompt user to enter the amount of loss cards 1
    prompt_prob_1 = Text(Point(x_midpoint, height/3), "What do you want the amount of loss cards 1 to be?")
    prompt_prob_1.setSize(medium_font)
    prompt_prob_1.draw(win)
    
    
    ## Get the amount of loss cards 1
    get_prob_1 = Entry(Point (x_midpoint, height/2.5), 10)
    get_prob_1.setFill('white')
    get_prob_1.setSize(medium_font)
    get_prob_1.draw(win)
    next_button(win)
    
    ## Exception Handling, Keep getting input until an non-negative integer is inputed
    flag = exception_handler(get_prob_1.getText())
    flag_bad_num = False
    
    if (flag == False):
        if (int(get_prob_1.getText()) < 0) or (int(get_prob_1.getText()) > 32):
            flag_bad_num = True   
    
    while flag == True or flag_bad_num == True:
        flag_bad_num = False
        prompt_bad_input = Text(Point(x_midpoint, height/1.5), "Invalid Input: Input Must be a Non-Negative Integer Smaller than 33")
        prompt_bad_input.setSize(big_font)
        prompt_bad_input.draw(win)
        next_button(win)
        flag = exception_handler(get_prob_1.getText())
        if (flag == False):
            if (int(get_prob_1.getText()) < 0) or (int(get_prob_1.getText()) > 32):
                flag_bad_num = True
        prompt_bad_input.undraw()
        
    prob_1 = int(get_prob_1.getText())
    
    
    ## Clean Prompt
    prompt_prob_1.undraw()
    get_prob_1.undraw()
    
    ## Prompt user to enter gain 2
    prompt_gain_2 = Text(Point(x_midpoint, height/3), "What do you want the gain amount 2 to be?")
    prompt_gain_2.setSize(medium_font)
    prompt_gain_2.draw(win)
    
    
    ## Get the gain amount 2
    get_gain_2 = Entry(Point (x_midpoint, height/2.5), 10)
    get_gain_2.setFill('white')
    get_gain_2.setSize(medium_font)
    get_gain_2.draw(win)
    next_button(win)
    
    ## Exception Handling, Keep getting input until an non-negative integer is inputed
    flag = exception_handler(get_gain_2.getText())
    flag_bad_num = False
    
    if (flag == False):
        if (int(get_gain_2.getText()) < 0):
            flag_bad_num = True  
    
    while flag == True or flag_bad_num == True:
        flag_bad_num = False
        prompt_bad_input = Text(Point(x_midpoint, height/1.5), "Invalid Input: Input Must be a Non-Negative Integer")
        prompt_bad_input.setSize(big_font)
        prompt_bad_input.draw(win)
        next_button(win)
        flag = exception_handler(get_gain_2.getText())
        if (flag == False):
            if (int(get_gain_2.getText()) < 0):
                flag_bad_num = True
        prompt_bad_input.undraw()
    
    gain_2 = int(get_gain_2.getText())
    
    ## Clean Prompt
    prompt_gain_2.undraw()
    get_gain_2.undraw()
    
        
    ## Prompt user to enter loss amount 2
    prompt_loss_2 = Text(Point(x_midpoint, height/3), "What do you want the loss amount 2 to be?")
    prompt_loss_2.setSize(medium_font)
    prompt_loss_2.draw(win)
    
    
    ## Get the loss amount 2
    get_loss_2 = Entry(Point (x_midpoint, height/2.5), 10)
    get_loss_2.setFill('white')
    get_loss_2.setSize(medium_font)
    get_loss_2.draw(win)
    next_button(win)
    
    ## Exception Handling, Keep getting input until an non-negative integer is inputed
    flag = exception_handler(get_loss_2.getText())
    flag_bad_num = False
    
    if (flag == False):
        if (int(get_loss_2.getText()) < 0):
            flag_bad_num = True
        
    while flag == True or flag_bad_num == True:
        flag_bad_num = False
        prompt_bad_input = Text(Point(x_midpoint, height/1.5), "Invalid Input: Input Must be a Non-Negative Integer")
        prompt_bad_input.setSize(big_font)
        prompt_bad_input.draw(win)
        next_button(win)
        flag = exception_handler(get_loss_2.getText())
        if (flag == False):
            if (int(get_loss_2.getText()) < 0):
                flag_bad_num = True
        prompt_bad_input.undraw()
        
    loss_2 = int(get_loss_2.getText())
    
    ## Clean Prompt
    prompt_loss_2.undraw()
    get_loss_2.undraw()
    
    ## Prompt user to enter the amount of loss cards 2
    prompt_prob_2 = Text(Point(x_midpoint, height/3), "What do you want the amount of loss cards 2 to be?")
    prompt_prob_2.setSize(medium_font)
    prompt_prob_2.draw(win)
    
    
    ## Get the amount of loss cards 2
    get_prob_2 = Entry(Point (x_midpoint, height/2.5), 10)
    get_prob_2.setFill('white')
    get_prob_2.setSize(medium_font)
    get_prob_2.draw(win)
    next_button(win)
    
    ## Exception Handling, Keep getting input until an non-negative integer is inputed
    flag = exception_handler(get_prob_2.getText())
    flag_bad_num = False
    
    if (flag == False):
        if (int(get_prob_2.getText()) < 0) or (int(get_prob_2.getText()) > 32):
            flag_bad_num = True
        
    while flag == True or flag_bad_num == True:
        flag_bad_num = False
        prompt_bad_input = Text(Point(x_midpoint, height/1.5), "Invalid Input: Input Must be a Non-Negative Integer Smaller than 32")
        prompt_bad_input.setSize(big_font)
        prompt_bad_input.draw(win)
        next_button(win)
        flag = exception_handler(get_prob_2.getText())
        if (flag == False):
            if (int(get_prob_2.getText()) < 0) or (int(get_prob_2.getText()) > 32):
                flag_bad_num = True
        prompt_bad_input.undraw()
    
    prob_2 = int(get_prob_2.getText())
    
    ## Clean Prompt
    prompt_prob_2.undraw()
    get_prob_2.undraw()
    
    
    ## Prompt user to enter the amount of blocks
    prompt_blocks = Text(Point(x_midpoint, height/3), "How many blocks do you want there to be?")
    prompt_blocks.setSize(medium_font)
    prompt_blocks.draw(win)
    
    
    ## Get the amount of blocks
    get_blocks = Entry(Point (x_midpoint, height/2.5), 10)
    get_blocks.setFill('white')
    get_blocks.setSize(medium_font)
    get_blocks.draw(win)
    next_button(win)
    
    
    ## Exception Handling, Keep getting input until an integer between 1-5 is imputed
    flag = exception_handler(get_blocks.getText())
    flag_bad_num = False
    
    if (flag == False):
        if (int(get_blocks.getText()) > 5 or int(get_blocks.getText()) < 1):
            flag_bad_num = True
        
    while flag == True or flag_bad_num == True:
        flag_bad_num = False
        prompt_bad_input = Text(Point(x_midpoint, height/1.5), "Invalid Input: Input Must be an Integer Between 1-5")
        prompt_bad_input.setSize(big_font)
        prompt_bad_input.draw(win)
        next_button(win)
        flag = exception_handler(get_blocks.getText())
        if (flag == False):
            if (int(get_blocks.getText()) > 5 or int(get_blocks.getText()) < 1):
                flag_bad_num = True
        prompt_bad_input.undraw()
        
        
    
    blocks = int(get_blocks.getText())
    
    ## Clean Prompt
    prompt_blocks.undraw()
    get_blocks.undraw()
    
    
    
    round_list = [[gain_1, gain_2], [loss_1, loss_2], [prob_1, prob_2], [blocks]]
    return round_list
    
    
    
'''

Function: make_cards

Purpose: Make the 32 cards and store their locations and names

Input: Graphics Window

Output: Center position for each card.

'''

def make_cards(win):

    # Create position variables
    x = width/10
    y = height/3
    card = "card1_resized.png"
    index = np.arange(1, 32)
    cards_list = []
    undraw_list = []
    

   # Create a point for location of the cards
    for i in range (1, 33):
        draw_card = Image(Point(x, y), card)
        draw_card.draw(win)
        undraw_list.append(draw_card)
        cards_list.append([x,y])
        if i%8 == 0:
            y = y + height/7
            x = width/10
        else:
            x = x + width/9
            
    # Return it
    return cards_list, undraw_list



'''

Function: create_rounds

Purpose: Create a list with the gain, loss, and loss cards for each round in each block

Input: List of selected gains, losses, loss cards, and blocks for the tasl
-
Output: List of randomized gains, losses, and loss cards for each round in each block [[gains, losses, loss_cards], [...]....]

'''


def create_rounds(rounds_list):
    
    ## Initialize Variables
    blocks = rounds_list[3][0]
    counter1 = 0
    pre_rounds_and_blocks = []
    final_rounds_and_blocks = []
    flag_repeat_gain = False
    flag_repeat_loss = False
    flag_repeat_loss_cards = False
    equals = 8
    
    if rounds_list[0][0] == rounds_list[0][1]:
        flag_repeat_gain = True
        equals = (equals/2)
    
    if rounds_list[1][0] == rounds_list[1][1]:
        flag_repeat_loss = True
        equals = (equals/2)
        
    if rounds_list[2][0] == rounds_list[2][1]:
        flag_repeat_loss_cards = True
        equals = (equals/2)
        
    ## Loop for blocks
    while counter1 < blocks:
        counter2 = 0
        counter3 = 0
        
        # Loop for rounds
        while counter2 < equals:
            
            
            counter3 = counter3 + 1
            
            ## Initialize random variables from 0-1
            random1 = randrange(0, 2)
            random2 = randrange(0, 2)
            random3 = randrange(0, 2)
            flag = False
            
            ## Create round variable
            single_round = [rounds_list[0][random1],rounds_list[1][random2], rounds_list[2][random3]]
            
            ## If it is the first round append the round with the set conditions
            if counter2 == 0:
                pre_rounds_and_blocks.append(single_round)
                counter2 = counter2 + 1
            ## If it is not the first round check to make sure that all the other rounds in the block are different from the current round  
            else:
                
                ## Handle all cases for all possible combinations of repeated values while creating a list with the maximum amount of unique three variable lists.
                for i in range(0, counter2):
                    
                    if ((flag_repeat_gain == False and flag_repeat_loss == False and flag_repeat_loss_cards == False) and single_round == pre_rounds_and_blocks[i]):
                        flag = True
                        
                    elif flag_repeat_gain:
                        if single_round[1] == pre_rounds_and_blocks[i][1] and single_round[2] == pre_rounds_and_blocks[i][2]:
                            flag = True
                            
                    elif flag_repeat_loss:
                        if single_round[0] == pre_rounds_and_blocks[i][0] and single_round[2] == pre_rounds_and_blocks[i][2]:
                            flag = True
                    
                    elif flag_repeat_loss_cards:
                        if single_round[0] == pre_rounds_and_blocks[i][0] and single_round[1] == pre_rounds_and_blocks[i][1]:
                            flag = True
                            
                    elif flag_repeat_gain and flag_repeat_loss:
                        if single_round[2] == pre_rounds_and_blocks[i][2]:
                            flag = True
                            
                    elif flag_repeat_gain and flag_repeat_loss_cards:
                        if single_round[1] == pre_rounds_and_blocks[i][1]:
                            flag = True
                    
                    elif flag_repeat_loss and flag_repeat_loss_cards:
                        if single_round[0] == pre_rounds_and_blocks[i][0]:
                            flag = True

                        
            ## If the round is different from all the other rounds in the block, append the round.        
            if (flag == False and counter3 != 1):
                pre_rounds_and_blocks.append(single_round)
                counter2 = counter2 + 1
                
        ## If all the values are different then just append to final list
        if equals < 8:
            randomized_round = randomize_and_make_round(pre_rounds_and_blocks)
            
            for i in range(0, len(randomized_round)):
                
                final_rounds_and_blocks.append(randomized_round[i])
            
        ## Else randomize the results and make proper randomized round setups  
        else:
            
            for i in range(0, len(pre_rounds_and_blocks)):
                
                final_rounds_and_blocks.append(pre_rounds_and_blocks[i])
        
        
        ## Reset variables
        pre_rounds_and_blocks = []
            
        counter1 = counter1 + 1
        
        
    ## Return list of rounds and blocks
    return final_rounds_and_blocks



'''

Function: round_setup

Purpose: Display round parameter (gain , losses, loss cards), display round number

Input: Graphics Window

Output: Text on Graphics Window of current round parameters

'''

def round_setup(win, round_number, rounds_and_blocks):
    
    ## Make variable for number of total rounds and current round
    number_of_rounds = (len(rounds_and_blocks))
    round_number_for_display = round_number + 1
    
    ## Display current round out the total rounds 
    round_number_display = Text(Point(width/10, height/15), "Round " + str(round_number_for_display) + " Out Of " + str(number_of_rounds))
    round_number_display.setSize(small_font)
    round_number_display.draw(win)
    
    ## Gain Display Box
    gain_display_box = Rectangle(Point(x_midpoint - width/3 - ((width/192) * 10), height/6.8 - ((width/192) * 2.7)), Point(x_midpoint - width/3 + ((width/192) * 10), height/6.8 + ((width/192) * 2.7)))
    gain_display_box.setFill("white")
    gain_display_box.draw(win)

    
    ## Display current gain amount
    gain_display = Text(Point(x_midpoint - width/3, height/6.8), "Gain: " + str(rounds_and_blocks[round_number][0]))
    gain_display.setSize(small_font)
    gain_display.draw(win)
    
    ## Loss Display Box
    loss_display_box = Rectangle(Point(x_midpoint - ((width/192) * 10), height/6.8 - ((width/192) * 2.7)), Point(x_midpoint + ((width/192) * 10), height/6.8 + ((width/192) * 2.7)))
    loss_display_box.setFill("white")
    loss_display_box.draw(win)
    
    
    ## Display current loss amount
    loss_display = Text(Point(x_midpoint, height/6.8), "Loss: " + str(rounds_and_blocks[round_number][1]))
    loss_display.setSize(small_font)
    loss_display.draw(win)
    
    ## Amount of Loss Cards Box
    loss_cards_display_box = Rectangle(Point(x_midpoint + width/3 - ((width/192) * 22), height/6.8 - ((width/192) * 2.7)), Point(x_midpoint + width/3 + ((width/192) * 22), height/6.8 + ((width/192) * 2.7)))
    loss_cards_display_box.setFill("white")
    loss_cards_display_box.draw(win)
    
    
    ## Display current amount of loss cards
    loss_cards_display = Text(Point(x_midpoint + width/3, height/6.8), "Number of Loss Cards: " + str(rounds_and_blocks[round_number][2]))
    loss_cards_display.setSize(small_font)
    loss_cards_display.draw(win)
    
    ## Create list for return
    round_displays = [round_number_display, gain_display, loss_display, loss_cards_display]
    
    return round_displays



'''

Function: finish_round_button

Purpose: Display a functional next round button

Input: Graphics Window

Output: Displays a next round button and returns Flag indicating if button was pressed (True or False)

'''

def finish_round_button(click):
    
    ## Define Coordinate Variables
    x1 = width/1.13
    x2 = width/1.02
    x_average = (x1 + x2)/2
    y1 = height/1.1
    y2 = height/1.03
    y_average = (y1 + y2)/2
    
    
    ## Draw Next Round Button
    next_round_button = Rectangle(Point(x1,y1), Point(x2, y2))
    next_round_button.draw(win)
    next_round_button_msg = Text(Point( x_average, y_average ), "Next Round")
    next_round_button_msg.setSize(medium_font)
    next_round_button_msg.draw(win)
    
    
    ## See if click is inside next round box
    if click == None:
        click_next_round = False
        
    else:
        click_next_round = inbox(Point(x1, y1), Point(x2, y2), click)
    
    
    ## Undraw next Round Box once it is clicked
    if click_next_round:
        next_round_button.undraw()
        next_round_button_msg.undraw()

    
    return click_next_round
    
    
    
    
    
'''

Purpose: To test a point to see if it is in a box defined by two other points (upper right and lower left) 

Pre-conditions: Two points that define the box, a third point

Post-conditions: True if point3 is inside the box, False if not
    
'''

def inbox(p1, p2, point_click):


# Design:

    # Initialize flag
    flag = False

    # If the point's X is inside the other points' X's and The point's Y is inside the other points' Y's
    if  p1.getX() < point_click.getX() < p2.getX() and p1.getY() < point_click.getY() < p2.getY():
        # Flag is set True
        flag = True

    # Return the flag
    return flag







'''

Purpose: To tell if a card has been clicked, print the amount of cards clicked on window, return list with position and amount of cards clicked

Pre-conditions: The list of centerpoints for all cards, a mouse click, the list of positions and amount of clicked cards

Post-conditions: Returns a list with the location of cards picked and the amount of cards picked [Location, Amount of clicked cards]
    
'''

def card_click(cards_list, click, picked_cards):
   
    ## Define y and x modifiers
    y_mod = 56.5
    x_mod = 42.5
    number_displays = []
    
    ## Loop through cards list
    for i in range (0, len(cards_list)):
        
        ## Set card location to iterator + 1
        card_location = i + 1
        
        ## See if current card has already been picked
        already_pick = already_picked(card_location, picked_cards)
        
        ## Set x and y to the center point of the cards
        x = cards_list[i][0]
        y = cards_list[i][1]
        
        ## See if click is inside any of the cards
        click_cards = inbox(Point((x - x_mod), (y - y_mod)), Point((x + x_mod), (y + y_mod)), click)
        
        ## If file_name = "cct_output\\" + filename + ".csv a card has been clicked and has not been picked yet
        if click_cards == True and already_pick == False:
            
            ## If there are no cards picked yet, set amount of picked cards to 1
            if len(picked_cards) == 0:
                amount_of_picked_cards = 1
            
            ## Otherwise set amount of picked cards to the current amount + 1
            else: 
                amount_of_picked_cards = picked_cards[len(picked_cards)-1][1] + 1
            
            ## Append card location and amount of picked card + display the amount of picked card on screen
            picked_cards.append([card_location, amount_of_picked_cards])
            card_number_display = Text(Point(x, y), str(amount_of_picked_cards))
            card_number_display.setSize(big_font)
            card_number_display.draw(win) 
            number_displays.append(card_number_display)
    
    ## Return list with [Location, Amount of clicked cards]
    return picked_cards, number_displays





'''

Purpose: To tell if a card that has been already picked has been clicked

Pre-conditions: Location of current card clicked

Post-conditions: Returns False is card has not been picked and True if card has been picked
    
'''



def already_picked(card_location, picked_cards):
    
    ## Set already picked flag to False
    already_picked = False
    
    ## Iterate through list of picked cards
    for i in range(0, len(picked_cards)):
        
        ## If any of the picked cards location is equal to the current location of click set flag to True
        if picked_cards[i][0] == card_location:
            already_picked = True
            
    ## Return Flag
    return already_picked






'''

Purpose: Calculate important outcomes from the current round

Pre-conditions: amount of bad cards, loss amount, gain amount, and picked cards for current round

Post-conditions: Returs a list in this format [Amount of picked cards, When the loss card was selected, net result]
    
'''


    
    
    
'''
Purpose: Make a cohesive list with the final outputs for the given round

Pre-conditions: Round Number, conditions, picked cards, and round calculations

Post-conditions: Returs a list in this format [round, gain, loss, loss_cards, amount_of_picked_cards, bad_card, net_outcome]

'''

def master_list_maker(user_id, date, rounds, gain, loss, loss_cards, picked_cards, round_calculations, warm_or_cold_var):
    
    ## Make master list and return it
    if warm_or_cold_var == "Warm":
        
        if len(picked_cards) > 0:
            master_list = [user_id, date, rounds, gain, loss, loss_cards, picked_cards[(len(picked_cards) - 1)][1],
                           round_calculations[1], round_calculations[2], warm_or_cold_var]
    
    ## If no cards are picked return proper output (exception handling)
        else: 
            master_list = [user_id, date, rounds, gain, loss, loss_cards, 0, 0, 0, warm_or_cold_var]
   
    elif warm_or_cold_var == "Cold":
        
        if picked_cards > 0:
            master_list = [user_id, date, rounds, gain, loss, loss_cards, picked_cards, round_calculations[1], round_calculations[2], warm_or_cold_var]
       
        else:
            master_list = [user_id, date, rounds, gain, loss, loss_cards, 0, 0, 0, warm_or_cold_var]
        
    return master_list



'''

Purpose: Make a filename for the file

Pre-conditions: Graphics Window

Post-conditions: A String with the filename

'''



def file_name_maker(win):
    
    flag_file_exists = True
    flag_valid = False
    
    ## Define Date Variable
    date = datetime.date(datetime.now())
    date = str(date)
    
    
    
    prompt_file_exists = Text(Point(x_midpoint, height/1.5), "This filename already exists, try a different filename")
    prompt_file_exists.setSize(big_font)
    
    prompt_file_valid = Text(Point(x_midpoint, height/1.5), "This filename contains illegal characters, try a different filename")
    prompt_file_valid.setSize(big_font)
    
    while ((flag_file_exists == True) or (flag_valid == False)):
    
        ## Prompt user to enter gain amount 1
        prompt_file = Text(Point(x_midpoint, height/3 ), "What do you want the filename to be?")
        prompt_file.setSize(medium_font)
        prompt_file.draw(win)
    
    
        ## Get the gain amount 1
        get_file = Entry(Point (x_midpoint, height/2.5), 40)
        get_file.setFill('white')
        get_file.setSize(medium_font)
        get_file.draw(win)
        next_button(win)
        file_name = str(get_file.getText()) + "(" + date + ")" + ".csv"
                
    
        flag_file_exists = file_already_exist(file_name)
        flag_valid = valid_filename(file_name)
        
        if str(get_file.getText()) == "":
            flag_valid = False
        
        prompt_file.undraw()
        get_file.undraw()
        prompt_file.undraw()
        prompt_file_valid.undraw()
        
        if flag_file_exists == True:
            
            prompt_file_exists.draw(win)
            
        if flag_valid == False:
            prompt_file_valid.draw(win)
            
        
    
    
    ## Clean Prompt
    prompt_file.undraw()
    get_file.undraw()
    prompt_file_exists.undraw()
    prompt_file_valid.undraw
    
    return file_name




'''

Purpose: Reset Graphics Window

Pre-conditions: Graphics Window

Post-conditions: Reset Graphics Window

'''

## Reset Window

def reset_window(win):
    
    for item in win.items[:]:
        item.undraw()
    win.update()
    
    
    
    
    
'''

Purpose: Make next round button

Pre-conditions: Graphics Window

Post-conditions: Next Button

'''

def next_button(win):
    
    
    ## Define Coordinate Variables
    x1 = width/1.1
    x2 = width/1.03
    x_average = (x1 + x2)/2
    y1 = height/1.1
    y2 = height/1.03
    y_average = (y1 + y2)/2
    
    ## Draw Next Round Button
    next_button = Rectangle(Point(x1,y1), Point(x2, y2))
    next_button.draw(win)
    next_button_msg = Text(Point( x_average, y_average ), "Next")
    next_button_msg.setSize(medium_font)
    next_button_msg.draw(win)
    
    
    ## Set click next flag to false
    click_next = False
    
    ## While next round button is not pressed keep the button there.
    while not click_next:
        click = win.getMouse()
        click_next = inbox(Point(x1, y1), Point(x2, y2), click)
        
        
    next_button.undraw()
    next_button_msg.undraw()
    
    
    
'''

Purpose: Checking if Input is an integer

Pre-conditions: Input

Post-conditions: a boolean flag, true if the input is not an integer

'''

def exception_handler(x):
    
    ## Set Flag to False
    flag = False
    
    ## If the value cannot be converted to an integer set flag to True
    try:
        int(x)
    
    except ValueError:
        flag = True
        return flag
    
    ## If value is not a whole number set Flag to true
        if float(x) % 1 != 0:
            flag = True
        
    ## Return Flag, True if value not integer, false if it is integer
    return flag





'''

Purpose: Randomize block and make it have 8 rounds

Pre-conditions: The current unique round items

Post-conditions: The randomized complete block

'''


def randomize_and_make_round(rounds_and_blocks):
    
    
    ## Initiate Variables
    storage_list = []
    random_list = []
    randomized_round = []
    length_round = len(rounds_and_blocks)
    start_position = 0
    end_position = len(rounds_and_blocks)
    j = 0
    k = 0
    
    ## Store the unique values contained in rounds_and_blocks in storage_list
    for i in range(start_position, end_position):
        storage_list.append(rounds_and_blocks[i])
    
    ## Duplicate unique values until storage list has 8 values
    while len(storage_list) < 8:
        storage_list.append(storage_list[k])
        k = k + 1
    
    ## Create a list of random numbers from 0-7 with no repeats
    while j < 8:
        
        flag_already_in_random_list = False
        random = randrange(0, 8)
        
        
        if j == 0:
            random_list.append(random)
            j = j + 1
            flag_already_in_random_list = True
        
        else:
            for k in range (0, len(random_list)):
                if random == random_list[k]:
                    flag_already_in_random_list = True
                    
        if flag_already_in_random_list == False:
            random_list.append(random)
            j = j + 1
    
    ## Make a randomized list with the proper amount of unique values based on the input
    for m in range(0, 8):
        randomized_round.append(storage_list[random_list[m]])
        
    return randomized_round
        


        
        

'''

Purpose: Display the results and select 3 random results and calculate net_earning

Pre-conditions: master list and graphics window

Post-conditions: Display the cold round results, pick three random rounds and display the net outcome

'''


def results_display(master_list, win):
    
    ## Initiate Variables
    x = width/10
    y = height/4
    list_positions = []
    random_list = []
    j = 0
    results_sum = 0
    
    
    ## Display the net earnings for all rounds
    for i in range(1, len(master_list) + 1):
        title = Text(Point(x, y), "Round " + str(master_list[i-1][2]) + ": " + str(master_list[i-1][8]))
        title.setSize(medium_font)
        title.draw(win)
        list_positions.append([x, y])
        if i % 8 == 0:
            x = x + 2*width/10
            y = height/4
            
        if i % 8 != 0:
            y = y + height/12
        
    
    ## Pick the 3 random rounds and calculate their sum
    while j < 3:
    
        flag_already_present = False
        random = randrange(0, len(master_list))
        
        if j == 0:
            
            random_list.append(random)
            j = j + 1
            flag_already_present = True
            
        else: 
            for k in range (0, len(random_list)):
                if random_list[k] == random:
                    flag_already_present = True
            
        if flag_already_present == False:
            random_list.append(random)
            j = j + 1
            
    ## Make a list of whether a number was seleted or not. 1 = selected, 0 = not selected
    outcome_list_binary = outcome_list(random_list, master_list)  
    
    ## Dislpay the 3 random rounds and the net sum
    for m in range(0, len(random_list)):
        x_pos = list_positions[random_list[m]][0]
        y_pos = list_positions[random_list[m]][1]
        
        results_sum = results_sum + master_list[random_list[m]][8]
            
        x1 = x_pos + width/13.5
        x2 = x_pos - width/13.5
            
        y1 = y_pos + height/25
        y2 = y_pos - height/25
            
        next_button(win)
        box = Rectangle(Point(x1,y1), Point(x2, y2))
        box.draw(win)
            
    final_result = Text(Point(x_midpoint, height/1.05), "Net Earning: " + str(results_sum))
    final_result.setSize(big_font)
    final_result.draw(win)
            
    next_button(win)
    
    return outcome_list_binary
    
    
    
    
'''

Purpose: Make buttons and return if person picked warm or cold

Pre-conditions: graphics window

Post-conditions: string variable - "Warm" if round is warm, "Cold" if round is cold.

'''




def warm_or_cold(win):
    
    
    ## Define Warn Coordinate Variables
    x1_warm = width/3
    x2_warm = width/2.5
    x_average_warm = (x1_warm + x2_warm)/2
    y1_warm = height/2
    y2_warm = height/1.7
    y_average_warm = (y1_warm + y2_warm)/2
    click_warm = False
    
    
    ## Define Cold Coordinate Variables
    x1_cold = x1_warm + width/4
    x2_cold = x2_warm + width/4
    x_average_cold = (x1_cold + x2_cold)/2
    y1_cold = height/2
    y2_cold = height/1.7
    y_average_cold = (y1_cold + y2_cold)/2
    click_cold = False
    
    
    ## Draw Warm Button
    warm_button = Rectangle(Point(x1_warm,y1_warm), Point(x2_warm, y2_warm))
    warm_button.setFill('red')
    warm_button.draw(win)
    warm_button_msg = Text(Point( x_average_warm, y_average_warm), "Warm")
    warm_button_msg.draw(win)
    warm_button_msg.setSize(medium_font)
    
    ## Draw Cold Button
    cold_button = Rectangle(Point(x1_cold,y1_cold), Point(x2_cold, y2_cold))
    cold_button.setFill('blue')
    cold_button.draw(win)
    cold_button_msg = Text(Point( x_average_cold, y_average_cold), "Cold")
    cold_button_msg.draw(win)
    cold_button_msg.setSize(medium_font)
    
    
    ## Ask the question
    prompt_warm_cold = Text(Point(x_midpoint, height/3 ), "What setting do you want to run the test in?")
    prompt_warm_cold.setSize(medium_font)
    prompt_warm_cold.draw(win)
    
    
    ## While next round button is not pressed keep the button there.
    while (click_warm == False and click_cold == False):
        click = win.getMouse()
        click_warm = inbox(Point(x1_warm, y1_warm), Point(x2_warm, y2_warm), click)
        click_cold = inbox(Point(x1_cold, y1_cold), Point(x2_cold, y2_cold), click)
        
    
    ##If cold button is clicked result is cold
    if click_cold == True:
        result = "Cold"
        
        
    ## Else result is warm  
    else: 
        result = "Warm"
        
       
    
    ## Erase stuff    
    cold_button.undraw()
    cold_button_msg.undraw()
    warm_button.undraw()
    warm_button_msg.undraw()
    prompt_warm_cold.undraw()
    
    ## Return Result
    return result
    
    
    
    
def file_already_exist(file_name):
    
    ## Set flag to True    
    flag_file_exists = True
    
    if is_windows == True:
        file_name = "cct_output\\" + file_name
    else:
        file_name = "cct_output/" + file_name
    
    try:
        f = open(file_name)
    
    ## If file does not exist set flag to false
    except IOError:
        flag_file_exists = False
      
    ## Return flag
    return flag_file_exists




'''

Purpose: Get the user ID

Pre-conditions: graphics window

Post-conditions: A string variable containing the user id

'''


def get_user_id(win):
        
    ## Prompt user to enter gain amount 1
    prompt_user_id = Text(Point( x_midpoint, height/3 ), "What is the user ID?")
    prompt_user_id.setSize(medium_font)
    prompt_user_id.draw(win)
    
    
    ## Get the gain amount 1
    get_user_id = Entry(Point ( x_midpoint, height/2.5), 10)
    get_user_id.setFill('white')
    get_user_id.setSize(medium_font)
    get_user_id.draw(win)
    next_button(win)
    
    ## Set user_id variable
    user_id = str(get_user_id.getText())
    get_user_id.undraw()
    prompt_user_id.undraw()
    
    ## Return the user ID
    return user_id
    
    
    
    
'''

Purpose: See if the filename contains any illegal characters.

Pre-conditions: The filename.

Post-conditions: A flag, True if filename is valid, False if filename is invalid.

'''

def valid_filename(filename):

## Set flag to true
    flag_valid = True
    
## If any of the illegal characters are present in filename set flag to False
    if (")>" in filename) or ("<" in filename) or (":" in filename) or ('"' in filename) or ('/' in filename) or ("\\" in filename) or ('|' in filename) or ('?' in filename) or ('*' in filename):
        flag_valid = False

## Return flag
    return flag_valid
    
    
    
'''

Purpose: Create a demonstration round

Pre-conditions: Window

Post-conditions: Demonstration round

'''    
    
    
def demonstration_round(win):
    
    ## Define y and x modifiers
    y_mod = 40
    x_mod = 30
    
    ## Define net outcome
    net_outcome = 0
    
        
    prompt_outcome = Text(Point(x_midpoint, height/1.1), "Round Outcome: " + str(net_outcome))
    prompt_outcome.setSize(medium_font)
    
    ## Define Round Setup
    round_number = 0
    rounds_and_blocks = [[10,250,3]]
    round_setup(win, round_number, rounds_and_blocks)
    
    ## Prompt the Practice Round
    prompt_practice = Text(Point( x_midpoint, height/4.7 ), "Practice Round")
    prompt_practice.setSize(big_font)
    prompt_practice.draw(win)
    
    ## Defining card names
    good_card = "card2_resized.png"
    bad_card = "card3_resized.png"
    neutral_card = "card4_resized.png"
    
    
    ## Default list of cards
    list_of_cards = [[7,1], [21,2], [27,3], [3, 4], [13,5], [18,6], [31,7], [24, 8]]
    
    ## Draw cards and store locations
    cards_list, undraw_cards = make_cards(win)
    
    next_button(win)
    
    ## Make list of all cards to be selected
    for i in range(0, len(list_of_cards)):
        x = cards_list[list_of_cards[i][0] - 1][0]
        y = cards_list[list_of_cards[i][0] - 1][1]
        
        amount_of_picked_cards = list_of_cards[i][1]
        
        
        card_number_display = Text(Point(x, y), str(amount_of_picked_cards))
        card_number_display.setSize(big_font)
        card_number_display.draw(win)
        
        
    next_button(win)
    
    prompt_outcome.draw(win)
    
    for j in range(0, len(list_of_cards)):
        
        x = cards_list[list_of_cards[j][0] - 1][0]
        y = cards_list[list_of_cards[j][0] - 1][1]
        
        next_button(win)
        
        if j < 5:
            draw_card = Image(Point(x, y), good_card)
            draw_card.draw(win)
            net_outcome = net_outcome + 10
            prompt_outcome.undraw()
            prompt_outcome = Text(Point(x_midpoint, height/1.1), "Round Outcome: " + str(net_outcome))
            prompt_outcome.setSize(medium_font)
            prompt_outcome.draw(win)
            
        elif j == 5:
            draw_card = Image(Point(x, y), bad_card)
            draw_card.draw(win)
            net_outcome = net_outcome - 250
            prompt_outcome.undraw()
            prompt_outcome = Text(Point(x_midpoint, height/1.1), "Round Outcome: " + str(net_outcome))
            prompt_outcome.setSize(medium_font)
            prompt_outcome.draw(win)
        
        else: 
            draw_card = Image(Point(x, y), neutral_card)
            draw_card.draw(win)
            
    ## Define round outcome display coordinates
        prompt_outcome_box = Rectangle(Point(x_midpoint - (((width/192) * 20) + ((width/192) * 2)), (height/1.1 - (width/192) * 4)),
        Point((x_midpoint + ((width/192) * 20) + ((width/192) * 2)), height/1.1 + ((width/192) * 4)))
    ## Define outcome display color
    if net_outcome > 0:
        color = "green"
    elif net_outcome == 0:
        color = "yellow"
    else:
        color = "red"
        
    prompt_outcome_box.setFill(color)
            
    ## Redefine outcome variable   
    prompt_outcome = Text(Point(x_midpoint, height/1.1), "Round Outcome: " + str(net_outcome))
    prompt_outcome.setSize(medium_font)
    
    ## Draw Box
    prompt_outcome_box.draw(win)
    
    ## Re-draw Text
    prompt_outcome.draw(win)
    
    
    next_button(win)
    reset_window(win)
    
    for i in range(32):
        undraw_cards[i].undraw()
            
        
        
        
        
    return
        
    

    
'''

Purpose: Prompt researcher when the task ends

Pre-conditions: Window

Post-conditions: Prompt

'''   
    
    
def warm_round_display(picked_cards, bad_card, cards_list, gain_amount, loss_amount, win):
    
    
    ## Defining card names
    good_card = "card2_resized.png"
    bad_card_drawing = "card3_resized.png"
    neutral_card = "card4_resized.png"
    
    ## Define net outcome
    net_outcome = 0
    
    ## Make list to store drawn cards
    list_of_drawn_cards = []
    
    ## Define round outcome display
    prompt_outcome = Text(Point(x_midpoint, height/1.1), "Round Outcome: " + str(net_outcome))
    prompt_outcome.setSize(medium_font)
    prompt_outcome.draw(win)
   
    
    
    
    for i in range(0, len(picked_cards)):
        
        
        sleep(0.5)
        x = cards_list[picked_cards[i][0] - 1][0]
        y = cards_list[picked_cards[i][0] - 1][1]
        
        if picked_cards[i][1] < bad_card or bad_card == 0:
            draw_card = Image(Point(x, y), good_card)
            draw_card.draw(win)
            net_outcome = net_outcome + gain_amount
            prompt_outcome.undraw()
            list_of_drawn_cards.append(draw_card)
            update()
            
            
        elif picked_cards[i][1] == bad_card:
            draw_card = Image(Point(x, y), bad_card_drawing)
            draw_card.draw(win)
            net_outcome = net_outcome - loss_amount
            prompt_outcome.undraw()
            list_of_drawn_cards.append(draw_card)
            update()
            
        else:
            draw_card = Image(Point(x, y), neutral_card)
            draw_card.draw(win)
            prompt_outcome.undraw()
            list_of_drawn_cards.append(draw_card)
            update()
            
            
        prompt_outcome = Text(Point(x_midpoint, height/1.1), "Round Outcome: " + str(net_outcome))
        prompt_outcome.setSize(medium_font)  
        prompt_outcome.draw(win)
        update()
        
    
    next_round = False
    
    
    ## Define round outcome display coordinates
    prompt_outcome_box = Rectangle(Point(x_midpoint - (((width/192) * 20) + ((width/192) * 2)), (height/1.1 - (width/192) * 4)),
    Point((x_midpoint + ((width/192) * 20) + ((width/192) * 2)), height/1.1 + ((width/192) * 4)))
    
    ## Define outcome display color
    if net_outcome > 0:
        color = "green"
    elif net_outcome == 0:
        color = "yellow"
    else:
        color = "red"
        
    prompt_outcome_box.setFill(color)
            
    
    ## Draw Box
    prompt_outcome_box.draw(win)
    update()
    
    ## Re-draw Text
    prompt_outcome.undraw()
    prompt_outcome.draw(win)
    update()
    
    
    while not next_round:
        click = win.getMouse()
        next_round = finish_round_button(click)
        
    prompt_outcome_box.undraw()
    prompt_outcome.undraw()
    
    return list_of_drawn_cards
    
'''

Purpose: Prompt researcher when the task ends

Pre-conditions: Window

Post-conditions: Prompt

'''      
    
def prompt_researcher(win):
    
    ## Prompt researcher to finish task
    reset_window_roots(win)
    prompt_researcher = Text(Point(x_midpoint ,height/2), "The task ended, please call the researcher before proceeding")
    prompt_researcher.setSize(medium_font)
    prompt_researcher.draw(win)
    
    next_button(win)
    

'''

Purpose: Prompt researcher and subject to begin test after practice round

Pre-conditions: Window

Post-conditions: Prompt

'''      

    
def prompt_begin_task(win):
    prompt_task = Text(Point(x_midpoint, height/2), "End of practice, the task will start next")
    prompt_task.setSize(medium_font)
    prompt_task.draw(win)
    
    ## Set variable of pressing next round buttton to False
    next_round = False
        
    ## Loop for picking cards while next round button is not pressed   
    while not next_round:
            
        ## Get mouse click
        click = win.checkMouse()
            
        ## See if next round button is clicked
        next_round = finish_round_button(click)
        
    prompt_task.undraw()
    
    
    
    
'''

Purpose: Reset Graphics Window

Pre-conditions: Graphics Window

Post-conditions: Reset Graphics Window

'''

## Reset Window Roots
def reset_window_roots(win):
    
    ## Reset the window roots style
    reset = Rectangle(Point(0,0), Point(width, height))
    reset.setFill("light gray")
    reset.draw(win)
    

'''

Purpose: Create a directory

Pre-conditions: Directory name

Post-conditions: Created directory for file storage

'''     
    
    
def create_directory(directory_name):

# Create target Directory if don't exist
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

        
def final_display(file_name, directory_name):
    
    
    ## Reset the window and write the text of the final display
    reset_window_roots(win)
    prompt_filename = Text(Point(x_midpoint, height/3), "The report for this run has been written to: " + str(file_name))
    prompt_filename.setSize(big_font)
    prompt_filename.draw(win)
    
    prompt_directory = Text(Point(x_midpoint, height/2.3), " inside a folder named: " + str(directory_name))
    prompt_directory.setSize(big_font)
    prompt_directory.draw(win)
    
    update()
    
    exit_button()
    
    update()
    
    
'''

Purpose: Create a binary list of whether an outcome was selected = 1, or not = 0

Pre-conditions: List of random outcomes selected, master list of outcomes

Post-conditions: Binary list indicating whether outcome was selected or not

'''


def outcome_list(random_list, master_list):
    
    ## Initiate Variables
    binary_list = []
    random_list.sort()
    i = 0
    j = 0
        
    ## Loop through the list of random numbers and master list
    while j < 3 or i < len(master_list):
       
        ## Set number default to 0
        number = 0
        
        ## if you have not iterated through the whole list
        if j < 3:
            
            ## if the random list number is equal to the current position
            if random_list[j] == i:
                ## Set number to 1 and iterate to next position on random list
                number = 1
                j = j + 1
                
        ## Append number to the list
        binary_list.append(number)
        
        ## Iterate over master list
        i = i + 1
        
    return binary_list

'''

Purpose: Insert binary result list of selection outcomes to master list

Pre-conditions: binary list and master list

Post-conditions: The master list with appended binary list

'''


def insert_list(binary_list, master_list):
    
    ## Iterate over master list
    for i in range (0, len(master_list)):
        
        ## Append binary to master list
        master_list[i].append(binary_list[i])
            
            
'''

Purpose: Make Exit Button

Pre-conditions: None

Post-conditions: Exit Button drawn on window

'''         
    
    
    
    
def exit_button():
    
        
    
    ## Define Coordinate Variables
    x1 = width/1.1
    x2 = width/1.03
    x_average = (x1 + x2)/2
    y1 = height/1.1
    y2 = height/1.03
    y_average = (y1 + y2)/2
    
    ## Draw Next Round Button
    exit_button = Rectangle(Point(x1,y1), Point(x2, y2))
    exit_button.draw(win)
    exit_button_msg = Text(Point( x_average, y_average ), "Exit")
    exit_button_msg.draw(win)
    exit_button_msg.setSize(medium_font)
    update()
    
    ## Set click next flag to false
    click_exit = False
    
    ## While next round button is not pressed keep the button there.
    while not click_exit:
        click = win.getMouse()
        click_exit = inbox(Point(x1, y1), Point(x2, y2), click)
        
        
    win.close()
    
    
    
'''

Purpose: Display Ruler and Get Amount of Picked Cards and Randomize Picked Cards

Pre-conditions: cards_list

Post-conditions: Returns a list with the location of cards picked and the amount of cards picked [Location, Amount of clicked cards]

'''  

def ruler():
    
    ## Display ruler
    line_locations, y1, y2, ruler_drawing = ruler_display()
    
    ## Initiate variables
    prompt_select_num = False
    next_round = False
    number = None
    click = win.getMouse()
    click_number = None
    
    # While not next round button
    while not next_round:
    
    # If no number has been clicked set circle to none
        if click_number != False:
            c = None
        next_round = finish_round_button(click)
        
        ## If next round has been clicked then ask user to select a number before proceefing
        if ((next_round == True) and (number == None)):
            select_num = Text(Point(x_midpoint, height/1.1), "Select a number of cards to before proceeding to next round")
            select_num.setSize(big_font)
            select_num.draw(win)
            prompt_select_num = True
            next_round = False
            
            ## Check to see if any number has been clicked
        for i in range (1,34):
            x1 = line_locations[i-1]
            x2 = line_locations[i]
            click_number = inbox(Point(x1, y1), Point(x2, y2), click)
            if click_number:
                number = i - 1
                c = Circle(Point((x1 + x2)/2, (y1 + y2)/2), (width/192)*2)
                c.setOutline('green')
                c.setWidth(3)
                c.draw(win)
                
        
        click = win.getMouse() 
        
        ## If a second number is clicked, delete the last one and let the new one be
        for i in range (1,34):
            x1 = line_locations[i-1]
            x2 = line_locations[i]
            click_number = inbox(Point(x1, y1), Point(x2, y2), click)
            if ((click_number) or (finish_round_button(click))):
                if c != None:
                    c.undraw()
                    next_round = finish_round_button(click)
                    
        if prompt_select_num == True:
            select_num.undraw()  
            
    ## Undraw everything and return number and next round value
    for i in range(len(ruler_drawing)):
        ruler_drawing[i].undraw()
        
        
    return [number, next_round]




'''

Purpose: Display the ruler and return button locations

Pre-conditions: None

Post-conditions: Returns a list with the location of cards picked and the amount of cards picked [Location, Amount of clicked cards]

'''  

def ruler_display():
    
    ## Make list to store borders in ruler
    line_locations = np.array([])
    all_drawings = np.array([])
    
    ## Define positions in ruler
    r_start_x = (width - (width/1.1))
    r_end_x = (width/1.1)
    r_start_y = (height/4.5 - ((width/192) * 2))
    r_end_y = (height/4.5 + ((width/192) * 2))
    r_midpoint_y = (height/4.5)
    r_width = (r_end_x - r_start_x)
    
    ## Ruler Display
    ruler_box = Rectangle(Point(r_start_x, r_start_y), Point(r_end_x, r_end_y))
    ruler_box.setFill("white")
    ruler_box.draw(win)
    
    # Create variable to store all drawings
    all_drawings = np.append(all_drawings, ruler_box)
    
    
    ## Display lines and numebers in ruler
    for i in range(1, 34):
        
        ## Create important coordinates
        old_x_line = (r_start_x + ((i - 1) * (r_width/33)))
        x_line = (r_start_x + (i * (r_width/33)))
        midpoint_x_line = ((old_x_line + x_line)/2)
        
        ## Draw line
        line = Line(Point(x_line, r_start_y), Point(x_line, r_end_y))
        line.draw(win)
        if i == 1:
            line_locations = np.append(line_locations, old_x_line)
        line_locations = np.append(line_locations, x_line)
        
        ## Draw numbers
        ruler_number = Text(Point(midpoint_x_line, r_midpoint_y), (i -1))
        ruler_number.setSize(small_font)
        ruler_number.draw(win)
        all_drawings = np.append(all_drawings, [ruler_number, line])
        
        
    return line_locations, r_start_y, r_end_y, all_drawings

    
    
'''

Purpose: Calculate important outcomes from the current round

Pre-conditions: amount of bad cards, loss amount, gain amount, and picked cards for current round

Post-conditions: Returs a list in this format [Ammunt of picked cards, When the loss card was selected, net result]

'''

def round_calculations_cold(amount_bad_cards,loss_amount, gain_amount, amount_of_cards):
    
    
    ## If there are no cards, there is nothing to calculate
    if amount_of_cards == 0:
        return [0, 0, 0]
    
    ## Initiate variables for lists and net_result
    picked_cards = list(range(1, 33))
    bad_cards_base = list(range(1,33))
    bad_cards = []
    net_result = 0
    index_first_bad_card = 100
    
    ## Make random list of picked cards
    for i in range(32 - amount_of_cards):
        
        index_to_be_removed = randrange(0, len(picked_cards))
        picked_cards.pop(index_to_be_removed)


    ## Make random list of bad cards
    for i in range(amount_bad_cards):
        index_to_be_removed = randrange(0, len(bad_cards_base))
        bad_cards.append(bad_cards_base[index_to_be_removed])
        bad_cards_base.pop(index_to_be_removed)
    
    ## Check to see which card was the first bad card to be picked
    for i in range(amount_bad_cards):
        
        if (picked_cards.count(bad_cards[i]) > 0):
            if (picked_cards.index(bad_cards[i]) < index_first_bad_card):
                index_first_bad_card = picked_cards.index(bad_cards[i])
   
    ## If no bad cards were picked then the pick of lost card is 0
    if index_first_bad_card == 100:
        pick_of_lost_card = 0
        
    ## Otherwise pick of lost card it the index of first bad card + 1
    else:
        pick_of_lost_card = index_first_bad_card + 1
    
    ## Calculate net result
    if pick_of_lost_card == 0:
        net_result = (gain_amount * amount_of_cards)
        
    else:
        net_result = ((gain_amount * (pick_of_lost_card - 1)) - loss_amount)
    
    ## Make list of desired output [Amount of picked cards, When the loss card was selected, net result]
    calculation_list = [amount_of_cards, pick_of_lost_card, net_result]
    
    
    ## Return List
    return calculation_list

   
    
'''

Purpose: Check if the operating system is Windows

Pre-conditions: None

Post-conditions: True if platform is Windows, False otherwise
'''

def is_windows():
    
    ## If the platform is windows return True
    if platform.system() == "Windows":
        return True
    
    ## Else return False
    else:
        return False

    
    
    
'''

Purpose: Calculate important outcomes from the current round

Pre-conditions: amount of bad cards, loss amount, gain amount, and picked cards for current round

Post-conditions: Returs a list in this format [Amount of picked cards, When the loss card was selected, net result]
    
'''

def round_calculations(amount_bad_cards,loss_amount, gain_amount, picked_cards):

    ## Make empty list for picked card locations
    picked_card_locations = []
    
    ## Fill the list with the locations
    for i in range(len(picked_cards)):
        picked_card_locations.append(picked_cards[i][0])
    
    ## Initiate variables for list of bad card locations and net_result
    amount_of_cards = len(picked_card_locations)
    
    if amount_of_cards == 0:
        return [0, 0, 0]
    
    ## Initiate variables for list of bad card locations and net_result
    bad_cards_base = list(range(1,33))
    bad_cards = []
    net_result = 0
    index_first_bad_card = 100
    
    

    ## Make a random list of bad cards
    for i in range(amount_bad_cards):
        index_to_be_removed = randrange(0, len(bad_cards_base))
        bad_cards.append(bad_cards_base[index_to_be_removed])
        bad_cards_base.pop(index_to_be_removed)
    
    
    ## Find out if there are any bad cards in the picked cards location and if there are which is the first
    for i in range(amount_bad_cards):
        
        if (picked_card_locations.count(bad_cards[i]) > 0):
            if (picked_card_locations.index(bad_cards[i]) < index_first_bad_card):
                index_first_bad_card = picked_card_locations.index(bad_cards[i])
   
    ## If no bad cards, pick of lost card is zero
    if index_first_bad_card == 100:
        pick_of_lost_card = 0
        
    ## Else pick of bad card is the index of first bad card + 1
    else:
        pick_of_lost_card = index_first_bad_card + 1
    
    # Based on all results calculate the net result
    if pick_of_lost_card == 0:
        net_result = (gain_amount * amount_of_cards)
        
    else:
        net_result = ((gain_amount * (pick_of_lost_card - 1)) - loss_amount)

    ## Make list of desired output [Amount of picked cards, When the loss card was selected, net result]
    calculation_list = [amount_of_cards, pick_of_lost_card, net_result]
    
    
    ## Return List
    return calculation_list
    
    
    
main()


# 
