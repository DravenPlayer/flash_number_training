from pandas import DataFrame,read_csv
from matplotlib import pyplot as plt
from os import system, listdir
import random
from colored import fore,style,fg
from itertools import combinations_with_replacement
import time
from datetime import datetime
#Colors:
#Red = fg("#ff1f7c")
Red = fg("#f44545")
Green = fg("#31c6c1")
Orange = fg('#ff875f')
Blue = fg('#0fd3ff')
Yellow = fg('#ffdd4a')

def import_log(Reset=False):
    if Reset==True:
        return read_csv('reset.csv',index_col=0,usecols=['Combination','Success Rate', 'Number of samples', 'Average reaction speed'])
    list_dir = listdir()
    if 'data.csv' in list_dir:
        return read_csv('data.csv', index_col=0,
                           usecols=['Combination', 'Success Rate', 'Number of samples', 'Average reaction speed'])
    else:
        return read_csv('reset.csv', index_col=0,
                           usecols=['Combination', 'Success Rate', 'Number of samples', 'Average reaction speed'])
class Menu:
    def __init__(self,game):
        self.options = {'Play':self.play, 'Settings':self.settings, 'Stats':self.stats, 'Exit':self.exit,'Train':self.train}
        self.game = game
    def get_option(self):
        menu = ['Play','Train','Settings', 'Stats','Exit']
        while True:
            system('cls')
            option = input(f'''{Orange}Choose one of the options{style.RESET} : 
{Green}[1] Play
[2] Train
[3] Settings
[4] Stats
[5] Exit{style.RESET}
''').lower().title()
            if option in self.options or option.isdigit():
                if option.isdigit():
                    if int(option) in range(1, 6):
                        return self.options[menu[int(option)-1]]()
                    else :
                        continue
                return self.options[option]()
    def train(self):

        if self.game.data.shape[0]<8:
            print(f'{fore.RED_1}You can\' train at the moment Please play so we can collect more data{style.RESET}')
        else:
            hard_combinations = [i for i in self.game.data.index if
                                 self.game.data.loc[i]['Average reaction speed'] > self.game.average_speed]
            while True:
                try:
                    train_duration = int(input('How many times do you want to train ?'))
                    break
                except:
                    pass
            for i in range(train_duration):
                choice = random.choice(hard_combinations)
                l = [int(i) for i in choice.split('-')]
                number_1, number_2 = l[0], l[1]
                while True:

                    start = input(f'{Blue}Press enter to start{style.RESET}')
                    self.game.print(number_1, number_2)
                    start_time = time.time()
                    answer = input('What is the sum of the numbers ?')
                    end_time = time.time()
                    time_sub = (len(str(answer)) + 1) * self.game.average_character_speed
                    if answer.isdigit() == True:
                        if int(answer) == number_1 + number_2:
                            print(f'{Green}Correct !{style.RESET}')
                            time_taken = round(end_time - start_time - time_sub / 1000, 4) * 1000
                            if time_taken <= self.game.data.loc[choice]['Average reaction speed']:
                                print(
                                    f"{Green}Good Job ! You were faster by {round(self.game.data.loc[choice]['Average reaction speed'] - time_taken, 1)} ms !{style.RESET}")
                                time.sleep(1)
                                system('cls')
                                break
                            else:
                                print(
                                    f"{Orange}But sadly you were slower than usual by {round(self.game.data.loc[choice]['Average reaction speed'] - time_taken, 1)}ms .{style.RESET}")
                                time.sleep(1)
                                system('cls')
                                continue
                        else:
                            print(f'{Red}Wrong..!{style.RESET}')
                            time.sleep(0.8)
                            system('cls')
                            continue
                    else:
                        print(f'{Red}Please Input A number{style.RESET}')
                        time.sleep(0.8)
                        system('cls')
                        continue
    def settings(self):
        system('cls')
        print(f'''Settings:
Length of digits : {self.game.len}
Number of Sums : {self.game.number_num}
        ''')
        while True:
            settings_to_change = input(f'''{Orange}What do you want to change ?{style.RESET}
{Green}[0] Length
[1] Number
[2] Reset Stats{style.RESET}
''')
            if settings_to_change.lower().title() in ['Length', 'Number', 'Reset Stats'] :
                break
            elif settings_to_change.isdigit():
                if int(settings_to_change)in range(3):
                    break
        while True:
            if settings_to_change == 'Length' or str(settings_to_change)=='0' :
                string = f'{Blue}Give the updated Length Value: {style.RESET}\n'
                answer = input(string)
                if answer.isdigit()==True:
                    if int(answer)>0:
                        self.game.len = int(answer)
                        break
                    else:
                        print(f'{Red}Give a positive integer !{style.RESET}')
                        string  = '\n'
                else:
                    print('Give a Number ! ')
                    string = '\n'
            elif settings_to_change == 'Number' or str(settings_to_change)=='1':
                string = f'{Blue}Give the updated Number of sum Value: {style.RESET}\n'
                answer = input(string)
                if answer.isdigit() == True:
                    if int(answer) > 2:
                        self.game.number_num = int(answer)
                        break
                    else:
                        print(f'{Yellow}The number must be bigger than 2 !{style.RESET})')
                        string = '\n'
                else:
                    print(f'{Red}Give a Number ! {style.RESET}')
                    string = '\n'
            elif settings_to_change.lower().title()=='Reset Stats' or str(settings_to_change)=='2':
                self.game.data = import_log(True)
                break
    def play(self):
        self.game.play()
    def exit(self):
        self.game.data.to_csv('data.csv', index=True)
        exit()
    def stats(self):
        system('cls')
        self.game.games_played = sum(self.game.data['Number of samples'])
        print(f'''{Green}Games played : {self.game.games_played}
Win-rate : {self.game.winrate}%
Hardest Sum : {self.game.hardest}
Average Answer Speed : {self.game.average_speed} ms{style.RESET}''')
        if self.game.data.shape[0]>0:
            dt_string = 'Output '+str(datetime.now().strftime("%d-%m-%Y %H-%M-%S"))+'.png'
            plt.style.use('Solarize_Light2')
            fig = plt.figure()
            subplot1 = fig.add_subplot(1, 2, 1)
            colors = []
            for i in self.game.data['Average reaction speed'].sort_values():
                if i>2*self.game.average_speed:
                    colors.append('#d22643')
                elif i<self.game.average_speed/2:
                    colors.append('#26d26e')
                else:
                    colors.append('#ff7f0e')
            self.game.data['Average reaction speed'].sort_values().plot(kind='bar', figsize=(10, self.game.data.shape[0]), color=colors,
                                                          title='Average reaction speed per combination')
            plt.xlabel('Combinations', fontsize=6 ,weight='bold')
            plt.xticks(weight='bold',fontsize=6)
            plt.yticks(weight='bold', fontsize=9)
            plt.ylabel('Average Reaction Speed', fontsize=8, weight='bold')
            plt.autoscale(enable=True, axis='x', tight=True)
            plt.axhline(y=self.game.average_speed, color='#ff7f0e', linewidth=0.5, linestyle='--')
            subplot2 = fig.add_subplot(1, 2, 2)
            colors = []
            for i in self.game.data['Success Rate'].sort_values():
                if i > 90:
                    colors.append('#26d26e')
                elif i < 50:
                    colors.append('#d22643')
                else:
                    colors.append('#268bd2')
            self.game.data['Success Rate'].sort_values().plot(kind='bar', figsize=(10, 6),color=colors, title='Success Rate Per combination')
            plt.xlabel('Combinations', fontsize=6, weight='bold')
            plt.xticks(weight='bold', fontsize=6)
            plt.yticks(weight='bold', fontsize=9)
            plt.ylabel('Average Reaction Speed', fontsize=8, weight='bold')
            #matplotlib.image.mpimg.imread({dt_string})
            plt.axhline(y=self.game.winrate, color='#ff1f0e', linewidth=0.5, linestyle='--')
            plt.autoscale(enable=True, axis='x', tight=True)

            plt.show()
            while True:
                answer = input(f'{Blue}Do you want to save the Figure ?{style.RESET}')
                if answer[0].lower() in ['y', 'n']:
                    break
            if answer[0].lower()=='y':
                fig.savefig(dt_string, dpi=300, orientation='landscape')



        else:
            print(f'{fore.RED_1}No Data To Show{style.RESET}')
