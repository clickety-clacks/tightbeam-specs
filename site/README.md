# Tightbeam documentation site

This directory contains the static HTML for `https://tightbeam.ing/docs/`.
The index links to the Engram and Tightbeam integration report, adapted from
the September 19, 2026 Lavish report. The separate Engram storage recommendations
are excluded from this public page.

The operating source is `../engram-local-setup-2026-09-21.md`. The original research is `../engram-integration-recon-2026-09-19.md` and is preserved publicly in `docs/engram-integration-research-20260919.html`. Keep the operating HTML and its source document consistent. These files need no build step.

Published on September 19, 2026. Both docs pages were verified over public
HTTPS against their source hashes. HTTP redirects to HTTPS, the apex root
redirects to `/docs/`, and the existing blog remains available. Certbot's
renewal timer is active.

## Hosting

The site uses nginx on `tbing`, the server that also hosts `blog.tightbeam.ing`.
The apex has its own virtual host and web root, `/var/www/tightbeam.ing`.
Requests to `/` redirect to `/docs/`.

Porkbun manages the DNS zone. The apex A record must point to `143.198.229.224`.
`nginx/tightbeam.ing.http.conf` is the HTTP bootstrap configuration. After DNS
resolves, Certbot's nginx plugin adds the apex certificate and HTTPS redirect
to `/etc/nginx/sites-available/tightbeam.ing` on the server. Do not overwrite
that active configuration with the bootstrap file during content updates.

## Updating content

From this repository, upload the two HTML files to staging paths:

```sh
scp site/docs/index.html tbing:/tmp/tightbeam-docs-index.html
scp site/docs/engram-integration.html tbing:/tmp/tightbeam-docs-engram-integration.html
```

Install the staged files through SSH:

```sh
ssh tbing 'install -m 0644 -o www-data -g www-data /tmp/tightbeam-docs-index.html /var/www/tightbeam.ing/docs/index.html'
ssh tbing 'install -m 0644 -o www-data -g www-data /tmp/tightbeam-docs-engram-integration.html /var/www/tightbeam.ing/docs/engram-integration.html'
```

Content updates do not require an nginx reload. Verify that `/docs/` and
`/docs/engram-integration.html` return HTML over HTTPS, compare the served report
with the source, and confirm `https://blog.tightbeam.ing/` still responds.
