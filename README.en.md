# Brag v1.1
This project is a multiplayer online game based on Python, which provides two modes: creating a room and joining a room. Players can play a game of "Bluff" in this game.

# Project Structure

    chui_niu/
    |--README.md
    |--main.py
    |--PlayerUtils.py
    |--RoomUtils.py

# Dependencies

This project uses the threading and socket libraries to implement network communication and multi-thread processing.

# Usage

1. Run main.py to start the game server.

2. Connect to the server and choose to join an existing room or create a new room.

    - If you choose to create a room, you will be prompted to enter the maximum number of players and wait for other players to join.

    - If you choose to join a room, you will be prompted to enter the room number, and once connected, you will enter the room.

3. Once the room is full, the room owner can choose to start the game, and other players can choose to leave the room before the game starts.

4. During the game, players take turns to bluff until only one player remains.

# Notes

1. Before running main.py, make sure that you have installed Python environment.

2. Before running main.py, modify the server address and port number to make it accessible from the Internet.

3. This is version 1.1 of the project, some features are not fully developed, and there are still some bugs.
