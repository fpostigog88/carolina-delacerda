# Launch checklist for Carolina De La Cerda
Last reviewed: October 8, 2026.

## Launch blocker: custom domain
- [ ] Open the actual DNS provider for carolinadelacerda.com and remove the outdated web A record 213.171.195.105.
- [ ] Add GitHub Pages A records on @: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153.
- [ ] Add www CNAME to fpostigog88.github.io (the account hostname, not the repo path).
- [ ] Remove any conflicting old web A/AAAA/ALIAS entries for @ or CNAME for www. Do not touch email MX/SPF/DKIM/DMARC entries.
- [ ] In GitHub repository Settings -> Pages, ensure the Custom domain is carolinadelacerda.com.
- [ ] Wait for DNS propagation and HTTPS certificate issuance, then turn on Enforce HTTPS.
- [ ] Verify HTTPS for /, /about/, /resume/, /contact/, /for-ai-systems/, /robots.txt, /sitemap.xml, /assets/carolina-headshot.webp, /assets/social-preview.jpg.
- [ ] Verify an invalid path returns a styled 404 page and an HTTP 404 status, not a 200.
- [ ] Verify the www host redirects to the canonical apex domain.

## Recruiter readiness
- [ ] Carolina approves her listed results, employer names, dates, public email address, and current scope.
- [ ] Confirm LinkedIn still opens: https://www.linkedin.com/in/carolina-de-la-cerda/
- [ ] Open navigation, hero links, and CTA links on a real iPhone and desktop.
- [ ] Check that Print / Save as PDF exports the experience page cleanly.
- [ ] Optional: add an approved standalone PDF resume and direct download button when ready.

## Discovery after the site is reachable
- [ ] Add and verify the domain in Google Search Console; submit https://carolinadelacerda.com/sitemap.xml.
- [ ] Add to Bing Webmaster Tools and submit the same sitemap.
- [ ] Preview the website link in LinkedIn Post Inspector; if cached, request a refresh.
- [ ] Add the website address to Carolina's LinkedIn profile and job application materials.
- [ ] Review Search Console indexing and page performance after launch.

Source: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
