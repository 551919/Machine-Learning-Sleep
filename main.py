'''
Libraries include matplotlib and scipy,
which can be installed by right clicking the
"installrequirements.bat" (Windows)
RUN THE BATCH AS ADMIN, OTHERWISE THE DEPENDANCIES DON'T INSTALL!
'''
import numpy
import matplotlib.pyplot as plt
from scipy import stats
import turtle as t
import os
from twilio.rest import Client
import datetime
import time

# Setup Variables

userconfig=[0,0,0,"gordon","crowbar",[],[]]
colorpallete=['#e6e6e6','#000000','#99AAB5']
# Defines the light and dark mode shapes

# WAY more than two different images and shapes.These images are shapes so it counts
darkshapes=['images\dark\darklogo.gif','images\dark\darkstart.gif','images\dark\darksettings.gif','images\dark\lightmode.gif','images\dark\esetbtn.gif','images\dark\darkback.gif','images\dark\lightmodeon.gif','images\dark\darkresetdone.gif','images\dark\start.gif','images\dark\log.gif']
lightshapes=['images\light\lightlogo.gif','images\light\lightstart.gif','images\light\lightsettings.gif','images\light\darkmode.gif','images\light\esetbtn.gif','images\light\lightback.gif','images\light\darkmodeon.gif','images\light\lightresetdone.gif','images\light\start.gif','images\light\log.gif']
# Variables to make sure that the 
usedshapes=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
linecount=0
blank_point=-1
sleep_text = -1
sleep_time='0H0M'
hours = 0
minutes = 0
custom_choose=-1
number=0
plot_choice = -1
choice_var=-1
now = datetime.datetime.now()
array_points = []
prevlines=[0]


# Set up Turtle Screen and Screensize

wn = t.Screen()
wn.setup(800,800)
wn.tracer(True)
 
# Set up Twilio (text message). I know you're supposed to promote both these variables to environment ones, but this is a trial account I don't care about.
account_sid = 'AC2f73ff7b4cb7be22ca84ae9315874b99'
auth_token = '24af39152f53518383171bbbef987210'

client = Client(account_sid, auth_token)
# Open config file and set variables

configtxt = open("config\config.txt", "r+")
Lines = configtxt.readlines()

# Most optimized line reading method I could write, using an array
# Iteration
for line in Lines:
  # String manipulation
  string=line.split('=')
  string=string[1]
  string=string.strip()
  userconfig[linecount]=string
  linecount+=1

# Closes config text file
configtxt.close()

#Turn the two data arrays into actual arrays
# String manipulation
userconfig[5]=[int(n) for n in userconfig[5].split(',')]
userconfig[6]=[int(n) for n in userconfig[6].split(',')]

# Set up Turtles
element1 = t.Turtle()
element1.speed(0)
element1.penup()

element2 = t.Turtle()
element2.speed(0)
element2.penup()

element3 = t.Turtle()
element3.speed(0)
element3.penup()

# Sets dark mode if it is enabled
if(userconfig[0]=='1'):
  # At least three different colors. Luckily, light mode bumps it up to 6
  colorpallete=['#2C2F33','#FFFFFF','#99AAB5']
  # register dark mode shapes for turtle
  # Iteration
  for i in range(len(darkshapes)):
    t.register_shape(darkshapes[i])
  for i in range(len(darkshapes)):
    usedshapes[i]=darkshapes[i]
# Register Shapes in light mode
else:
  # Iteration
  for i in range(len(lightshapes)):
    t.register_shape(lightshapes[i])
  for i in range(len(lightshapes)):
    usedshapes[i]=lightshapes[i]

#Dark or light mode bg
t.screensize(bg=colorpallete[0])


# Functions (Lots and lots)

# Main Menu
def main_menu():
  #Turtle positions and button shapes
  element2.shape(usedshapes[1])
  element2.goto(0,100)

  element3.shape(usedshapes[2])
  element3.goto(0,-100)

  element1.shape(usedshapes[0])
  element1.goto(0,500)
  element1.speed(1)
  element1.goto(0,300)
  element1.speed(0)

  # Turtle listeners
  element2.onclick(lambda x,y:button_action('home_screen'))
  element3.onclick(lambda x,y:button_action('settings'))

