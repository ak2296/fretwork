# Fretwork

A guitar practice app for Windows.

- **A 6-level course, 45 exercises**: first chords and strumming, finger strength and dexterity, scales, rhythm guitar (power chords, 12-bar blues, barre chords), fingerpicking, and lead techniques (hammer-ons, pull-offs, slides, bends, string skipping, arpeggios). Every exercise shows pick directions, finger or technique labels, and where your fingers go next.
- **Speed trainer**: a click that speeds up every few loops until you reach your target tempo; log clean runs and track your best tempo.
- **Your songs**: search for tabs from inside the app, then paste a tab or chord names and practise it with guide notes.
- **Progress**: minutes practised per day and best clean tempo for every drill and song.

## Download

Get **Fretwork.exe** from the [latest release](../../releases/tag/latest) and double-click it. No install or Python needed.

Windows may show a SmartScreen warning the first time because the app is not code-signed. Click **More info → Run anyway**.

## How it's built

- `fretwork.html`: the whole app interface (drills, player, songs, progress).
- `fretwork_app.py`: opens the interface in its own window (Edge WebView2) and provides tab search.
- Every push to `main` builds a new `Fretwork.exe` with GitHub Actions and publishes it as the `latest` release.
- To build locally instead, run `Build Fretwork.bat` (needs Python).
