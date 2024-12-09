# Hoi4 IC calculator
Savegame checker for hoi4

## Hoi 4 autosaves
1. Open C:\Users\you\Documents\Paradox Interactive\Hearts of Iron IV\settingsx.txt
2. Set debug_saves=120 (maximum number of autosaves)
3. Set save_as_binary=no (saves without compression)
4. In game set autosaves to be monthly

## Usage
1. Download latest compiled release 
2. Copy the autosaves to /_internal/save (Autosaves must be named autosave_N.hoi4 and nothing else can be in the folder)
3. Run iccalculator.exe
4. Ic graphs are created in /_internal/output

## Notes
- Only actual production is measured. IC from focuses/decision is not considered.
- Monthly IC is approximated as 30 times the instant IC at the time of the save. 