from flask import Flask, render_template, request
import random
from functions import *
from pybaseball import playerid_lookup
from pybaseball import batting_stats
from pybaseball import bwar_bat
import pandas as pd
from pybaseball.lahman import *
download_lahman()

app = Flask(__name__)

global bardletest, turn, guess_key, wins, losses, streak, bardle_tracker
turn = 0
wins = 0
losses = 0
streak = 0
guess_key = []
bardle_tracker = ""

df1 = pd.DataFrame(batting())
dfwar = pd.DataFrame(bwar_bat())
df1.sort_values(by="stint", ascending=False)
dfwar.sort_values(by="stint_ID", ascending=False)

def picknewbardle():
  global turn
  turn = 0
  playerlist = ['Marcus Semien', 'Bryan De La Cruz', 'Daz Cameron', 'Franhcy Cordero', 'Nick Gordon', 'Aristides Aquino', 'Adam Frazier', 'Mike Trout', 'Oneil Cruz', 'Whit Merrifield', 'Vladimir Guerrero', 'Freddie Freeman', 'Tommy Edman', 'Mitch Haniger', 'Bo Bichette', 'J. P. Crawford', 'Ozzie Albies', 'Paul Goldschmidt', 'DJ LeMahieu', 'Jose Altuve', 'Isiah Kiner-Falefa', 'Cedric Mullins', 'Jonathan Schoop', 'Matt Olson', 'Robbie Grossman', 'Kyle Seager', 'David Fletcher', 'Salvador Perez', 'Rafael Devers', 'Austin Riley', 'José Abreu', 'Carlos Santana', 'Juan Soto', 'Nolan Arenado', 'Dansby Swanson', 'Ty France', 'Bryan Reynolds', 'Trea Turner', 'Jorge Polanco', 'Jake Cronenworth', 'Nathaniel Lowe', 'Carlos Correa', 'Manny Machado', 'Adam Frazier', 'Shohei Ohtani', 'Myles Straw', 'Pete Alonso', 'Cesar Hernandez', 'Jose Ramirez', 'J. D. Martinez', 'Aaron Judge', 'Jonathan India', 'Jeimer Candelario', 'Mark Canha', 'Matt Chapman', 'Adolis García', 'Dylan Carlson', 'Joey Gallo', 'Trey Mancini', 'Yoan Moncada', 'Brandon Lowe', 'Justin Turner', 'Yuli Gurriel', 'Randy Arozarena', 'Alex Verdugo', 'Xander Bogaerts', 'Jorge Soler', 'Eduardo Escobar', 'Bryce Harper', 'Yordan Alvarez', 'Ryan McMahon', 'Teoscar Hernandez', 'Trevor Story', 'Max Muncy', 'Austin Meadows', 'Amed Rosario', 'Kris Bryant', 'Ryan Mountcastle', 'Nick Castellanos', 'Enrique Hernandez', 'Jared Walsh', 'Nelson Cruz', 'Charlie Blackmon', 'Chris Taylor', 'Giancarlo Stanton', 'Andrew McCutchen', 'Eugenio Suarez', 'Hunter Renfroe', 'Luis Urias', 'Josh Bell', 'Jean Segura', 'Kyle Tucker', 'Eric Hosmer', 'Nicky Lopez', 'Tommy Pham', 'Josh Harrison', 'Willy Adames', 'Adam Duvall', 'Kevin Newman', 'Tim Anderson', 'Mookie Betts', 'Josh Rojas', 'Brandon Crawford', 'Javier Baez', 'C. J. Cron', 'Fernando Tatis', 'Randal Grichuk', 'Pavin Smith', 'Josh Donaldson', 'Hunter Dozier', 'Elvis Andrus', 'Yandy Díaz', 'Lourdes Gurriel', 'Miguel Rojas', 'Andrew Benintendi', 'David Peralta', "Tyler O'Neill", 'J. T. Realmuto', 'Ian Happ', 'Raimel Tapia', 'Joey Votto', 'Miguel Sano', 'Mike Yastrzemski', 'Kyle Farmer', 'Austin Hays', 'Michael Taylor', 'Trent Grisham', 'Miguel Cabrera', 'Starling Marte', 'Francisco Lindor', 'Gleyber Torres', 'Avisail Garcia', 'Jed Lowrie', 'Jose Iglesias', 'Nick Solak', 'Jesus Aguilar', 'Michael Brantley', 'Jazz Chisholm', 'Jonathan Villar', 'Will Smith', 'Joey Wendle', 'Wil Myers', 'Christian Vazquez', 'Garrett Hampson', 'Dominic Smith', 'Odubel Herrera', 'Kolten Wong', 'Max Kepler', 'Jesse Winker', 'Willson Contreras', 'Joc Pederson', 'Luis Arraez', 'Michael Conforto', 'Christian Yelich', 'Leury Garcia', 'Nick Ahmed', 'Yadier Molina', 'Kyle Schwarber', 'Andrew Vaughn', 'Franmil Reyes', 'Manuel Margot', 'Akil Baddoo', 'Brett Gardner', 'Tyler Naquin', 'Buster Posey', 'Bobby Dalbec', 'Andrelton Simmons', 'Willi Castro', 'Sean Murphy', 'Omar Narvaez', 'Christian Walker', 'Rhys Hoskins', 'Gio Urshela', 'Gary Sanchez', 'Anthony Santander', 'Wilmer Flores', 'Jackie Bradley', 'Adam Frazier', 'Jacob Stallings', 'Martin Maldonado', 'Jeff McNeil', 'AJ Pollock', 'Cesar Hernandez', 'Trea Turner', 'Pedro Severino', 'Alec Bohm', 'Brendan Rodgers', 'Willy Adames', 'James McCann', 'Jurickson Profar', 'Eddie Rosario', 'Corey Seager', 'Didi Gregorius', 'Maikel Franco', 'Paul DeJong', 'Tyler Stephenson', 'Harrison Bader', 'Alex Bregman', 'Eduardo Escobar', 'Ben Gamel', 'Tony Kemp', "Ke'Bryan Hayes", 'Freddy Galvis', 'Kevin Kiermaier', 'Tucker Barnhart', 'Joey Gallo', 'Brandon Nimmo', 'Ben Gamel', 'Gregory Polanco', 'Brandon Belt', 'Eric Haase', 'Gavin Lux', 'LaMonte Wade', 'Ramon Laureano', 'Luis Torrens', 'Jarred Kelenic', 'Brad Miller', 'Dylan Moore', 'Anthony Rizzo', 'Yan Gomes', 'Yasmani Grandal', 'Abraham Toro', 'Patrick Wisdom', 'Mike Zunino', 'Kris Bryant', 'Ketel Marte', 'Phil Gosselin', 'Elias Diaz', 'Myles Straw', 'Victor Robles', 'Corey Dickerson', 'Justin Upton', 'Javier Baez', 'Rougned Odor', 'Harold Ramirez', 'Ronald Acuna', 'Jorge Soler', 'Josh Harrison', 'Carson Kelly', 'Colin Moran', 'Victor Caratini', 'Jason Heyward', 'Asdrubal Cabrera', 'Cody Bellinger', 'Alcides Escobar', 'Bradley Zimmer', 'Guillermo Heredia', 'Kevin Pillar', 'Starlin Castro', 'Nelson Cruz', 'Donovan Solano', 'Ronald Torreyes', 'George Springer', 'Harold Castro', 'Adam Duvall', 'Yonathan Daza', 'Rafael Ortega', 'David Bote', 'Juan Lagares', 'Edmundo Sosa', 'Niko Goodrum', 'Tom Murphy', 'Rowdy Tellez']
  bardleselect = ''
  if turn == 0:
    bardleselect = (playerlist.pop(random.randint(0,len(playerlist)-1)).lower())
  else:
    pass
  return bardleselect

