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


def _clean_title(t):
    t = re.sub(r"\s*@\s*Ultimate-Guitar\.com.*$", "", t or "", flags=re.I)
    t = re.sub(r"\s*\((ver|version)\s*\d+\)", "", t, flags=re.I)
    t = re.sub(r"\s+(official\s+)?(chords|tabs?|bass tabs?|ukulele chords|guitar pro|power tab)\b", "", t, flags=re.I)
    m = re.match(r"\s*(.+?)\s+by\s+(.+?)\s*$", t)
    return f"{m.group(2)} - {m.group(1)}" if m else t.strip()


def _read_clipboard():
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes
        u, k = ctypes.windll.user32, ctypes.windll.kernel32
        u.GetClipboardData.restype = wintypes.HANDLE
        k.GlobalLock.argtypes = [wintypes.HGLOBAL]
        k.GlobalLock.restype = ctypes.c_void_p
        k.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
        if not u.OpenClipboard(None):
            return ""
        try:
            h = u.GetClipboardData(13)  # CF_UNICODETEXT
            if not h:
                return ""
            ptr = k.GlobalLock(h)
            try:
                return ctypes.wstring_at(ptr) if ptr else ""
            finally:
                k.GlobalUnlock(h)
        finally:
            u.CloseClipboard()
    try:
        import tkinter
        r = tkinter.Tk()
        r.withdraw()
        try:
            return r.clipboard_get()
        finally:
            r.destroy()
    except Exception:
        return ""


class Api:
    """Functions the page can call as window.pywebview.api.<name>().

    Names starting with _ are kept private (not exposed to the page)."""

    def __init__(self):
        self._viewer = None

    def _viewer_closed(self):
        self._viewer = None

    def open_page(self, url, title="Tab"):
        """Open a tab or search page in Fretwork's own tab window."""
        try:
            if self._viewer is not None:
                self._viewer.load_url(url)
                self._viewer.set_title(f"Fretwork tab window - {title}")
                self._viewer.show()
                return {"ok": True}
        except Exception:
            self._viewer = None
        self._viewer = webview.create_window(f"Fretwork tab window - {title}", url=url, width=1050, height=850)
        self._viewer.events.closed += self._viewer_closed
        return {"ok": True}

    def import_page(self):
        """Read the text of the page you have open in the tab window (only when you press Import)."""
        if self._viewer is None:
            return {"error": "No tab window is open. Search for a song and open a tab or chord page first."}
        try:
            text = self._viewer.evaluate_js("document.body ? document.body.innerText : ''") or ""
            title = self._viewer.evaluate_js("document.title") or ""
        except Exception as e:
            return {"error": f"Could not read the tab window ({e})."}
        if not text.strip():
            return {"error": "The tab window is still loading or empty. Wait a moment and try again."}
        return {"text": text, "title": _clean_title(title)}

    def clipboard(self):
        try:
            return _read_clipboard()
        except Exception:
            return ""

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
    try:
        webview.start(private_mode=False, storage_path=data_dir(), icon=resource("fretwork.ico"))
    except TypeError:  # older pywebview without the icon argument
        webview.start(private_mode=False, storage_path=data_dir())


if __name__ == "__main__":
    main()
