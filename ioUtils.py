# ioUtils.py
# Input / Output utilities used with Tom the AI.
# Programmed by Murray Jones (murray.jones12@bigpond.com)
# Completed 21/06/2021

# Impport command handellers.
import os
import sys
import subprocess

import time


if "\\" in os.getcwd(): # Recognises windows machines by use of \\ in their file paths.
    
    platform = "windows"
    
    dir_ = os.getcwd() + "\\" # Find directory from which program is running.
    
    sys.path.insert(0, dir_ + "windows_modules") # Add windows module directory to locations that python will search when trying to import modules.

    
else:
    
    platform = "linux" # File path uses / instead of \\. Therefor we are running on a unix or bsd system
    
    dir_ = os.getcwd() + "/" # Find directory from which program is running.
    
    sys.path.insert(0, dir_ + "linux_modules") # Add linux module directory to locations that python will search when trying to import modules.


sys.path.insert(0, dir_ + "generic_modules") # Modules used by both windows and linux systems.



loadIteration = 0.0 # Number of load iterations so far

def iterateLoadProgress(window): # Creates a smooth loading bar without knowing how many items need to be loaded.
    global loadIteration
    import math

    loadIteration += 1 # Increment counter.

    # Smooth the counter to advance on the previous, buut never reach the max.
    progress = 1 - (1 / (math.sqrt(float(loadIteration))))
    progress *= 100

    window["-LOAD-PROGRESS-"].update(progress) # Update PySimpleGUI window.


