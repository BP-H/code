# Guess That Persona Mini-game

**Experimental:** This folder contains a small browser game that is not yet wired
into the main GPT Frenzy application. It serves as a standalone demo and may
change or break without notice.

This browser game challenges you to match short replies to the correct GPT Frenzy persona.

## Setup

No build step is required. Clone the repository and open `index.html` in a modern browser.
To serve the game over HTTP (useful for mobile devices), run:

```bash
python3 -m http.server 8000
```

Then visit <http://localhost:8000> in your browser.

## Gameplay

Each round displays a prompt along with several possible replies. Choose the response you think belongs to the highlighted persona. Five rounds total—try to get a perfect score!

## Hosting

All files run client-side, so you can host this folder on any static web server
(e.g., GitHub Pages or Netlify). Copy the contents of `mini-game/` to your host
and point users to `index.html`.

The code is MIT licensed under the project’s [LICENSE_CODE](../LICENSE_CODE).
Personas and their descriptions remain the property of their creators.
