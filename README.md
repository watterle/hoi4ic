# Hoi4 IC calculator
Savegame checker for hoi4

## Requirements
- Python 3 (os, re, numpy, matplotlib modules)
- Autosave macro: Pulover's Macro Creator

## Usage
1. Change Hoi4 saves to be non binary in settings.txt in hoi4 documents folder
2. Obtain monthly saves. Autosaves for singleplayer, autosave macro for multiplayer (it's likely a smarter way exists).
3. Move saves in /save folder
4. Rename them to "save1-hoi4", "save2.hoi4", etc., or whatever you set the IC calculator to read. rename.py does this.
5. Run IC calculator

## Things to edit
- Select the countries to analyze in the inputtag variable. Tags variable has a list of them, majors/minors variables are shortcuts to usual choices.

