#!/usr/bin/env python3
"""
Local git-backed history viewer for how-to-ai.

    python3 history/serve.py        # then open http://localhost:8770

Serves the page with a small "history" control in the corner. Pick any commit
and the server hands you `git show <sha>:index.html` — the page exactly as it
was at that commit. The control is injected only by this server, so it never
appears in the committed file or the published artifact.
"""
import http.server
import json
import os
import re
import subprocess
import sys
import webbrowser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8770


def git(*args):
    return subprocess.run(
        ["git", "-C", ROOT, *args], capture_output=True, text=True, check=True
    ).stdout


def commits():
    out = git("log", "--reverse", "--date=short",
              "--pretty=%H%x00%h%x00%ad%x00%s")
    rows = []
    for line in out.strip().splitlines():
        full, short, date, subject = line.split("\x00")
        rows.append({"sha": full, "short": short, "date": date, "subject": subject})
    return rows


def page_at(ref):
    """`index.html` as of a commit (or the working tree for ref='WORKING')."""
    if ref == "WORKING":
        return open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    return git("show", f"{ref}:index.html")


PANEL_CSS = """
#h9-btn{position:fixed;left:14px;bottom:14px;z-index:99999;font:600 11px/1 -apple-system,
BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:.08em;text-transform:uppercase;
color:#1F6FA8;background:#fff;border:1px solid #CFE3F2;border-radius:999px;padding:7px 13px;
cursor:pointer;box-shadow:0 6px 18px -6px rgba(19,58,84,.4);}
#h9-btn:hover{border-color:#1F6FA8;}
#h9-wrap{position:fixed;inset:0;z-index:99998;background:rgba(20,40,55,.34);
display:none;align-items:flex-end;justify-content:flex-start;padding:14px;}
#h9-wrap.open{display:flex;}
#h9-panel{background:#fff;border:1px solid #CFE3F2;border-radius:14px;width:min(420px,92vw);
max-height:70vh;overflow:auto;box-shadow:0 24px 60px -18px rgba(19,58,84,.5);
font:13px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#1B2A33;}
#h9-panel h4{margin:0;padding:14px 16px 10px;font:600 11px/1 -apple-system,sans-serif;
letter-spacing:.12em;text-transform:uppercase;color:#5C7180;border-bottom:1px solid #EAF3FB;}
.h9-row{display:block;width:100%;text-align:left;border:0;background:none;font:inherit;
color:inherit;padding:11px 16px;cursor:pointer;border-bottom:1px solid #F2F8FD;}
.h9-row:hover{background:#F2F8FD;}
.h9-row.cur{background:#EAF3FB;}
.h9-row .d{color:#5C7180;font-size:11px;font-variant-numeric:tabular-nums;}
.h9-row .s{display:block;margin-top:2px;}
.h9-row .tag{color:#F0640A;font-weight:700;}
"""

PANEL_JS = """
(function(){
  var here = %s;               // current ref shown
  var rows = %s;               // commit list (oldest first)
  var btn = document.createElement('button');
  btn.id = 'h9-btn'; btn.textContent = '\\u25F7 history';
  var wrap = document.createElement('div'); wrap.id = 'h9-wrap';
  var panel = document.createElement('div'); panel.id = 'h9-panel';
  var html = '<h4>Version history</h4>';
  rows.slice().reverse().forEach(function(c, i){
    var cur = (c.sha === here || c.short === here) ? ' cur' : '';
    var tag = (i === 0 ? '<span class="tag">latest</span> ' : '');
    html += '<button class="h9-row' + cur + '" data-sha="' + c.sha + '">'
      + '<span class="d">' + c.date + ' \\u00b7 ' + c.short + '</span>'
      + '<span class="s">' + tag + c.subject.replace(/</g,'&lt;') + '</span></button>';
  });
  panel.innerHTML = html;
  wrap.appendChild(panel);
  btn.addEventListener('click', function(){ wrap.classList.add('open'); });
  wrap.addEventListener('click', function(e){ if(e.target === wrap) wrap.classList.remove('open'); });
  panel.addEventListener('click', function(e){
    var r = e.target.closest('.h9-row'); if(!r) return;
    location.href = '/at/' + r.getAttribute('data-sha');
  });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') wrap.classList.remove('open'); });
  document.body.appendChild(btn);
  document.body.appendChild(wrap);
})();
"""


def inject(page_html, ref):
    rows = commits()
    control = (
        "<style>" + PANEL_CSS + "</style>\n<script>"
        + PANEL_JS % (json.dumps(ref), json.dumps(rows))
        + "</script>\n"
    )
    if "</body>" in page_html:
        return page_html.replace("</body>", control + "</body>", 1)
    return page_html + control


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, body, ctype="text/html; charset=utf-8"):
        b = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        path = self.path.split("?")[0]
        try:
            if path in ("/", "/index.html"):
                self._send(inject(page_at("WORKING"), "WORKING"))
            elif path == "/api/commits":
                self._send(json.dumps(commits()), "application/json")
            elif path.startswith("/at/"):
                ref = re.sub(r"[^0-9a-zA-Z]", "", path[len("/at/"):])
                self._send(inject(page_at(ref), ref))
            else:
                self.send_error(404)
        except subprocess.CalledProcessError as e:
            self.send_error(500, e.stderr.strip() or "git error")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    if not os.path.isdir(os.path.join(ROOT, ".git")):
        sys.exit("no git repo at " + ROOT)
    url = f"http://localhost:{PORT}"
    print(f"how-to-ai history viewer  →  {url}   (Ctrl+C to stop)")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    http.server.HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
