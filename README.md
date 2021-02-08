# Skyscrapers
Skyscrapers is a Python programme, which checks if there is a winning combination on the game board.
#Usage
The program takes a list consisting of table rows. The lines consist of pivots, which indicate how many houses should be visible from a certain position, as well as from houses of a certain height.
```python
import skyscrapers

scyscrapers.check_skyscrapers("check.txt") #returns  True
# ['***21**', '412453*', '423145*','*543215', '*35214*', '*41532*', '*2*1***'] - board
```