# Write variable to file
def save_variable(usedvar,usernum):
  global prevlines
  global Lines
  global array_points
  prevlines=Lines

  #Open config.txt as in read mode
  with open('config\config.txt', 'r') as read:
    readdata=read.readlines()
  # Open config.txt as in write mode
  writeconfig = open("config\config.txt", "w")
  # Options to write to each line of the file separately
  # Conditional Statements
  if(usernum==0):
    Lines[0]='darkmode='+str(usedvar)+'\n'
  elif(usernum==1):
    Lines[1]='hours='+str(usedvar)+'\n'
  elif(usernum==2):
    Lines[2]='age='+str(usedvar)+'\n'
  elif(usernum==3):
    Lines[3]='username='+str(usedvar)+'\n'
  elif(usernum==5):
    #Cleans up array so it can be written to file
    array_points = ",".join(str(element) for element in usedvar)
    Lines[5]='datapoints_happy='+str(array_points)+'\n'
  elif(usernum==6):
    #Cleans up array so it can be written to file
    array_points = ",".join(str(element) for element in usedvar)
    Lines[6]='datapoints_hours='+str(array_points)+'\n'
  #Writes lines
  for i in range(len(Lines)):
    writeconfig.write(Lines[i])
  # Save lines
  Lines=prevlines
  writeconfig.close()

# Remind user with text message
def remind_text():
  global sleep_text
  global sleep_time
  global hours
  global minutes
  global number
  global now

  # Simple console 1/0 selection, re asks user for value if number is less than 0 or greater than 1
  while(sleep_text<0 or sleep_text>1):
    # User input
    sleep_text = int(input('Would you like a reminder sent to your phone 10 minutes before your chosen sleep time? (1 for yes 0 for no): '))
  #Conditional statement
  if(sleep_text==1):
    # Uses date/time and asks user what time they are going to sleep, and subtracts 10 from minutes
    # User input
    sleep_time = input("Great! What time are you planning on going to sleep (write like so: x.y x is hours in 12 hours time and y is minutes. DO NOT FORGET THE COLON BETWEEN THE HOURS AND MINUTES! Example: 9:05 is 9:05 PM.): ")
    # String manipulation
    hours,minutes = sleep_time.split(':')
    print('Text will be sent at: ' + hours + ':' + minutes)
    hours=int(hours)
    minutes=int(minutes)
    minutes=minutes-10
    sleep_text=-1
    number = input("Finally, enter your number in this format: +1xxxxxxxxxx with NO SEPARATORS OR ANYTHING: ")
    print("Great! The message will be sent soon! Please DO NOT CLOSE THE PROGRAM!")
    # While loop that waits until hour and minute match user's time, then sends text message
    while(int(now.hour)!= hours and int(now.minute) != minutes):
      now = datetime.datetime.now()
    message = client.messages.create(body="Get ready for bed! Remember to set your alarm!", from_='+12517275685', to=number)
  #Doesn't send text message.
  else:
    print("Alright. text will not be sent! Do not forget to set a timer for however many hours you have to sleep!")
    print('You may close the program now. When you wake up, start the program, click on the "log" button, and rate how you feel after waking up on a scale of 1-100')
    sleep_text=-1

# Home Screen
def home_screen():
  # Turtle Setup
  element1.shape(usedshapes[8])
  element1.goto(0,200)

  element2.shape(usedshapes[9])
  element2.goto(0,-200)

  element3.shape(usedshapes[5])
  element3.goto(-350,350)

  # Turtle listeners
  element1.onclick(lambda x,y:button_action('start_sleep'))
  element2.onclick(lambda x,y:button_action('log_sleep'))
  element3.onclick(lambda x,y:button_action('main_menu'))

# Settings Screen
def settings():
  #Setup Turtles
  element1.shape(usedshapes[5])
  element1.goto(-350,350)

  element2.shape(usedshapes[3])
  element2.goto(0,200)

  element3.shape(usedshapes[4])
  element3.goto(0,-200)

  # Turtle listeners
  element1.onclick(lambda x,y:button_action('main_menu'))
  element2.onclick(lambda x,y:button_action('togglemode'))
  element3.onclick(lambda x,y:button_action('reset'))

