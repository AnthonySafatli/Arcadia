# Arcadia — Browser-Based Multiplayer Game Platform

![App Screenshot](https://anthonysafatli.ca/projects/screenshots/arcadia.png)

> An online, browser-based multiplayer game platform. The multiplayer code is fully abstracted away from game logic, making it trivial to add and update multiplayer games.

🔗 **[Live Demo](https://arcadia.anthonysafatli.ca)**

🌐 **[More Information](https://anthonysafatli.ca/Project/arcadia)**

## Features

- **Abstracted Multiplayer Code** — WebSocket and multiplayer session logic is fully decoupled from game code, making new games easy to add without touching networking code.
- **Beautiful SPA Frontend** — A smooth, responsive frontend built in Vue.js 3, compiled and served directly by the Flask backend.
- **Multiple Games** — Three games available so far:
  - **Tic Tac Toe** — The classic that started it all.
  - **The Mind** — A group card game where players place cards in order without communicating. Great for telepathics.
  - **Wordle** — A competitive multiplayer twist on the classic word-guessing game — fewest guesses wins.
  - *More to come!*

### Future Games

- Connect Four
- Dots and Boxes
- Battle Ship
- Crazy 8s
- A Typing Race Game

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vue.js 3, TypeScript, CSS |
| Backend | Flask, Socket.io, Python |
| Hosting | VPS |

## Running Locally
 
```bash
# 1. Clone the repo
git clone https://github.com/AnthonySafatli/Arcadia.git
cd Arcadia
 
# 2. Install and build frontend
cd client
npm install
npm run build
 
# 3. Set up Python environment
cd ..
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
 
# 4. Start the server
python .venv/bin/python server/app.py
```

## What I learned

Arcadia was a deliberate step outside my comfort zone on both ends of the stack.
 
- **Vue.js 3 vs. React** — I typically reach for React, so building the entire frontend in Vue was a valuable exercise in learning a new component model. The Composition API felt natural coming from React hooks, but Vue's template syntax and built-in directives (like `v-model` and `v-for`) pushed me to think differently about how reactivity is expressed in markup vs. JavaScript.
- **Flask vs. ASP.NET** — My usual backend is ASP.NET, so Flask was a shift in philosophy — less convention, more explicit wiring. It gave me a better appreciation for how minimal a web server can be, and forced me to make deliberate decisions about project structure rather than relying on framework defaults.
- **Python Packaging** — Working with `venv`, `pip`, and `requirements.txt` gave me a solid grounding in Python dependency management, which I hadn't needed to think carefully about before.
- **WebSockets & Socket.io** — The most technically interesting part of the project. I learned how to manage persistent connections, broadcast events to game rooms, and — critically — how to design an abstraction layer so that game logic never needs to know it's running over a socket. The architecture decision to decouple multiplayer code from game code made adding each new game significantly faster.

## Roadmap

### Planned Games

- [ ] Connect Four
- [ ] Dots and Boxes
- [ ] Battleship
- [ ] Crazy 8s
- [ ] Typing Race

### Improvements

- [ ] Improve security by keeping player identity server-side rather than on the client
- [ ] Replace in-memory game state with a proper database
- [ ] Support players joining or leaving mid-game

## Licence

[GNU GPL v3](LICENCE)
