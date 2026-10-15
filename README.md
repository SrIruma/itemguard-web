# itemguard-web

The documentation site for [ItemGuard](https://github.com/SrIruma/ItemGuard).

It's a static site — plain HTML, CSS and JavaScript, no build step. Open
`index.html` and it works.

## Pages

One view with three sections, switched with the sidebar and searchable with the
box in the top bar (press `/` to jump to it):

- **Documentation** — overview, installation, commands, permissions, config,
  protection flags and the placeholder tokens.
- **Addon API** — how to build a bridge, the `ItemGuardIntegration` interface and
  the API downloads.
- **Community Addons** — the addons in the repository's `addons/` folder and how
  to submit your own.

## Local preview

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Serving it over HTTP (rather than opening the file directly) makes the downloads
behave the same way they do on Pages.

## Adding a community addon

Drop the addon JAR into `addons/`, then add an entry to the `ADDONS` array near
the top of `js/app.js`:

```js
{
    file: "YourBridge.jar",
    name: "Your Bridge",
    author: "YourName",
    description: "What it does.",
    version: "1.0.0",
    href: "addons/YourBridge.jar"
}
```

## API artifacts

The files in `api/` are copies of the build output from the main repository
(`api/target/itemguard-api*.jar`). Replace them when the API changes.

## License

MIT for the site and the bundled API. The ItemGuard core plugin is proprietary.