# Action for button presses
def button_action(action):
  global Lines
  global configtxt
  global blank_point
  global sleep_text
  global client
  global sleep_time
  global plot_choice
  global choice_var
  global custom_choose

  # Go to main menu
  # Conditional statements
  if(action=='main_menu'):
    main_menu()

  # Go to home screen
  elif(action=='home_screen'):
    home_screen()
  
  # Go to settings
  elif(action=='settings'):
    settings()

  # Reset the config.txt file
  elif(action=='reset'):
    element1.speed(1)
    element1.goto(-500,350)
    copy = open("config\defaultconfig.txt", "r")
    paste = open("config\config.txt", "w")
    copylines = copy.readlines()
    for line in copylines:
      paste.write(line)
    element3.shape(usedshapes[7])

  # What happens after you press the start button. Tells user how many hours they have to sleep and if the user just started, asks for age and name. Also, if you are done with your 5 data points, you can add more data points to increase accuracy
  #More conditional statements
  elif(action=='start_sleep'):
    if(int(userconfig[2])==0):
      # New profile
      # User input
      userconfig[3] = input('Enter Username: ')
      save_variable(userconfig[3],3)
      while(int(userconfig[2])>100 or int(userconfig[2])<6):
        # User input
        userconfig[2] = input('Enter your age (Used for recommended sleep hours): ')
      userconfig[2]=int(userconfig[2])
      save_variable(userconfig[2],2)

      # Sets hours of sleep based on age range
      if(int(userconfig[2])<=13):
        userconfig[1]=6
      elif(int(userconfig[2])>=14 and int(userconfig[2])<=17):
        userconfig[1]=5
      else:
        userconfig[1]=4
    # If age isn't 0, that means user already started. So, greeting + moving on.
    else:
      print('Hello, ' + str(userconfig[3]))
    for i in range(len(userconfig[5])):
      # Conditional statement
      if(userconfig[5][i]==0):
        userconfig[1]=int(userconfig[1])+1
        print('You need to sleep ' + str(userconfig[1]) + ' hours today')
        save_variable(userconfig[1],1)
        print('Set an alarm to sleep that many hours today, and once you wake up, come back and click on "log sleep" to rate your mood')
        # Reminder Text
        remind_text()
        break
    # 5 data points already recorded
    #Conditional statemens
    if(userconfig[5][4]!=0):
      while(custom_choose<0 or custom_choose>1):
        # User input
        custom_choose = input('You are done with all 5 datapoints. Enter 1 if you want to go to the final process, or 0 if you want to enter more custom data points: ')
        custom_choose = int(custom_choose)
      # Choice between adding custom data point or going to main menu to see log
      if(custom_choose==1):
        print('Alright. Click on the "Log Sleep/Show Graph" Button and follow the directions there.')
      else:
        userconfig[1]=int(input('Enter the custom hour: '))
        print('OK. You need to sleep ' + str(userconfig[1]) + ' hours today')
        save_variable(userconfig[1],1)
        remind_text()
    
# If bottom button is clicked on home screen. Log data / look at graph
# EVEN MORE CONDITIONAL STATEMENTS
  elif(action=='log_sleep'):
    # Choices, choices. 1 to view graph or 0 to log hours
    while(choice_var<0 or choice_var>1):
      choice_var = int(input('Enter 1 to view graph or 0 to log hours: '))
    # Log hours choice
    if(choice_var==0):
      for i in range(len(userconfig[5])):
        # 5 data points logging (required to show graph)
        if(userconfig[5][i]==0):
          blank_point=userconfig[5][i]
          data_point = int(input('Enter how you feel (1-100) for ' + userconfig[1] + ' hours slept: '))
          userconfig[5][i]=data_point
          print('Data logged. You may now click on the "Start/Continue" button')
          userconfig[6][i]=userconfig[1]
          save_variable(userconfig[5],5)
          save_variable(userconfig[6],6)
          choice_var=-1
          break
        # More than 5 data points logging
        if(userconfig[5][4]!=0):
          print('All necessary data points are already entered, so you are entering extra ones.')
          # User input
          data_point = input('Enter how you feel (1-100) for ' + userconfig[1] + ' hours: ')
          userconfig[6].append(int(data_point))
          userconfig[5].append(userconfig[1])
          save_variable(userconfig[5],5)
          save_variable(userconfig[6],6)
          print('Done! Now, you can either look at the plotted graph, or continue adding more custom points!')
          choice_var=-1
          break
    else:
      # Generate Graph, checking if all required data points are graphed first
      # Jeez, do these conditional statements end?
      if(userconfig[5][4]==0):
        print("Sorry! You can only view the graph after all data points are recorded!")
        choice_var=-1
      else:
        # Generates graph if all 5 points are present
        sleepmodel = numpy.poly1d(numpy.polyfit(userconfig[5], userconfig[6], 3))

        sleepline = numpy.linspace(0,12,100)
        plt.scatter(userconfig[5], userconfig[6])
        plt.plot(sleepline, sleepmodel(sleepline))
        #Choice
        while(plot_choice<0 or plot_choice>1):
          plot_choice = input('Enter 1 to show plot or 0 to enter an hour and get a correlated amount of hapiness: ')
          plot_choice = int(plot_choice)
          # Shows plot of attributes hours to happiness.
        if(plot_choice==1):
          plot_choice=-1
          choice_var=-1
          plt.show()
        else:
          plot_choice = int(input("Enter hours: "))
          plot_choice = sleepmodel(plot_choice)
          print("Happiness: " + str(plot_choice))
          plot_choice=-1
          choice_var=-1

# Toggles dark and light mode
  elif(action=='togglemode'):
    element2.shape(usedshapes[6])
    element1.speed(1)
    element1.goto(-500,350)
    # Selection
    if(userconfig[0]=='1'):
      Lines[0]='darkmode=0\n'
      file = open('config\config.txt', 'w')
      for i in range(len(Lines)):
        file.write(Lines[i])
    else:
      Lines[0]='darkmode=1\n'
      file = open('config\config.txt','w')
      for i in range(len(Lines)):
        file.write(Lines[i])


# Background Setup
button_action('main_menu')

# wn updates
wn.update()
wn.mainloop()
