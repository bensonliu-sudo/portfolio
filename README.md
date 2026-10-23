# Bingcheng Liu — Portfolio

Personal portfolio for software, AI and data projects. Independent from the individual project repositories.

## Maintenance handoff / CC 接手入口

更新作品或配置前，请先读 [作品集介绍与部署维护](docs/作品集介绍与部署维护.md)：网站定位、资源入口、域名与 DNS、Vercel 自动部署、更新流程及待办均记录在此。配置变更后继续更新同一文档。

## Development

A buildless static site with no runtime dependencies, external fonts or analytics.

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open http://127.0.0.1:4173. Edit `index.html` to update the page.

## Deployment

Import this repository into Vercel. Framework preset: **Other**. No build command; serve the repository root. The production domain is **bingchengliu.com**, with `www` redirecting to the apex domain.

The stock-scoring project is linked as source code. This portfolio does not host its Python backend, audit database or private development records. The ranking graphic is an explicitly labelled conceptual illustration.

## Deployment record — 2026-10-24

- Production: https://bingchengliu.com
- `https://www.bingchengliu.com` redirects permanently (308) to the apex domain.
- Hosting: Vercel Hobby; project `portfolio`; production branch `main`.
- DNS: Cloudflare; apex and `www` use the CNAME target recommended by the Vercel project, in DNS-only mode.
- GitHub App access was limited to this repository. Pushes to `main` trigger production deployments.
- Initial validation: HTML anchors/configuration checked; local and deployed pages opened successfully; custom-domain HTTPS and the `www` redirect verified in the browser. Mainland China network performance has not been tested.
