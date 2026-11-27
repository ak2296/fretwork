"""Fretwork - guitar practice app for Windows.

Opens Fretwork in its own window (uses the Edge WebView2 engine built into
Windows 10/11) and adds tab search, which a browser page cannot do.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

import webview

APP_NAME = "Fretwork"


def resource(name):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


def data_dir():
    root = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    path = os.path.join(root, APP_NAME)
    os.makedirs(path, exist_ok=True)
    return path


def _get_json(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0) Fretwork/1.0",
                 "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))


class Api:
    """Functions the page can call as window.pywebview.api.<name>()."""

    def search(self, query):
        q = urllib.parse.quote((query or "").strip())
        if not q:
            return {"results": [], "error": "Type a song or artist first."}
        urls = [
            f"https://www.songsterr.com/api/songs?size=25&pattern={q}",
            f"https://www.songsterr.com/a/ra/songs.json?pattern={q}",
        ]
        last_err = ""
        for url in urls:
            try:
                data = _get_json(url)
            except Exception as e:  # try the next address
                last_err = str(e)
                continue
            if isinstance(data, dict):
                data = data.get("songs") or data.get("records") or []
            out = []
            for s in data[:25]:
                sid = s.get("songId") or s.get("id")
                title = s.get("title")
                artist = s.get("artist") or ""
                if isinstance(artist, dict):
                    artist = artist.get("name", "")
                if not (sid and title):
                    continue
                slug = re.sub(r"[^a-z0-9]+", "-", f"{artist} {title}".lower()).strip("-")
                out.append({
                    "artist": artist,
                    "title": title,
                    "url": f"https://www.songsterr.com/a/wsa/{slug}-tab-s{sid}",
                })
            return {"results": out, "error": "" if out else "No tabs found. Try the artist name or another spelling."}
        return {"results": [], "error": "Search failed (" + last_err + "). Use the links below instead."}


def main():
    webview.settings["OPEN_EXTERNAL_LINKS_IN_BROWSER"] = True
    webview.create_window(
        "Fretwork",
        url=resource("fretwork.html"),
        js_api=Api(),
        width=1280,
        height=860,
        min_size=(420, 600),
    )
    # private_mode=False + storage_path keeps your songs and progress between runs
    webview.start(private_mode=False, storage_path=data_dir())


if __name__ == "__main__":
    main()
