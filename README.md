# pyglet-studies
Studies on pyglet usages in Python. 

Game development is probably going to change with the development of LLMs. Game engines might just lose space for packages like pyglet, which a developer might just ask for a game from a LLM. This study is mainly to prove we seem to be a long way from abolishing engines for the complexity between object handling.

- Ping-pong game
  
  A simple game of ping-pong. Handles physics, speed, keeps score, resets game when ball goes off. Very simple, doesn't handle much nor it separates between objects or between scenes.

- Ping-pong game v2
  
  A more enhanced game of ping-pong. Handles physics, speed, keeps score, resets game when ball goes off, and separates logics with classes of Scenes similar to Godot.

- Ping-pong game v3
  
  A more refined game of ping-pong. Handles physics, speed, keeps score, resets game when ball goes off, and separates logics with classes of Scenes similar to Godot. Everything here is a scene, meaning everything has it's own class with more or less independent attributes, with 4 scenarios (Main Menu, GameScene, WinScene and Options) and objects (Button, Paddle, and Ball).
