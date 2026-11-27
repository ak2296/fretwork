# Fretwork

A guitar practice app for Windows.

- **A 9-level course, 131 exercises**: chords and strumming, finger dexterity, scales, two levels of rock and metal rhythm (power chords, palm muting, chugs, gallops, downpicking, tremolo picking, riffs, grooves, barre chords), two levels of lead guitar where every technique has a drill plus licks that use it together with earlier skills (hammer-ons, pull-offs, legato, slides, bends, vibrato, double stops, speed picking, string skipping, sweeping, tapping, octaves, arpeggios) ending in full solos, scales across the neck and modes, and fingerpicking.
- **Scale and mode trainer**: any key, 12 scales and modes, box positions (7 three-notes-per-string shapes or 5 pentatonic shapes), diagonal, along one string, or all positions connected; up and down, groups of 3 or 4, thirds; optional legato. The fretboard shows the whole shape with roots ringed.
- **Speed trainer**: a click that speeds up every few loops until you reach your target tempo; log clean runs and track your best tempo.
- **Your songs**: search, open a tab or chord page in the built-in tab window, press **Import**. Lyrics and page clutter are ignored; tabs and chord sheets (including slash chords) are recognised. Or paste from the clipboard.
- **Progress**: minutes practised per day, course progress per level, best clean tempo for everything you log.

## Download

Get **FretworkSetup.exe** from the [latest release](../../releases/tag/latest) and run it. It installs Fretwork for your user (no admin rights needed), adds it to the Start menu, optionally to the desktop, and to Windows' list of installed apps for uninstalling. **Fretwork.exe** in the same release is the portable version that runs without installing.

Windows may show a SmartScreen warning the first time because the app is not code-signed. Click **More info → Run anyway**.

## How it's built

- `fretwork.html`: the whole app interface (drills, player, songs, progress).
- `fretwork_app.py`: opens the interface in its own window (Edge WebView2) and provides tab search.
- Every push to `main` builds a new `Fretwork.exe` with GitHub Actions and publishes it as the `latest` release.
- To build locally instead, run `Build Fretwork.bat` (needs Python).
