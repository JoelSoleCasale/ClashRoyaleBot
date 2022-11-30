# Clash Royale Bot

## Play the game
In order to be able to play the game, you need to use an emulator. For this bot, I used BlueStacks. You can download it [here](http://www.bluestacks.com/).

## Interact with the game
With the game already installed, the first challenge is to be able to interact with it. For this, pyautogui is used. You can install it with `pip install pyautogui`.
With this library, we can take screenshots of the game and use them to interact with it. 

The library "pyautogui" can take screenshots of the game window in order to get information about the enemies positions, the current elixir, the current cards in deck, or to detect whether the game has ended or not.
The library also allows to interact with the game in order to play the cards in the board by simulating keyboard and mouse events.

## Detect the cards
We can detect the cards in the deck by comparing the screenshots with the images of the cards. All the avaliable cards the bot will be able to detect are in the folder "Cards1080p". The bot will compare the screenshots with the images of the cards and will return the name of the card that is in the deck.

## Detect the enemies
In Clash Royale, the enemies troops can have different positions in the board. In order to detect the enemies, we will use their level, wich is always in the same position. The bot will take a screenshot of the level of the enemy troops and will compare it with the images of the levels in the folder "EnemyLevels1080p". This will allow us to know the level of the enemy troops and their position in the board.
For example, this are some reference images of the levels of the enemy troops for their detection:

<p align="center">
<img src="./EnemyLevels1080p/lvl10.png" width="30">
<img src="./EnemyLevels1080p/lvl11.png" width="30">
<img src="./EnemyLevels1080p/lvl12.png" width="30">
<img src="./EnemyLevels1080p/lvl13.png" width="30">
<img src="./EnemyLevels1080p/lvl14.png" width="30">
</p>


## Detect the elixir
The elixir is always in the same position in the board. Thus, we only need to check some precise pixels in the screenshot to get the current elixir of the game.

## Play the game
The bot will play the game by simulating keyboard and mouse events. The bot will take a screenshot of the game and will detect the cards in the deck, the enemies and the elixir. With this information, the bot will decide which card to play and where to play it. The bot will play the card by simulating a mouse click in the position of the card in the deck and in the position of the enemy troop. The bot will also play the spells by simulating a mouse click in the position of the spell in the deck and in the position of the enemy troop.

All the data of the cards present in the json stats file is extracted from "https://github.com/RoyaleAPI/cr-api-data"