bardletest = picknewbardle()

wsgi_app = app.wsgi_app

@app.route("/",methods=['GET', 'POST'])
def welcome():
    global bardletest, turn, guess_key, wins, losses, streak, bardle_tracker
    check = ""
    bardle_stats1 = findplayerstats4(playersplit_id3(bardletest),2021)
    if request.method == 'POST':
        form = request.form
        user_guess = form["guess"]
        if user_guess.lower() == "restart":
            turn = 0
            guess_key = []
            picknewbardle()
            bardletest = picknewbardle()
            check = "You have restarted the game. To begin, guess a player."
            losses = losses
            wins = wins
            streak = streak
            bardle_tracker = bardle_tracker
            return render_template("bardle3.xhtml", check = check, guesses = "", message1 = "", message3 = "", message5 = "", message7 = "", message9 = "", message11 = "", message13 = "", message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
        elif playersplit_id3(user_guess) == "Invalid Player" or playersplit_id3(user_guess) == "Too Old":
            check = 'Sorry, the player you guessed could not be located. Guess again (press back if you need to see your previous guesses).'
            return render_template("bardle3.xhtml", check = check)
        else:
            turn += 1
            guess_key.append(user_guess)
            if turn == 1:
                player_stats1 = findplayerstats4(playersplit_id3(user_guess),2021)
                comp = bardle_comp3(player_stats1, bardle_stats1)
                guesses_left = str(7 - turn)
                message1 = player_stats1[0] + " " + comp[0] + player_stats1[1] + " " + comp[1] + player_stats1[2] + " " + comp[2] + player_stats1[3] + " " + comp[3] + player_stats1[4] + " " + comp[4] + player_stats1[5] + " " + comp[5]
                if bardletest.lower() == user_guess.lower():
                    check = "Congrats! You got the Bardle! To play again guess 'Restart'." 
                    wins += 1
                    streak += 1
                    bardle_tracker += ' ✅ '
                    return render_template("bardle3.xhtml", check = check, guesses = "", message1 = message1, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
                else:
                    check = "Guess again."
                    return render_template("bardle3.xhtml", check = check, guesses = "Guesses left: " + guesses_left, message1 = message1, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
            elif turn == 2:
                player_stats1 = findplayerstats4(playersplit_id3(guess_key[0]),2021)
                comp1 = bardle_comp3(player_stats1, bardle_stats1)
                player_stats2 = findplayerstats4(playersplit_id3(user_guess),2021)
                comp = bardle_comp3(player_stats2, bardle_stats1)
                guesses_left = str(7 - turn)
                message1 = player_stats1[0] + " " + comp1[0] + player_stats1[1] + " " + comp1[1] + player_stats1[2] + " " + comp1[2] + player_stats1[3] + " " + comp1[3] + player_stats1[4] + " " + comp1[4] + player_stats1[5] + " " + comp1[5]
                message3 = player_stats2[0] + " " + comp[0] + player_stats2[1] + " " + comp[1] + player_stats2[2] + " " + comp[2] + player_stats2[3] + " " + comp[3] + player_stats2[4] + " " + comp[4] + player_stats2[5] + " " + comp[5]
                if bardletest.lower() == user_guess.lower():
                    check = "Congrats! You got the Bardle! To play again guess 'Restart'."
                    wins += 1
                    streak += 1
                    bardle_tracker += ' ✅ '
                    return render_template("bardle3.xhtml", check = check, guesses = "", message1 = message1, message3 = message3, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
                else:
                    check = "Try again."
                    return render_template("bardle3.xhtml", check = check, guesses = "Guesses left: " + guesses_left, message1 = message1, message3 = message3, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
            elif turn == 3:
                player_stats1 = findplayerstats4(playersplit_id3(guess_key[0]),2021)
                comp1 = bardle_comp3(player_stats1, bardle_stats1)
                player_stats2 = findplayerstats4(playersplit_id3(guess_key[1]),2021)
                comp2 = bardle_comp3(player_stats2, bardle_stats1)
                player_stats3 = findplayerstats4(playersplit_id3(user_guess),2021)
                comp = bardle_comp3(player_stats3, bardle_stats1)
                guesses_left = str(7 - turn)
                message1 = player_stats1[0] + " " + comp1[0] + player_stats1[1] + " " + comp1[1] + player_stats1[2] + " " + comp1[2] + player_stats1[3] + " " + comp1[3] + player_stats1[4] + " " + comp1[4] + player_stats1[5] + " " + comp1[5]
                message3 = player_stats2[0] + " " + comp2[0] + player_stats2[1] + " " + comp2[1] + player_stats2[2] + " " + comp2[2] + player_stats2[3] + " " + comp2[3] + player_stats2[4] + " " + comp2[4] + player_stats2[5] + " " + comp2[5]
                message5 = player_stats3[0] + " " + comp[0] + player_stats3[1] + " " + comp[1] + player_stats3[2] + " " + comp[2] + player_stats3[3] + " " + comp[3] + player_stats3[4] + " " + comp[4] + player_stats3[5] + " " + comp[5]
                if bardletest.lower() == user_guess.lower():
                    check = "Congrats! You got the Bardle! To play again guess 'Restart'."
                    wins += 1
                    streak += 1
                    bardle_tracker += ' ✅ '
                    return render_template("bardle3.xhtml", check = check, guesses = "", message1 = message1, message3 = message3, message5 = message5, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
                else:
                    check = "Guess again."
                    return render_template("bardle3.xhtml", check = check, guesses = "Guesses left: " + guesses_left, message1 = message1, message3 = message3, message5 = message5, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
            elif turn == 4:
                player_stats1 = findplayerstats4(playersplit_id3(guess_key[0]),2021)
                comp1 = bardle_comp3(player_stats1, bardle_stats1)
                player_stats2 = findplayerstats4(playersplit_id3(guess_key[1]),2021)
                comp2 = bardle_comp3(player_stats2, bardle_stats1)
                player_stats3 = findplayerstats4(playersplit_id3(guess_key[2]),2021)
                comp3 = bardle_comp3(player_stats3, bardle_stats1)
                player_stats4 = findplayerstats4(playersplit_id3(user_guess),2021)
                comp = bardle_comp3(player_stats4, bardle_stats1)
                guesses_left = str(7 - turn)
                message1 = player_stats1[0] + " " + comp1[0] + player_stats1[1] + " " + comp1[1] + player_stats1[2] + " " + comp1[2] + player_stats1[3] + " " + comp1[3] + player_stats1[4] + " " + comp1[4] + player_stats1[5] + " " + comp1[5]
                message3 = player_stats2[0] + " " + comp2[0] + player_stats2[1] + " " + comp2[1] + player_stats2[2] + " " + comp2[2] + player_stats2[3] + " " + comp2[3] + player_stats2[4] + " " + comp2[4] + player_stats2[5] + " " + comp2[5]
                message5 = player_stats3[0] + " " + comp3[0] + player_stats3[1] + " " + comp3[1] + player_stats3[2] + " " + comp3[2] + player_stats3[3] + " " + comp3[3] + player_stats3[4] + " " + comp3[4] + player_stats3[5] + " " + comp3[5]
                message7 = player_stats4[0] + " " + comp[0] + player_stats4[1] + " " + comp[1] + player_stats4[2] + " " + comp[2] + player_stats4[3] + " " + comp[3] + player_stats4[4] + " " + comp[4] + player_stats4[5] + " " + comp[5]
                if bardletest.lower() == user_guess.lower():
                    check = "Congrats! You got the Bardle! To play again guess 'Restart'."
                    wins += 1
                    streak += 1
                    bardle_tracker += ' ✅ '
                    return render_template("bardle3.xhtml", check = check, guesses = "", message1 = message1, message3 = message3, message5 = message5, message7 = message7, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
                else:
                    check = "Guess again."
                    return render_template("bardle3.xhtml", check = check, guesses = "Guesses left: " + guesses_left, message1 = message1, message3 = message3, message5 = message5, message7 = message7, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
            elif turn == 5:
                player_stats1 = findplayerstats4(playersplit_id3(guess_key[0]),2021)
                comp1 = bardle_comp3(player_stats1, bardle_stats1)
                player_stats2 = findplayerstats4(playersplit_id3(guess_key[1]),2021)
                comp2 = bardle_comp3(player_stats2, bardle_stats1)
                player_stats3 = findplayerstats4(playersplit_id3(guess_key[2]),2021)
                comp3 = bardle_comp3(player_stats3, bardle_stats1)
                player_stats4 = findplayerstats4(playersplit_id3(guess_key[3]),2021)
                comp4 = bardle_comp3(player_stats4, bardle_stats1)
                player_stats5 = findplayerstats4(playersplit_id3(user_guess),2021)
                comp = bardle_comp3(player_stats5, bardle_stats1)
                guesses_left = str(7 - turn)
                message1 = player_stats1[0] + " " + comp1[0] + player_stats1[1] + " " + comp1[1] + player_stats1[2] + " " + comp1[2] + player_stats1[3] + " " + comp1[3] + player_stats1[4] + " " + comp1[4] + player_stats1[5] + " " + comp1[5]
                message3 = player_stats2[0] + " " + comp2[0] + player_stats2[1] + " " + comp2[1] + player_stats2[2] + " " + comp2[2] + player_stats2[3] + " " + comp2[3] + player_stats2[4] + " " + comp2[4] + player_stats2[5] + " " + comp2[5]
                message5 = player_stats3[0] + " " + comp3[0] + player_stats3[1] + " " + comp3[1] + player_stats3[2] + " " + comp3[2] + player_stats3[3] + " " + comp3[3] + player_stats3[4] + " " + comp3[4] + player_stats3[5] + " " + comp3[5]
                message7 = player_stats4[0] + " " + comp4[0] + player_stats4[1] + " " + comp4[1] + player_stats4[2] + " " + comp4[2] + player_stats4[3] + " " + comp4[3] + player_stats4[4] + " " + comp4[4] + player_stats4[5] + " " + comp4[5]
                message9 = player_stats5[0] + " " + comp[0] + player_stats5[1] + " " + comp[1] + player_stats5[2] + " " + comp[2] + player_stats5[3] + " " + comp[3] + player_stats5[4] + " " + comp[4] + player_stats5[5] + " " + comp[5]
                if bardletest.lower() == user_guess.lower():
                    check = "Congrats! You got the Bardle! To play again guess 'Restart'."
                    wins += 1
                    streak += 1
                    bardle_tracker += ' ✅ '
                    return render_template("bardle3.xhtml", check = check, guesses = "", message1 = message1, message3 = message3, message5 = message5, message7 = message7, message9 = message9, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
                else:
                    check = "Guess again."
                    return render_template("bardle3.xhtml", check = check, guesses = "Guesses left: " + guesses_left, message1 = message1, message3 = message3, message5 = message5, message7 = message7, message9 = message9, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
            elif turn == 6:
                player_stats1 = findplayerstats4(playersplit_id3(guess_key[0]),2021)
                comp1 = bardle_comp3(player_stats1, bardle_stats1)
                player_stats2 = findplayerstats4(playersplit_id3(guess_key[1]),2021)
                comp2 = bardle_comp3(player_stats2, bardle_stats1)
                player_stats3 = findplayerstats4(playersplit_id3(guess_key[2]),2021)
                comp3 = bardle_comp3(player_stats3, bardle_stats1)
                player_stats4 = findplayerstats4(playersplit_id3(guess_key[3]),2021)
                comp4 = bardle_comp3(player_stats4, bardle_stats1)
                player_stats5 = findplayerstats4(playersplit_id3(guess_key[4]),2021)
                comp5 = bardle_comp3(player_stats5, bardle_stats1)
                player_stats6 = findplayerstats4(playersplit_id3(user_guess),2021)
                comp = bardle_comp3(player_stats6, bardle_stats1)
                guesses_left = str(7 - turn)
                message1 = player_stats1[0] + " " + comp1[0] + player_stats1[1] + " " + comp1[1] + player_stats1[2] + " " + comp1[2] + player_stats1[3] + " " + comp1[3] + player_stats1[4] + " " + comp1[4] + player_stats1[5] + " " + comp1[5]
                message3 = player_stats2[0] + " " + comp2[0] + player_stats2[1] + " " + comp2[1] + player_stats2[2] + " " + comp2[2] + player_stats2[3] + " " + comp2[3] + player_stats2[4] + " " + comp2[4] + player_stats2[5] + " " + comp2[5]
                message5 = player_stats3[0] + " " + comp3[0] + player_stats3[1] + " " + comp3[1] + player_stats3[2] + " " + comp3[2] + player_stats3[3] + " " + comp3[3] + player_stats3[4] + " " + comp3[4] + player_stats3[5] + " " + comp3[5]
                message7 = player_stats4[0] + " " + comp4[0] + player_stats4[1] + " " + comp4[1] + player_stats4[2] + " " + comp4[2] + player_stats4[3] + " " + comp4[3] + player_stats4[4] + " " + comp4[4] + player_stats4[5] + " " + comp4[5]
                message9 = player_stats5[0] + " " + comp5[0] + player_stats5[1] + " " + comp5[1] + player_stats5[2] + " " + comp5[2] + player_stats5[3] + " " + comp5[3] + player_stats5[4] + " " + comp5[4] + player_stats5[5] + " " + comp5[5]
                message11 = player_stats6[0] + " " + comp[0] + player_stats6[1] + " " + comp[1] + player_stats6[2] + " " + comp[2] + player_stats6[3] + " " + comp[3] + player_stats6[4] + " " + comp[4] + player_stats6[5] + " " + comp[5]
                if bardletest.lower() == user_guess.lower():
                    check = "Congrats! You got the Bardle! To play again guess 'Restart'."
                    wins += 1
                    streak += 1
                    bardle_tracker += ' ✅ '
                    return render_template("bardle3.xhtml", check = check, guesses = "", message1 = message1, message3 = message3, message5 = message5, message7 = message7, message9 = message9, message11 = message11, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
                else:
                    check = "Guess again."
                    return render_template("bardle3.xhtml", check = check, guesses = "Guesses left: " + guesses_left, message1 = message1, message3 = message3, message5 = message5, message7 = message7, message9 = message9, message11 = message11, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
            elif turn == 7:
                player_stats1 = findplayerstats4(playersplit_id3(guess_key[0]),2021)
                comp1 = bardle_comp3(player_stats1, bardle_stats1)
                player_stats2 = findplayerstats4(playersplit_id3(guess_key[1]),2021)
                comp2 = bardle_comp3(player_stats2, bardle_stats1)
                player_stats3 = findplayerstats4(playersplit_id3(guess_key[2]),2021)
                comp3 = bardle_comp3(player_stats3, bardle_stats1)
                player_stats4 = findplayerstats4(playersplit_id3(guess_key[3]),2021)
                comp4 = bardle_comp3(player_stats4, bardle_stats1)
                player_stats5 = findplayerstats4(playersplit_id3(guess_key[4]),2021)
                comp5 = bardle_comp3(player_stats5, bardle_stats1)
                player_stats6 = findplayerstats4(playersplit_id3(guess_key[5]),2021)
                comp6 = bardle_comp3(player_stats6, bardle_stats1)
                player_stats7 = findplayerstats4(playersplit_id3(user_guess),2021)
                comp = bardle_comp3(player_stats7, bardle_stats1)
                guesses_left = str(7 - turn)
                message1 = player_stats1[0] + " " + comp1[0] + player_stats1[1] + " " + comp1[1] + player_stats1[2] + " " + comp1[2] + player_stats1[3] + " " + comp1[3] + player_stats1[4] + " " + comp1[4] + player_stats1[5] + " " + comp1[5]
                message3 = player_stats2[0] + " " + comp2[0] + player_stats2[1] + " " + comp2[1] + player_stats2[2] + " " + comp2[2] + player_stats2[3] + " " + comp2[3] + player_stats2[4] + " " + comp2[4] + player_stats2[5] + " " + comp2[5]
                message5 = player_stats3[0] + " " + comp3[0] + player_stats3[1] + " " + comp3[1] + player_stats3[2] + " " + comp3[2] + player_stats3[3] + " " + comp3[3] + player_stats3[4] + " " + comp3[4] + player_stats3[5] + " " + comp3[5]
                message7 = player_stats4[0] + " " + comp4[0] + player_stats4[1] + " " + comp4[1] + player_stats4[2] + " " + comp4[2] + player_stats4[3] + " " + comp4[3] + player_stats4[4] + " " + comp4[4] + player_stats4[5] + " " + comp4[5]
                message9 = player_stats5[0] + " " + comp5[0] + player_stats5[1] + " " + comp5[1] + player_stats5[2] + " " + comp5[2] + player_stats5[3] + " " + comp5[3] + player_stats5[4] + " " + comp5[4] + player_stats5[5] + " " + comp5[5]
                message11 = player_stats6[0] + " " + comp6[0] + player_stats6[1] + " " + comp6[1] + player_stats6[2] + " " + comp6[2] + player_stats6[3] + " " + comp6[3] + player_stats6[4] + " " + comp6[4] + player_stats6[5] + " " + comp6[5]
                message13 = player_stats7[0] + " " + comp[0] + player_stats7[1] + " " + comp[1] + player_stats7[2] + " " + comp[2] + player_stats7[3] + " " + comp[3] + player_stats7[4] + " " + comp[4] + player_stats7[5] + " " + comp[5]
                if bardletest.lower() == user_guess.lower():
                    check = "Congrats! You got the Bardle! To play again guess 'Restart'."
                    wins += 1
                    streak += 1
                    bardle_tracker += ' ✅ '
                    return render_template("bardle3.xhtml", check = check, guesses = "", message1 = message1, message3 = message3, message5 = message5, message7 = message7, message9 = message9, message11 = message11, message13 = message13, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
                else:
                    check = "You ran out of guesses. To play again guess 'Restart'. The Bardle was: " + bardletest
                    showstats = bardle_stats1[0] + " " + bardle_stats1[1] + " " + bardle_stats1[2] + " " + bardle_stats1[3] + " " + bardle_stats1[4] + " " + bardle_stats1[5]
                    losses += 1
                    bardle_tracker += ' ❌ '
                    return render_template("bardle3.xhtml", check = check, guesses = showstats, message1 = message1, message3 = message3, message5 = message5, message7 = message7, message9 = message9, message11 = message11, message13 = message13, message17 = bardle_tracker, message19 = str(wins), message20 = str(losses), message21 = str(streak))
    else:
        pass
    return render_template("bardle3.xhtml", check = check)




def findplayerstats4(playerID, year):
    updatedPID =''
    attributeslist=[]
    try:
        if playerID == 'ramirjo02':
            updatedPID += 'ramirjo01'
            df_new1 = df1[df1['playerID'] == updatedPID][df1['yearID'] == year]
            df_warlookup = dfwar[dfwar['player_ID'] == updatedPID][dfwar['year_ID'] == year]
            attributeslist.append(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][4])
            attributeslist.append(df_new1.sort_values(by="stint", ascending=False).iloc[0][4])
            attributeslist.append(div_lookup2(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][4]))
            attributeslist.append(str(df_new1.sort_values(by="stint", ascending=False).iloc[0][11]))
            attributeslist.append(str(round(df_new1.sort_values(by="stint", ascending=False).iloc[0][8]/df_new1.sort_values(by="stint", ascending=False).iloc[0][6]*1000)))
            attributeslist.append(str(round(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][16],1)))
        elif  playerID == 'guerrvl01':
            updatedPID += 'guerrvl02'
            df_new1 = df1[df1['playerID'] == updatedPID][df1['yearID'] == year]
            df_warlookup = dfwar[dfwar['player_ID'] == updatedPID][dfwar['year_ID'] == year]
            attributeslist.append(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][4])
            attributeslist.append(df_new1.sort_values(by="stint", ascending=False).iloc[0][4])
            attributeslist.append(div_lookup2(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][4]))
            attributeslist.append(str(df_new1.sort_values(by="stint", ascending=False).iloc[0][11]))
            attributeslist.append(str(round(df_new1.sort_values(by="stint", ascending=False).iloc[0][8]/df_new1.sort_values(by="stint", ascending=False).iloc[0][6]*1000)))
            attributeslist.append(str(round(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][16],1)))
        elif  playerID == 'tatisfe01':
            updatedPID += 'tatisfe02'
            df_new1 = df1[df1['playerID'] == updatedPID][df1['yearID'] == year]
            df_warlookup = dfwar[dfwar['player_ID'] == updatedPID][dfwar['year_ID'] == year]
            attributeslist.append(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][4])
            attributeslist.append(df_new1.sort_values(by="stint", ascending=False).iloc[0][4])
            attributeslist.append(div_lookup2(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][4]))
            attributeslist.append(str(df_new1.sort_values(by="stint", ascending=False).iloc[0][11]))
            attributeslist.append(str(round(df_new1.sort_values(by="stint", ascending=False).iloc[0][8]/df_new1.sort_values(by="stint", ascending=False).iloc[0][6]*1000)))
            attributeslist.append(str(round(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][16],1)))
        elif playerID == 'taylomi01':
            updatedPID += 'taylomi02'
            df_new1 = df1[df1['playerID'] == updatedPID][df1['yearID'] == year]
            df_warlookup = dfwar[dfwar['player_ID'] == updatedPID][dfwar['year_ID'] == year]
            attributeslist.append(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][4])
            attributeslist.append(df_new1.sort_values(by="stint", ascending=False).iloc[0][4])
            attributeslist.append(div_lookup2(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][4]))
            attributeslist.append(str(df_new1.sort_values(by="stint", ascending=False).iloc[0][11]))
            attributeslist.append(str(round(df_new1.sort_values(by="stint", ascending=False).iloc[0][8]/df_new1.sort_values(by="stint", ascending=False).iloc[0][6]*1000)))
            attributeslist.append(str(round(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][16],1)))
        else:
            df_new1 = df1[df1['playerID'] == playerID][df1['yearID'] == year]
            df_warlookup = dfwar[dfwar['player_ID'] == playerID][dfwar['year_ID'] == year]
            attributeslist.append(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][4])
            attributeslist.append(df_new1.sort_values(by="stint", ascending=False).iloc[0][4])
            attributeslist.append(div_lookup2(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][4]))
            attributeslist.append(str(df_new1.sort_values(by="stint", ascending=False).iloc[0][11]))
            attributeslist.append(str(round(df_new1.sort_values(by="stint", ascending=False).iloc[0][8]/df_new1.sort_values(by="stint", ascending=False).iloc[0][6]*1000)))
            attributeslist.append(str(round(df_warlookup.sort_values(by="stint_ID", ascending=False).iloc[0][16],1)))
        return attributeslist
    except IndexError:
        return "Invalid Player"


