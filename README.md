# Blitzball_Editor_workInProgress
Let's you modify the player growth curves, and player levels in save files; effectively stat editting.

Select your player and their stat from the dropdown options.
Then drag the red dots that control the curve to change how their stat grows as they level.
A slider at the top controls their level in the save file, the curves are automatically edited<img width="997" height="744" alt="bandicam 2026-06-27 20-22-06-092" src="https://github.com/user-attachments/assets/30fadf5c-c542-41df-b3f7-38c7ae8aec32" />

Later on the tool will be developed to edit LENGTH of the game (proof-tested_ and perhaps what moves each player can access.

<img width="997" height="747" alt="bandicam 2026-06-27 20-21-50-904" src="https://github.com/user-attachments/assets/a8262039-4758-4a8d-9926-cf803a1acedb" />


You will need to appropriately edit the python code to refelect the save file you want edited and your specific directory names of the .ebp file being edited.
<img width="1407" height="284" alt="bandicam 2026-06-27 20-22-47-742" src="https://github.com/user-attachments/assets/8a32b1b5-674a-4468-b768-b36c7c3d0cd1" />




Note 1: Works with Python and the modules are listed you ned to pip install are at the start of the code.
Note 2: You will need an external file loader and the Blitzball .ebp script files in the correct location.
Note 3: This is a WORK IN PROGRESS - and will only affect the in-game minigame stats, it has not yet been developed to reflect the new stat curves when you scout a player or read their stats in the Blitzball menu.
In layman's terms, currently you may scout Keepa and he shows a Catch Stat of 10, but when you play him in the actual minigame, he will show your edited growth stat e.g. 60 and play as such.
