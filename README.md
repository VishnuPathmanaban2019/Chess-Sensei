# Chess-Sensei

Project Demo: https://www.youtube.com/watch?v=ZIEnsMQApgI&feature=youtu.be

![image](https://i.imgur.com/ocxdTgN.png)

A short description of the project's name and what it does:
==============================================================================
The name of my term project is “ChessSensei”. ChessSensei is a chess software 
package with two modes: player versus player and player versus AI. And at the 
user’s request, the ChessSensei AI will give the player advice on what moves 
they should make and explain why they should make those moves. Essentially, 
the software pushes beginners to start thinking like chess players and gain 
experience.

How to run the project:
==============================================================================
Run the "main.py" file to run the project.

Which libraries you're using that need to be installed:
==============================================================================
I am using tkinter and pillow.

A list of any shortcut commands that exist:
==============================================================================
Press m or r to reset the game at any time.

Press 1 to bring up a scenario where you can check the black king.
- Move your queen to H5 to check the black king
- Press A to see advised check defense for black king

Press 2 to bring up a scenario where you can checkmate the opponent.
- Press A to see advised checkmate offense against black king
- Move your queen to H5 to checkmate the black king

Press 3 to bring up a scenario to test AI difficulty.
- Move the rightmost pawn up just to trigger the AI move
- In easy mode, the black queen should take the bishop naively
- In medium mode, the AI should move its pawn up defensively

Press 4 to bring up a scenario to test advice explanation.
- Press A to see your advised move
- Should suggest a defensive play instead of taking the bishop
- Should explain why an offensive play is bad underneath board
