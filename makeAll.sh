
DRIVE="/Volumes/NO NAME"


dir=("00-bat" "00-classica" "00elettronica" "00rock")

for f in "${dir[@]}"; do
    uv run make-playlists.py --run "${DRIVE}/${f}"
done