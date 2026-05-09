# Claude Session Context

## Project
A pyRevit addon for Autodesk Revit that exports selected lines to the bowl backend API as **A-Lines**. A-Lines are used to generate seating bowls.

## Backend API
- Base URL: `https://bowl-backend-x0jz.onrender.com`
- Login: `POST /api/v1/auth/login` — returns a bearer token
- Create A-Line: `POST /api/v1/alines` — requires bearer token

## Auth
Credentials are stored in `RevitLineExporter.extension/config.json`:
- `email`: justin_best@gensler.com
- `password`: 1318
- The script logs in fresh on every button click to get a token.

## A-Line Payload
```json
{
    "name": "user-entered name",
    "closed": true,
    "points": [{"x": 0.0, "y": 0.0}, ...]
}
```
- Minimum 3 points required by the API
- `closed: true` when multiple lines are selected (a polygon), `false` for a single line
- Points are in **inches** — Revit internal units are decimal feet, converted by multiplying by 12
- Points are sent in **reversed** winding order so the seating bowl faces outward

## How it works
1. User selects one or more connected straight lines in Revit
2. Clicks **Send Line** in the RevitLineExporter ribbon tab
3. Prompted to enter a name for the A-Line
4. Script chains the line segments end-to-end into ordered points
5. Logs in, gets token, POSTs the A-Line to the backend

## Repo Structure
```
RevitLineExporter.extension/      ← drop this folder into pyRevit extensions
├── config.json                   ← credentials and base URL
├── lib/
│   ├── api_client.py             ← login() and post_aline()
│   ├── collector.py              ← get_selected_lines() and chain_segments()
│   └── serializer.py            ← serialize_aline() with unit conversion + winding
└── RevitLineExporter.tab/
    └── Export.panel/
        └── Send Line.pushbutton/
            └── script.py         ← entry point, wires everything together
```

## Branches
- `main` — stable, always working
- `claude/analyze-repo-contents-InnFA` — active working branch
- `scale-corrected` — snapshot before unit conversion fix
- `scale-corrected2` — snapshot after unit conversion, before winding fix

## pyRevit Notes
- pyRevit uses IronPython 2.7 — use `urllib2`, not `urllib.request`
- Only folders following pyRevit naming conventions are loaded by pyRevit
- `lib/` and `config.json` must live inside the `.extension` folder to be found at runtime
