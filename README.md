# VRChess
Smart chess board, enables 2-way communication with chess player via physical chess board.
Chess board, just like pieces are 3d printed, player action detection mechanism is made on a budget using cheep and easily bought components. 

# Board's board 
Smart chess board runs on single Arduino-Uno board, witch is connected to PC via USB port.

### Note 
Arduino side-library is light enough that (with slight pin reconfiguration) any board could run script therefore cheapening cost of duplicating VRChess board even more.
Note thet library is written for Arduino Leonardo board in mind.

# Installation 
1. Clone VRChess repository 

## I Python Api
On your personal computer 
1. Install python 3.8 
2. Open Python-Api folder
3. (optional) Activate python venv
4. Install dependencies using pip tool 
    list of dependencies can be found in requirements.txt file

## II Arduino Api
Connect board of your choice to your PC via USB port.
1. Install Platform IO extension in your visual studio code editor
2. Connect all hardware components to your board, for this step use provided guide
3. Open Arduino-Api via Platform IO "open project" option, 
    located on the main screen, prompt will pop-up with board selection, chose yours.
    
    Note that library is written for Arduino Leonardo board in mind. 
4. Compile and Write program to your board

## III Determine connection port
While your board is connected to PC via USB port
    
For windows:  go to settings/devices and search for your board, determine on witch "COM" port it's connected. In `Python-Api/ main` file , update port variable with previously determined one.
 
# User action detection
Board detects user input by measuring piece placement using specially designed magnetic buttons, thus require usage of special pieces, to witch files can be found [here](not yet linked). All information collected by board is passed to PC and interpreted by provided python Api, than  detected "button" presses are analyzed and interpreted as user piece movement. In a way chessboard acts as glorified keyboard, that can only be touched with special magnetic pieces.  

# Backlight
Boards main feature is RGB backlight under each square, enabling output communication. This backlight is controlled with python script, thus acts as very low quality 64x64 led display, with around 23ms refresh rate.

# List of parts:
1. 96, 2mm high, 7mm diameter magnets, 32 for pieces, 64 for squares 
2. 64, 7mm outer-diameter, 2mm inner-diameter 1mm high spacers 
2. 64 straightening diodes rated for 5v current
3. around 2 meters of 1.6mm diameter soldering wire, for connectors
4. 64 led long addressable led strip (each individual led will be cut from strip and re-soldered with connections because money limitations, and we're masochists), can come in pieces
5. soldering wire for led-2-led connections and board-2-arduino connectors
6. Filament and 3-d printer, maybe some slicing skills, all models are designed to be easily 3-d printed
