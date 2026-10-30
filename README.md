# artkeeper.app

The public website for Art Keeper: a home page, Support, Privacy Policy, Terms of Use and a 404 page. Plain HTML and one stylesheet, served by GitHub Pages.

No analytics, no cookies, no tracking and no third-party requests: the fonts (Figtree, and Instrument Serif in case headlines switch to serif) are self-hosted in `assets/fonts/` under the SIL Open Font License. The privacy policy promises this, so keep it that way.

## Files

| Path | What it is |
| --- | --- |
| `index.html`, `support/`, `privacy/`, `terms/`, `404.html` | The built pages (committed, served as they are) |
| `assets/site.css` | The one stylesheet. All colours and font families are custom properties at the top |
| `assets/fonts/` | Self-hosted woff2 fonts (Latin subset) and their licences |
| `favicon-32.png`, `apple-touch-icon.png`, `assets/icon-192.png` | From the app icon |
| `CNAME` | `artkeeper.app`, for GitHub Pages |
| `.well-known/apple-app-site-association` | Tells iOS that invite links (`/join/*`) open the Art Keeper app. Team ID NY5J499945, bundle IDs `app.artkeeper` and `app.artkeeper.redesign`. Published because `_config.yml` includes `.well-known` |
| `404.html` and `/join/…` | Invite links (`artkeeper.app/join/K7QM-3XRP`) have no page of their own: GitHub Pages serves `404.html`, whose script shows the invite (code, Get Art Keeper) instead. The Get Art Keeper link is `data-href` in `_src/404.html` (empty: the button is hidden and a beta note shows) |
| `_src/` | Page content. `_src/legal/` holds the approved Privacy Policy and Terms, word for word |
| `build.py` | Wraps `_src/` pages in the shared header and footer (Python 3, standard library only) |
| `_config.yml` | Keeps `README.md`, `build.py` and `screenshots/` off the public site (`_src/` is skipped because it starts with `_`) |
| `screenshots/` | Local previews at 393px and 1280px, light and dark. Not published |

## Editing

1. Change a page in `_src/` (or the stylesheet).
2. Run `python3 build.py`.
3. Preview, then commit.

**Legal text:** never edit the Privacy Policy or Terms by hand. Replace `_src/legal/privacy.html` or `_src/legal/terms.html` with the newly approved file and run `python3 build.py`. The build copies the `<body>` exactly; its only change is wrapping the permissions table so it scrolls on narrow phones.

**Switching the look:** the top of `assets/site.css` has every colour and font family:

- Accent: change the five "Accent" tokens in both the light block and the dark block.
- Serif headlines (Saffron Studio's default): set `--font-display: var(--font-serif);` and `--display-weight: 400;`.

**App screenshots on the home page:** save them as `images/screens/01.png` to `06.png`, write each one's alt text in `_src/home.html` (the `screens:start` comment explains), and run `python3 build.py`. The carousel stays out of the page until at least one image exists.

**Going live on the App Store:** see the `TODO(launch)` comment in `_src/home.html`. It says where Apple's official badge comes from and has the link (App Store ID 6821221274) ready.

## Preview locally

```bash
cd /Users/jason/Documents/Claude/artkeeper-site
python3 -m http.server 8000
```

Open http://localhost:8000. (Python's server doesn't show `404.html` for missing pages; open http://localhost:8000/404.html to see it. GitHub Pages uses it automatically.)

## Publishing on GitHub Pages (later, with Jason's yes)

Checked against GitHub's docs on 2026-10-12:
[Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site),
[Managing a custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site),
[Verifying your custom domain](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages).

GitHub recommends verifying the domain **first**, and adding it to the repository **before** pointing DNS at GitHub, so nobody else can claim it.

1. **Verify the domain** (account-wide, once). On GitHub: profile picture > **Settings** > **Pages** (under "Code, planning, and automation") > **Add a domain** > `artkeeper.app` > **Add domain**. GitHub shows a TXT record; add it at Spaceship (below), wait for it to resolve, then click **Verify**. Keep that TXT record for good.
2. **Create a public repository** under `jsanio` (for example `artkeeper-site`), add it as this folder's remote and push `main`. (GitHub Pages on a free account needs a public repo.)
3. **Turn on Pages.** Repository > **Settings** > **Pages** > "Build and deployment" > **Source: Deploy from a branch** > branch **main**, folder **/(root)** > **Save**.
4. **Custom domain.** Same page, under "Custom domain": enter `artkeeper.app` > **Save**. (The `CNAME` file in this folder already says `artkeeper.app`.)
5. **Add the DNS records** at Spaceship (below).
6. **Enforce HTTPS.** Back on the Pages settings, tick **Enforce HTTPS** once it's available. GitHub says it can take up to 24 hours after DNS is set.
7. Check https://artkeeper.app, https://www.artkeeper.app (redirects to the apex), and /privacy, /terms and /support. The app links to `https://artkeeper.app/privacy` and `/terms`, without the trailing slash; GitHub Pages redirects those to the folder pages.

## DNS records at Spaceship

Spaceship > Domains > artkeeper.app > **Advanced DNS** (manage DNS records). First remove any parking or default `A`, `AAAA` or `CNAME` records on `@` and `www` that point elsewhere. **Leave any MX or email TXT records alone**: they carry support@artkeeper.app.

| Type | Host | Value | Notes |
| --- | --- | --- | --- |
| A | `@` | `185.199.108.153` | |
| A | `@` | `185.199.109.153` | |
| A | `@` | `185.199.110.153` | |
| A | `@` | `185.199.111.153` | |
| AAAA | `@` | `2606:50c0:8000::153` | |
| AAAA | `@` | `2606:50c0:8001::153` | |
| AAAA | `@` | `2606:50c0:8002::153` | |
| AAAA | `@` | `2606:50c0:8003::153` | |
| CNAME | `www` | `jsanio.github.io` | The account's Pages domain, no repository name. Not the `*.pages.github.io` address |
| TXT | `_github-pages-challenge-jsanio` | (the value GitHub shows in step 1) | Domain verification. Keep it |

Don't add a wildcard (`*`) record; GitHub warns it allows takeover.

To check from a terminal once saved:

```bash
dig artkeeper.app +noall +answer -t A
dig artkeeper.app +noall +answer -t AAAA
dig www.artkeeper.app +nostats +nocomments +nocmd
dig _github-pages-challenge-jsanio.artkeeper.app +nostats +nocomments +nocmd TXT
```

`artkeeper.co` isn't covered here. If it should forward to artkeeper.app, Spaceship's URL redirect for that domain is the simplest way.
