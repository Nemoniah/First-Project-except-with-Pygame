def intro():
    return """You are Lavender, a member of a mercenary band known as Stormcallers. Well, not really a member just yet. Count Grimbald, the band's leader, gave you a test - to hunt down and defeat a certain spellblade. It is but a test so the task isn't particularly dangerous and you've already tracked down your target to his lair.
\nFrom what you were told, the spellblade is fond of using puzzles to protect his property. But one's puzzles can only be as challenging as one is intelligent and this particular isn't exactly the brightest light. Puzzles most likely will not prove difficult.
\nIt's quite interesting that your target is a spellblade - a mage uses spells as well as swords in combat. You yourself are a spellblade, being able to use a sword and shock magic for offense and the same sword and mental magic for defence.
\nYou have a feeling you have everything you need to complete your task unscathed as all the enemy is known for is small-time robbery and so he likely lacks the combat experience you have.
\nPress Space to continue after a message pops up
Press WASD for movement
Press Enter to confirm a choice
"""


def intro_stalling():
    return "The sunk cost fallacy doesn't let you leave the Spellblade's lair."


def first_puzzle_intro():
    return "There's a locked door with a writing on it."


def first_puzzle_text():
    return """ You take a closer look at the door and notice three small keyholes in it, a hanging from the handle key small enough to fit into the keyholes and an inscription on the wall.
\nThe inscription says:
"If you wish to enter you have to use the right keyhole!
One of them opens the door.
Another will make the earth swallow you whole.
And the last one will bring heaven's wrath upon you.
Here are tips to figure out which one does what but beware as all of them are lies!
The first one brings the wrath.
The keyholes that open the door and bring the gluttony are next to each other.
The third one will open the door."
\nYou try bashing the door open but it's too sturdy. And it's covered with spell-reflecting runes. Not that you could destroy it with shock spells to begin with. Looks like the key is your only option. So which keyhole will it be?
"""


def first_puzzle_text_small():
    return """The first one brings the wrath.
The keyholes that open the door and bring the gluttony are next to each other.
The third one will open the door.
Every statement is a lie."""


def first_puzzle_won():
    return "You open the door without dying!"


def second_puzzle_text():
    return """You passed through the door into another hall. You see a spectral image of the spellblade appear at the other end of it.
"Well aren't you a smart one! But that was just the first puzzle!"
"Yeah yeah, whatever. Bring on the second one already."
"Be careful what you wish for! Now listen up! There are three men: Kolbert, Wolfgang and Chris. One of them is a paladin,
another is a rogue and the last one's a bard! The paladin never lies, the rogue lies all the time and the bard just tells
whatever the hell he wants. Wolfgang says: "Chris is the rogue." Kolbert says: "Wolfgang is the paladin." Chris says:"I
am the bard." Who is the bard?"
So who's the bard?
A. Kolbert
B. Wolfgang
C. Chris
"""


def second_puzzle_text_small():
    return """Wolfgang: "Chris is the rogue." Kolbert: "Wolfgang is the paladin." Chris: "I am the bard."
Paladin never lies, rogue always lies, bard can do either.
Who is the bard?"""


def second_puzzle_won():
    return """The spellblade image makes an extremely displeased face and then disappears before you could tell it that this was way 
too similar to the previous puzzle. At the same time, the door at the end of this hall opens.
"""


def second_puzzle_stalling():
    return "You really hate the idea of turning back at this point."


def second_puzzle_leave():
    return "This time there are no puzzles on the door so you go through freely."


def third_puzzle_table():
    return "There is a table with several bottles and a piece of paper on it."


def third_puzzle_text():
    return """You pick up a piece of paper from the table. It says:
"Danger lies before you, while safety lies behind,
Two of us will help you, whichever you would find,
One among us seven will let you move ahead,
Another will transport the drinker back instead,
Two among our number hold only nettle wine,
Three of us are killers, waiting hidden in line.
Choose, unless you wish to stay here for evermore,
To help you in your choice, we give you these clues four:
First, however slyly the poison tries to hide
You will always find some on nettle wine's left side;
Second, different are those who stand at either end,
But if you would move onwards neither is your friend;
Third, as you see clearly, all are different size,
Neither dwarf nor giant holds death in their insides;
Fourth, the second left and the second on the right
Are twins once you taste them, though different at first sight."
You're getting a feeling you already read this in some book. Did the spellblade read it too and then recreate the puzzle? Not that it would help you, since you definitely don't have it on you. You look at the potion bottles. So which one is it?
"""


def third_puzzle_small_text():
    return """One lets go forward, one lets go back, two are wine, three are poison.
There is always poison to the left of the wine; First and last are different and neither lets go forward;
Neither the smallest nor the largest hold poison; The second on the left and the second on the right hold the same thing."""


def meeting():
    return """Good news: it looks like you're in the final room. Bad news: you're met with a horryfying screech.
"How, how did you get past the last one?!"    
"Oh yeah, thanks for reminding me, I nearly forgot again. I have seveal question. Well, two, actually. First, did you
copy the last one from somewhere? Second, what's the deal with all the logic puzzles?"
You weren't really expecting your opponent to answer and he, indeed, didn't. Instead, he screeched again, this time
something not entirely intelligible, pulled out an estoc and rushed towards you.
You quikcly assess the situation. The opponent can use both magic and melee, as you were informed back at the Stormcaller
HQ, and wields an estoc. They're usually longer than rapiers but between this one being a bit on the shorter end and
your rapier being longer than normal, your weapons looked comparable. The estoc's heavier but judging by the spellblade's
movements he wasn't nearly as agile and trained as you are. Definitely winnable.
"""


def end():
    return """The spellblade's lying on the ground, unconscious. He was a bit more dangerous than you expected and didn't leave you in
the greatest shape but you should be right as rain after you slam down a few healing potions. More importantly, you've 
finally passed the test and are ready to join the Stormcallers!
CONGRATULATIONS!
All that's left is to either haul this guy all the way back or... 
"""


