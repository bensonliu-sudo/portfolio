# Bingcheng Liu — Portfolio

Personal portfolio for software, AI and data projects. Independent from the individual project repositories.

## Development

A buildless static site with no runtime dependencies, external fonts or analytics.

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173. Edit `index.html` to update the page.

## Deployment

Import this repository into Vercel. Framework preset: **Other**. No build command; serve the repository root. The intended production domain is **bingchengliu.com**, with `www` redirecting to the apex domain.

The stock-scoring project is linked as source code. This portfolio does not host its Python backend, audit database or private development records. The ranking graphic is an explicitly labelled conceptual illustration.
