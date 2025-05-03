# Snake Game

A simple Snake game implemented in Python using Pygame, with web compatibility through Pygbag.

## Features

- Classic Snake gameplay
- Score tracking
- Pause/resume functionality
- Game over detection with restart option
- Web compatibility for playing in browsers

## How to Play

- Use arrow keys to control the snake
- Eat the red food to grow and increase your score
- Avoid hitting the snake's own body
- Press SPACE to pause/resume the game
- Press R to restart after game over
- Press ESC to quit

## Running Locally

### Prerequisites

- Python 3.6 or higher
- Pygame library

### Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python -m snakegame.game
```

## Web Version

This game can be played in a web browser thanks to Pygbag, which converts Pygame applications to WebAssembly.

### Building the Web Version

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Run the build script:

```bash
python pygbag_build.py
```

3. The web version will be available in the `build/build/web` directory

### Playing the Web Version Locally

After building, you can test the web version locally:

```bash
cd build/build/web
python -m http.server
```

Then open your browser and navigate to `http://localhost:8000`

## Deployment

See [deploy_to_github.md](deploy_to_github.md) for instructions on how to deploy the game to GitHub Pages for free hosting.

## License

This project is open source and available under the MIT License.

## Credits

Created by [Your Name]
