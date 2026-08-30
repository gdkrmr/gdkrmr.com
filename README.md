# gdkrmr.com

Sources of my personal website, built with [Quarto](https://quarto.org) and
hosted on GitHub Pages at <https://gdkrmr.com>.

## Layout

- `index.qmd`, `publications.qmd`, `impressum.qmd`, `404.qmd`: top-level pages.
- `projects/posts/`: one `.qmd` per software project; the listing on
  `projects/index.qmd` is generated from them.
- `blog/posts/`: blog posts, listed on `blog/index.qmd`.
- `resources/`: CV, bibliography and CSL style, self-hosted fonts and
  Academicons, images.
- `theme.scss`, `light.scss`, `dark.scss`, `styles.css`: custom theme.
- `src/gdkrmr_com/og_images.py`: pre-render hook that downloads a preview
  image for every project post that has a `link:` but no `image:`.

## Building

Requires Quarto and [uv](https://docs.astral.sh/uv/).

```sh
uv sync            # Python dependencies for the pre-render hook
quarto preview     # local development server
quarto render      # builds into _site/
```

Publications are rendered from `resources/documents/publications.bib`; add an
entry there to add a publication.