def number_range(len_num):
    result = []
    i=1
    while len(str(i))<=len_num:
        if len(str(i))==len_num:
            result.append(i)
        i+=1
    return result
class Game:
    def  __init__(self,number_ofnum=10, len_of_num=1,data=None):
        self.len= len_of_num
        self.number_num = number_ofnum
        self.number = None
        self.games_played = 0

        self.hardest = None

        self.random_list = number_range(self.len)
        self.data = data
        self.winrate = sum(self.data['Success Rate'])/self.data.shape[0] if self.data.shape[0]!=0 else 100
        self.average_speed = sum(self.data['Average reaction speed']) / self.data.shape[0] if self.data.shape[0]!=0 else 0
        #print(self.data.loc[:,'Average reaction speed'])
        self.average_character_speed = 134.84
    def random_number(self):
        return random.choice(self.random_list)
    def print(self,number_1=None, number_2=None):
        if number_1 ==None:
            number_1 = self.random_number()
        if number_2 == None:
            number_2 = self.random_number()
        print(f"{Red}{number_1}{style.RESET} {Blue}+{style.RESET} {Red}{number_2}{style.RESET}")
    def play(self):
        self.random_list = number_range(self.len)
        system('cls')
        for i in range(self.number_num):
            while True:
                number_1,number_2 = self.random_number(),self.random_number()
                #self.number = 4


                start = input(f'{Blue}"Press enter to start"{style.RESET}')
                self.print(number_1, number_2)

                start_time = time.time()
                answer = input('=')
                end_time = time.time()
                combinations = combinations_with_replacement(self.random_list, 2)
                if (number_1, number_2) in combinations:
                    combination = str(number_1) + '-' + str(number_2)
                else:
                    combination = str(number_2) + '-' + str(number_1)
                if answer.isdigit() == True:
                    time_sub = (len(str(answer)) + 1) * self.average_character_speed
                    if int(answer) == number_1 + number_2:
                        print(f'{Green}Correct !{style.RESET}')
                        # len of word andpressing enter
                        time.sleep(0.5)
                        # [sucess_rate, number of samples, average reaction speed]
                        if combination in self.data.index:


                            self.data.loc[combination]['Average reaction speed'] = round(((self.data.loc[combination]['Average reaction speed'] * self.data.loc[combination]['Number of samples'])+ round(end_time - start_time - time_sub / 1000, 4) * 1000)/(self.data.loc[combination]['Number of samples']+1),1)
                            self.data.loc[combination]['Success Rate'] = (self.data.loc[combination]['Number of samples'] * (self.data.loc[combination]['Success Rate']/100) +1)/(self.data.loc[combination]['Number of samples']+1)*100
                            self.data.loc[combination]['Number of samples'] += 1
                        else:
                            self.data.loc[combination] = [100, 1,round(end_time - start_time - time_sub / 1000, 4) * 1000]
                    else:
                        print(f'{Red}Wrong..!{style.RESET}')
                        if combination in self.data.index:
                            #self.data.loc[combination]['Average reaction speed'] = round(((self.data.loc[combination]['Average reaction speed'] * self.data.loc[combination]['Number of samples'])+ round(end_time - start_time - time_sub / 1000, 4) * 1000)/(self.data.loc[combination]['Number of samples']+1),1)
                            self.data.loc[combination]['Success Rate'] = (self.data.loc[combination]['Number of samples'] * (self.data.loc[combination]['Success Rate']/100))/(self.data.loc[combination]['Number of samples']+1)*100
                            self.data.loc[combination]['Number of samples'] += 1

                        else:
                            self.data.loc[combination] = [0, 1,round(end_time - start_time - time_sub / 1000, 4) * 1000 +500]
                    time.sleep(0.8)
                    system('cls')
                    break
                    '''
                        if self.hardest == None or self.hardest > (end_time-start_time):
                            self.hardest = end_time-start_time
                        self.average_speed = (self.average_speed*self.games_played + (end_time-start_time))/(self.games_played+1)
                    
                    else:
                        print(f'{fore.RED_1}Wrong{style.RESET}')
                        self.winrate = (self.winrate*self.games_played)/(self.games_played+1)
                '''
                else:
                    print(f'{Yellow}Please Input A number{style.RESET}')
                    time.sleep(1)
                    system('cls')
                    continue
        self.winrate = sum(self.data['Success Rate']) / self.data.shape[0] if self.data.shape[0] != 0 else 100
        self.average_speed = sum(self.data['Average reaction speed']) / self.data.shape[0] if self.data.shape[
                                                                                                  0] != 0 else 0

def main():
    data = import_log()

    menu = Menu(Game(data=data))



    while True:
        system('cls')
        menu.get_option()
        data.to_csv('data.csv', index=True)

main()