def playersplit_id3(playername):
    try:
        if playername.lower() == "tommy la stella":
            return 'lasteto01'
        elif playername.lower() == "bryan de la cruz":
            return 'delacbr01' 
        elif len(playername.split())>2:
            return playerid_lookup(playername.lower().split()[2],playername.lower().split()[0]+" "+playername.lower().split()[1]).iloc[0][4]       
        elif playerid_lookup(playername.lower().split()[1],playername.lower().split()[0]).sort_values(by="mlb_played_last", ascending=False).iloc[0][7] != 2021:
            return 'Too Old'
        elif len(playerid_lookup(playername.lower().split()[1],playername.lower().split()[0]))>1:
            return playerid_lookup(playername.lower().split()[1],playername.lower().split()[0]).iloc[len(playerid_lookup(playername.lower().split()[1],playername.lower().split()[0]))-1][4]
        else:
            return playerid_lookup(playername.lower().split()[1],playername.lower().split()[0]).iloc[0][4]
    except IndexError:
        return "Invalid Player"

def bardle_comp3(player_stats, bardle_stats):
    comp = []
    for x in range(0,3):
        if player_stats[x] == bardle_stats[x]:
            comp.append(' ✅ ')
        else:
            comp.append(' ❌ ')
    for x in range(3,6):
            if float(player_stats[x])*10 == float(bardle_stats[x])*10:
                comp.append(' ✅ ')
            elif float(player_stats[x])*10 > float(bardle_stats[x])*10:
                comp.append(' ⬇️ ')
            else:
                comp.append(' ⬆️ ')
    return comp


def league_lookup(team):
    AL = ['BOS','NYY','BAL','TOR','TBR','CHW','CLE','KCR','MIN','DET','LAA','OAK','SEA','HOU','TEX']
    NL = ['CHC','STL','PIT','CIN','MIL','WSN','NYM','ATL','MIA','PHI','LAD','SFG','COL','ARI','SDP']
    if team in AL:
        return 'AL'
    elif team in NL:
        return 'NL'
    else:
        return '--'

def div_lookup2(team):
    EAST = ['WSN','NYM','ATL','MIA','PHI','BOS','NYY','BAL','TOR','TBR']
    CEN = ['CHC','STL','PIT','CIN','MIL','CHW','CLE','KCR','MIN','DET']
    WEST = ['LAD','SFG','COL','ARI','SDP','LAA','OAK','SEA','HOU','TEX']
    
    if team in EAST:
        return 'EST'
    elif team in CEN:
        return 'CEN'
    elif team in WEST:
        return 'WST'
    else:
        return '- - -'



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
