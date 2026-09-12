# TODO before going live

## Blockers

- [ ] Replace `resources/documents/cv.pdf`: the current file contains home
      address, mobile number and date of birth in plain text, undoing the
      obfuscation on the Impressum. It is also from June 2023 and still names
      the Institute for Geology and Geophysics. NOTE: remove CV for now.
- [ ] Set up deployment: this repo has no git remote and no GitHub Actions
      workflow (`CNAME` file is in place). The Datenschutzerklärung promises GitHub
      Pages hosting.
- [x] Connect the domain: `gdkrmr.com` currently resolves to a Namecheap
      parking page. Add DNS records for GitHub Pages and enforce HTTPS once the certificate is issued.
- [ ] Decide what happens to the old site: `www.guido-kraemer.com` still serves
      the Hugo Academic site from the `master` branch of
      `gdkrmr/gdkrmr.github.io`. Either replace it there or redirect the old
      domain; old URLs (`/publication/…`, `/software/…`, `/post/…`) will
      otherwise go dead.

## Should fix before launch

- [x] Add a 404 page (`404.qmd`).
- [x] Add a favicon in `_quarto.yml`.
- [x] Add `website.description` and a default social image so link previews
      show more than the title.
- [ ] Rewrite the launch blog post (`blog/posts/2026_09_03_new_website.qmd`):
      fix "I switched to build system from Hugo Academic to Quarto" and set the
      date to the actual launch date.
- [x] Twitter: the navbar links to twitter.com and the Impressum mentions X.
      Keep both or drop both.
- [ ] Deploy workflow must install `uv` for the `og_images` pre-render hook and
      tolerate fetch failures (the hook hits the network).

## Polish

- [x] Remove the leftover `<!-- This does not work -->` comments from every
      project post in `projects/posts/`.
- [x] Fix typo "Smooting" in `projects/posts/srdfilter.jl.qmd` categories.
- [x] Fill in `README.md`.
- [x] `pyproject.toml`: replace "Add your description here", drop the unused
      `jupyter` dependency.
- [x] Footer year is hard-coded to 2026 in `_quarto.yml` (now bumped to the
      current year by an inline script; the build year stays as fallback).
- [x] Take publications from CV, there is a cleaned up bib file.
- [x] Blacklist TODO.qmd
- [x] rename "Projects" -> "Software"
