# Updates

**Script:** [Updates (script)](../updates.py)

## Purpose
Monorepo auto-update standard (root CLAUDE.md, Rule #23): the LAST released
version on GitHub is the source of truth, and the running app offers an
UPDATE when it is behind. `check(repo, enabled)` compares the latest release
tag of the project's repo against the running version (`app_version()`) and
returns an `Update(version, installer_url, page_url)`, or `None`.

`None` is the documented result for: up to date, check disabled, a dev
checkout (version has no numbers), a repo with no releases yet, or any
network failure — logged at info, never raised (the app starts fine
offline).

## Pseudocode

```
app_version():
    TRY import version.__version__
    ON failure -> read version.py text next to the bundle, regex the string
    ON failure -> "dev"

check(repo, enabled):
    IF disabled OR not repo -> None
    current = numbers from app_version() ("0.1.230" -> (0,1,230))
    IF current is empty -> None                      # dev checkout
    GET api.github.com/repos/<repo>/releases/latest  (10 s timeout)
    ON any failure -> log info, None
    latest = numbers from tag_name ("v0.1.23" -> (0,1,23))
    IF latest empty OR latest <= current -> None
    installer_url = first release asset ending in .exe (or None)
    RETURN Update(latest, installer_url, release page URL)
```

## Config
`config.json → update`: `{ "repo": "UVuruna/Ultra-Vivid", "check": true }`
(defaults apply when the section is absent).

## Connections
### Used by
- [Main Window](../../gui/__about/main_window.md) — startup check → in-window
  Update button (download installer → launch → quit so files can be replaced)
