# From Grades to Growth website

Static site for **fromgradestogrowth.com**. Plain HTML and CSS, no framework, no build step
on the server. Pages are generated locally by `build.py` and the output in `site/` is
committed, so Netlify just serves files.

Migrated off Lovable — see the living project doc (`instructions.md`) and the general
migration playbook, both kept in the Dropbox project folder
(`BeaconHillCommunityUniversity/9. Website/`), for the full story, decisions, and gotchas.

---

## Where this lives

| Field | Value |
|---|---|
| Repo | https://github.com/mbraithwaite9/grades-to-growth-site |
| Domain | fromgradestogrowth.com |
| Branch that deploys | `main` |
| Publish directory | `site` |
| Build command | none |
| Netlify account | **A separate account from the one used for AutoTech Fusion / Ottawa ATC — do not connect this to that team.** Which account, TBD. |
| Form backend | Netlify Forms (no database — submissions show up under Forms in the Netlify dashboard) |

The old Lovable-synced repo, `mbraithwaite9/grades-to-growth`, is a separate, unrelated repo
kept as a backup for now. It is not connected to this one.

---

## Deploy to Netlify via GitHub (the main route)

1. **Push this folder to the repo**

   ```bash
   git init
   git branch -M main
   git add .
   git commit -m "From Grades to Growth static site"
   git remote add origin https://github.com/mbraithwaite9/grades-to-growth-site.git
   git push -u origin main
   ```

   The first push opens a browser window to authorise GitHub. Sign in as **mbraithwaite9**.

   If the push is rejected because the remote already has a commit (e.g. a README created
   when the repo was made on GitHub):

   ```bash
   git pull origin main --rebase --allow-unrelated-histories
   git push -u origin main
   ```

2. **Connect it in Netlify**

   Sign in to the Netlify account this project should use (not Ottawa-ATC/mbraithwaite9's
   existing team) → *Add new site* → *Import an existing project* → *Deploy with GitHub* →
   **mbraithwaite9/grades-to-growth-site** → branch `main`.

   Netlify reads `netlify.toml`, so the settings should fill themselves in. Confirm:

   | Setting | Value |
   |---|---|
   | Build command | *(leave empty)* |
   | Publish directory | `site` |

3. **Add the domain**

   Netlify → *Domain management* → *Add a domain* → `fromgradestogrowth.com`, then point
   Namecheap at Netlify's nameservers or add the records Netlify shows you. HTTPS is
   automatic once DNS resolves. Once confirmed working, remove the old Namecheap URL
   Redirect Record so there's no overlap.

That's it. Every `git push` redeploys, with version history and one-click rollback under
*Deploys*.

---

## Deploy without GitHub (fallback)

Slower to maintain, no version history, but needs nothing installed.

1. Unzip the download. You get a folder called `grades-to-growth-site`.
2. Go to **https://app.netlify.com/drop**
3. Drag the folder called **`site`** onto the page (the one inside `grades-to-growth-site`,
   not the outer folder itself).
4. Wait about ten seconds. The site is live at a random address such as
   `curious-pastry-8a3f21.netlify.app`.
5. Click *Claim your site* and sign up, otherwise the deploy expires.
6. *Domain management* → add `fromgradestogrowth.com` when ready to switch it over.

The security headers and redirects still apply on this route, because they live in
`site/_headers` and `site/_redirects` rather than only in `netlify.toml`.

To update later, drag the `site` folder onto the same site's *Deploys* page. That replaces
everything. Do not mix the routes on one site: once a repo is linked, the next push
overwrites anything dragged in by hand.

---

## Making changes

All the site's content lives in `build.py`, near the top (`SETTINGS` and the `DATA` lists).

```bash
python3 build.py     # regenerates ./site/
git add -A && git commit -m "Update copy" && git push
```

Do not hand-edit files in `site/`. They are overwritten on the next build.

---

## What is in here

```
build.py              generator, and the single source of all content
netlify.toml          Netlify config: publish dir and no build command
assets/               CSS and image sources
site/                 generated output, this is what Netlify serves
```

---

## Before launch

1. ~~Replace the placeholder Facilitator bio.~~ Done — real photo and bio are in place.
2. **Test the "Stay Updated" form end-to-end** on the live Netlify deploy — submit it and
   confirm it shows up under **Forms** in the Netlify dashboard. Visual QA is done; this
   functional check is not yet done (Python's local dev server used for previews doesn't
   support POST, so this can only be confirmed on the real deploy).
