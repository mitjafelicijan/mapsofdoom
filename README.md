# Maps of DOOM

Extracts maps from DOOM's WAD files and converts them into SVG files and then
creates a simple web interface where you can view them.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then check `config.py` to see all the configuration options.

Run extraction of maps into SVG with `python3 wad-svg.py` while you have
environemnt activated.
