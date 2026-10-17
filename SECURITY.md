# Security policy

## Reporting a vulnerability

Email **security@stellarpartners.gr** with a description and, if you can, the
steps to reproduce it. Do not open a public issue for a security problem.

Expect an answer within five working days. If the report is valid we will fix it
on `master`, which deploys the site, and credit you in the fix commit unless you
ask us not to.

## Scope

This repository is the published site. The root is served as-is by Cloudflare
Pages, so every tracked file is public.

In scope:

- the app at <https://qrcode.stellarpartners.gr/>
- the two CDN libraries, if the pinned hash or version is wrong
- anything that sends user data off the device

Out of scope:

- findings that need a compromised browser, extension or operating system
- missing headers on a page we do not control
- reports produced only by an automated scanner with no working proof
