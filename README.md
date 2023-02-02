# Hoi4 IC calculator
Savegame checker for hoi4

## Requirements
- Python 3 (os, re, numpy, scipy, matplotlib, sys)
- Autosave macro: https://www.macrocreator.com/

## Usage
1. Change Hoi4 saves to be non binary in settings.txt in hoi4 documents folder
2. Obtain monthly saves. Autosaves for singleplayer, autosave macro for multiplayer (or smarter ways).
3. Move saves in /save folder
4. Rename them to "save1.hoi4", "save2.hoi4", etc., or whatever you set the IC calculator to read. rename.py does this.
5. Run IC calculator
6. Output plots will be in the /images folder

## Things to edit
- Select the countries to analyze in the inputtag variable. Tags variable has a list of them, majors/minors variables are shortcuts to usual choices.

## Autoclicker settings
- Modify the path to the images inside the script to fit your own pc. The files are s1.png s2.png s3.png. Right click to edit the 3 lines working on pictures.
- Press the play button on the middle-top to start the script. It will open a small window where you can check the script progress and start/stop it
- Set number of loops to infinite (0)
- Run the script from the window

## Autoclicker loop and notes
1. Find image s1.png (day 10 of month)
2. Open menu
3. Find image s2.png (menu opened)
4. Press Save
5. Find image s3.png (save menu)
6. Press Save
7. Repeat

It fucks up if you keep your cursor on the pixels it's looking for, just move it a bit and it will go on.

If you stop mid loop for micro or mistake (pressed something while it was doing it), you can just return manually to the point it was in (closed save menu, just reopen save menu manually and it will restart).

If you fuck up and don't resume the loop for a year or so, it lags the pc until you do or close the program. No idea why but it works as a remainder.


## Notes
- Only actual production is measured. IC from focuses/decision is not considered.
- Monthly IC is approximated as 30 times the instant IC at the time of the save. 
- A moving mean of 3 months is applied to the data.
- Cumulative IC is calculated with trapezoidal approximation

## Bugs
- If something is host tool annexed, it needs to be removed from the list of tags. I

- Sometimes the script can't find nations. Either play with the search function variables and hope for the best, or send me the saves. Again you can remove it from the list of tags as a stopgap.