def removeMarkup(string, A, B): # Removes  all charactes  from a string that fall after the A deliminator and before the B deliminator.
    # e.g. can remove HTML tage between the < and > deliminators.
    
    tag = False
    quote = False
    out = ""

    for char in string: # Iterate through each character in the string.
        if char == A and not quote:
            tag = True
        elif char == B and not quote:
            tag = False
        elif (char == '"' or char == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + char

    return out # String with markup removed.



def incur(package, window=None): # Importa a module, or installs the module if the import failed.
    # Can also output progress to a GUI windoww, if desired.
    
    try: # try to import the module.
        
        print("Importing " + package + " ... ", end="")

        if window: # Update loading window status.
            window["-LOAD-TEXT-"].update("Importing " + package + "... ")
        
        exec("import " + package)
        
        
    except ImportError as error: # Package has not been installed.
        
        print("ImportError: " + str(error))
        print("\nInstalling " + package + " ... ", end="")

        if window: # Update loading window status.
            window["-LOAD-TEXT-"].update("Installing " + package + " ...")

        subprocess.check_call(["pip", "install", "--timeout", "36000", package]) # Use a pip command to install the package.

        exec("import " + package)
        

    except ModuleNotFoundError as error: # A dependancy od thhe moule is missing, this is harder to fix.
        print("ModuleNotFoundError: " + str(error))
        print("\nFixing dependancies for " + package + " ... ", end="")

        if window:
            window["-LOAD-TEXT-"].update("Installing " + package + " ...")

        subprocess.check_call(["pip", "install", "--timeout", "36000", package]) # Attempt to install mmissimg module.

        exec("import " + package)
        

    finally:

        if window != None: # Output information to window, if a window was given
            iterateLoadProgress(window)
            window.refresh()
        
        print("Done.")
        
        return eval(package) # Return the local package as a variable.


def tinput(prompt="", timeout=20, timeoutmsg=None): # Same as the input() function, but has a timeout.
    signal = incur(signal)
    
    def timeout_error(*_): # Raises a timeout error.
        raise TimeoutError

    # Set a timeout alarm for the desired length of time.
    signal.signal(signal.SIGALRM, timeout_error)
    signal.alarm(int(timeout))
    
    try: # Try to recieve ann input.
        answer = input(prompt)
        signal.alarm(0) # Ready the alarm for next time.
        return answer
    
    except TimeoutError: # Input timed out.
        if timeoutmsg:
            print(timeoutmsg)
            
        signal.signal(signal.SIGALRM, signal.SIG_IGN) # Deactivate the alarm
        return None
    

def tprint(String): # Prints chatacters one at a time.
    # Good for command line programs, but causes lag in a GUI.
    
    try:
        for letter in String: # Iterate through characters in string.
            print(letter, end="")
            time.sleep(0.02)
        time.sleep(.7)
        print("")
        
    except:
        pass

def lprint(list_): # Prints a list line by line.
    print("[")
    for i in list: # Iterate through items in list.
        print(i, ",")
    print("]")


def contains(string, list_, wholeWord=False): # Returns true if the words iin the list are anywhere in the string.
    from nltk.tokenize import word_tokenize
    
    if wholeWord: # List item must be a entire word in string.
        for i in list_: 
            for s in word_tokenize(string): 
                if i == s:
                    return True
                
    else: # List item can be can be part of a word in string
        for i in list_:
            try:
                if i.lower().strip() in string.lower().strip():
                    return True
            except AttributeError:
                pass
            
    return False # List item was not found in sting.


def mbox(message, type_="info", title=None, heading=None, image=None, icon="graphics/squareFace.gif",
         text_color=None, heading_color=None, background_color=None, buttons=["Ok"]):
    # Displays a custom alert dialog box..

    import PySimpleGUI as sg

    # Defind dialog box parameters.
    type_ = type_.lower() # Type of alert
    defaultBackground = "grey30" # Background color of dialog box.
    windowImage = None # IImage  to display as window icon

    if type_ == "error": # Fatal error message.
        windowImage = dir_ + "graphics/dialog-error.png"
        background_color = "maroon"
        heading_color = "red"
        text_color = "grey90"
        
    elif type_ == "warning": # Warning. Use for non-fatal errors.
        windowImage = dir_ + "graphics/dialog-warning.png"
        background_color = defaultBackground
        heading_color = "orange red"
        text_color = "grey90"
        
    elif type_ == "info": # General information, not an error.
        windowImage = dir_ + "graphics/dialog-information.png"
        background_color = defaultBackground
        heading_color = "light blue"
        text_color = "grey90"
        
    elif type_ == "secure": # Displays a dialog box with a 'high security' symbol.
        windowImage = dir_ + "graphics/security-high.png"
        background_color = defaultBackground
        heading_color = "white"
        text_color = "grey90"
        
    elif type_ == "insecure": # Security risk alert.
        windowImage = dir_ + "graphics/security-low.png"
        background_color = defaultBackground
        heading_color = "white"
        text_color = "grey90"
        
    elif type_ == "star": # Displays a dialog box with a 'star' symbol.
        windowImage = dir_ + "graphics/starred.png"
        background_color = defaultBackground
        heading_color = "yellow"
        text_color = "grey90"
        
    elif type_ == "password": # Displays a dialog box with a 'password' symbol.
        windowImage = dir_ + "graphics/dialog-password.png"
        background_color = defaultBackground
        heading_color = "cyan"
        text_color = "grey90"
        
    elif "trophy" in type_: # Displays a dialog box with a tropy in it. Tropy can be bronze, silver, or gold.
        type_ = type_.replace("_", "-")
        windowImage = dir_ + "graphics/trophy-" + type_ + ".png"
        background_color = defaultBackground
        heading_color = "gold"
        text_color = "grey90"
        
    else: # Sesort ti generic info icon if no type_ was given.
        print("Warning: Bad message type.")
        windowImage = dir_ + "graphics/dialog-information.png"

    # Assign customisable window parameters.

    if image != None:
        windowImage = image

    if icon == None:
        icon = windowImage

    if title == None:
        type_ = type_.replace("-", " ").replace("_", " ")
        title = type_.capitalize()

    if heading == None:
        heading = title


    buttonList = [] # Holds PySimpleGUI button elements as var's.

    for buttonName in buttons: # Assemble a series of buttons, based on a list of their names.
        button = sg.Button(buttonName, button_color=("white", "grey20"), key=buttonName, font=("Any", 10))
        buttonList.append(button)

    # Define the loayout for th message box.
    mboxLayout = [[sg.Image(windowImage, background_color=background_color),
                   sg.Text(heading, font=("Helevicta", 16), text_color=heading_color, background_color=background_color)],
                  [sg.Text("\n"*2, font=("Helevicta", 11), text_color=text_color, background_color=background_color, key="-TEXT-")],
                  buttonList]

    # Define thhe message box its-self.
    mbox = sg.Window(title, mboxLayout,
            grab_anywhere=False,
            keep_on_top=True,
            background_color=background_color,
            alpha_channel=.96,
            finalize=True,
            icon=icon,
            margins=(16, 16))

    mbox['-TEXT-'].Update(message) # Print the message to the bmessage box's test element.
    mbox['-TEXT-'].Widget.configure(wraplength=400) # Wrap thhe text in the text element.
    mbox['-TEXT-'].set_size(size = (None, max(1, int(len(str(message))/(400/11))))) # Resize the text element to fit the wrapped text.
    
    while True: # Event loop for the message box.
        event, values = mbox.read() # Read events form the window.

        if event == sg.WIN_CLOSED: # The user just 'X'ed out of the message box :(
            mbox.close()
            time.sleep(0.1)
            mbox.refresh()
            return "Closed"
        
        elif event in buttons: # The user clicked one of the buttons :)
            mbox.close() # Close the message box.
            time.sleep(0.1)
            mbox.refresh() # Make sure it's actually closed.
            time.sleep(0.1)
            
            return event # Return the name of the button pressed.


