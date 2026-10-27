# agrexpert.ru

Static site of AGREXPERT (АГР / АГО). These HTML files ARE the site. Every push to `main` is uploaded to Sprinthost by `.github/workflows/deploy.yml`.

- Blog sources and builder: `_blog/` (see `_blog/RUNBOOK.md`). Not uploaded to the server.
- Build: `python3 _blog/build.py --check`
- FTP password: repository Secret `FTP_PASSWORD`. Server folder: `domains/agrexpert.ru/public_html/` (override with Variable `FTP_SERVER_DIR`).
- `send.php` and `private/` (form handler config with the Telegram bot token, saved leads) live only on the server and are never committed or uploaded.
- Analytics: Yandex Metrika 113822254, loaded only after cookie consent.
