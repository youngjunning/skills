# Vercel Operations — Next.js Static Export Fiction Sites

Reference for deploying and operating `output: 'export'` Next.js sites on Vercel, scoped to this project's submodule-per-site architecture.

---

## 1. Project Setup

### New site via Vercel CLI

```bash
# Install once globally
npm i -g vercel

# Link from inside the submodule root (e.g. velvet-throne/)
cd velvet-throne
vercel link          # prompts: scope → project name
vercel env pull .env.local   # pull any existing env vars
```

### New site via Dashboard

1. vercel.com → **Add New Project**
2. Import the **main `fictions` repo** from GitHub (not the submodule directly — submodules aren't importable as standalone repos unless you push them separately).
3. Under **Root Directory**, set the submodule folder: e.g. `velvet-throne`
4. Framework preset will auto-detect **Next.js**. Verify build settings (see §3).

> Vercel rebuilds only happen when files under that root directory change. Changes to other submodules in the same push do not trigger a rebuild for unrelated projects — this is the correct behaviour for the submodule-per-site model.

---

## 2. Custom Domain Configuration

### DNS records

For apex domain (`velvet.fiction.example` is a subdomain, so CNAME is fine):

| Type  | Name               | Value                      |
|-------|--------------------|----------------------------|
| CNAME | `velvet`           | `cname.vercel-dns.com`     |
| CNAME | `midnight`         | `cname.vercel-dns.com`     |
| CNAME | `fuego`            | `cname.vercel-dns.com`     |
| CNAME | `wildfire`         | `cname.vercel-dns.com`     |
| CNAME | `london`           | `cname.vercel-dns.com`     |

For a true apex (e.g. `fiction.example` itself) you'd need an A record:

```
A  @  76.76.21.21
```

But since all sites use subdomains, CNAME is sufficient.

### Assign domain in dashboard

**Project → Settings → Domains → Add** → type the subdomain → Vercel validates the DNS.

Or via CLI:

```bash
vercel domains add velvet.fiction.example --project velvet-throne
```

### SSL

Vercel provisions Let's Encrypt automatically once DNS propagates. No action required.

---

## 3. Build Settings

These are set per-project in **Settings → General → Build & Development Settings**.

| Setting           | Value                        |
|-------------------|------------------------------|
| Framework Preset  | Next.js                      |
| Root Directory    | `velvet-throne` (or the relevant submodule folder) |
| Build Command     | `pnpm build` (or override: `next build && node scripts/preload-css.js`) |
| Output Directory  | `out` (auto-detected for `output: 'export'`) |
| Install Command   | `pnpm install`               |
| Node.js Version   | 20.x (match local version)   |

> **Root Directory** is the critical setting for submodule repos. Without it Vercel tries to build from repo root and fails.

### vercel.json — place in submodule root, not repo root

```json
{
  "headers": [
    {
      "source": "/(covers|illustrations)/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    },
    {
      "source": "/_next/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ],
  "rewrites": [
    { "source": "/covers/:file.json", "destination": "/___blocked___" },
    { "source": "/illustrations/:book/:file.json", "destination": "/___blocked___" }
  ]
}
```

> `/_next/static/` assets already get `immutable` from Next.js itself, but declaring it explicitly in `vercel.json` overrides any CDN stripping and makes the policy explicit.

### next.config.ts — canonical settings for this project

```ts
import { withContentCollections } from '@content-collections/next'
import path from 'path'
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'export',          // static HTML/CSS/JS only — no server-side runtime
  images: { unoptimized: true }, // required: next/image optimizer is server-side
  trailingSlash: true,       // /book/slug/ → out/book/slug/index.html
  turbopack: {
    resolveAlias: {
      'content-collections': './.content-collections/generated/index.js',
    },
  },
  webpack(config) {
    config.resolve.alias['content-collections'] = path.resolve(
      process.cwd(),
      '.content-collections/generated/index.js'
    )
    return config
  },
}

export default withContentCollections(nextConfig)
```

---

## 4. Environment Variables

### Add via CLI

```bash
# Add a secret (prompted for value)
vercel env add NEXT_PUBLIC_SITE_URL production

# Add for all environments at once
vercel env add NEXT_PUBLIC_SITE_URL

# List all vars
vercel env ls

# Pull to local .env.local
vercel env pull .env.local
```

### Add via Dashboard

**Project → Settings → Environment Variables**

- `NEXT_PUBLIC_*` prefix: exposed to browser JS bundle
- Non-prefixed: server-only — but since `output: 'export'` has **no server**, only `NEXT_PUBLIC_*` vars are available at runtime. Non-public vars are still accessible at build time (e.g. in `generateStaticParams`, `content-collections` config).

### Scope

Each env var is scoped to: **Production**, **Preview**, or **Development** (or all three).

| Variable               | Scope       | Notes                          |
|------------------------|-------------|--------------------------------|
| `NEXT_PUBLIC_SITE_URL` | Production  | Used in `metadataBase`         |
| `NEXT_PUBLIC_GA_ID`    | All         | Analytics IDs if needed        |

> For static sites there are no runtime secrets to protect — anything not needed at build time can be omitted entirely.

---

## 5. Cache-Control Headers

Vercel respects `Cache-Control` headers defined in `vercel.json`. The CDN (Vercel Edge Network) caches assets globally and serves them from the nearest edge PoP.

### Pattern in use

```json
{
  "headers": [
    {
      "source": "/(covers|illustrations)/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

- `max-age=31536000` = 1 year
- `immutable` = browser won't revalidate even on hard reload
- Applies to `/covers/*.png`, `/illustrations/**/*.webp`, etc.

### Extended example — full asset caching policy

```json
{
  "headers": [
    {
      "source": "/(covers|illustrations)/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/_next/static/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/fonts/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/(.*).html",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }
      ]
    }
  ]
}
```

> HTML pages should **not** be immutably cached — they need to be refreshed on each deploy. Vercel auto-invalidates the CDN on deploy for HTML, but `must-revalidate` ensures browser compliance.

---

## 6. Redirects and Rewrites

### Block internal JSON files (currently in use)

```json
{
  "rewrites": [
    { "source": "/covers/:file.json", "destination": "/___blocked___" },
    { "source": "/illustrations/:book/:file.json", "destination": "/___blocked___" }
  ]
}
```

This returns a 404 for `.json` metadata files that aren't meant to be publicly browsable.

### Redirect old slug to new slug

```json
{
  "redirects": [
    {
      "source": "/books/old-slug/",
      "destination": "/books/new-slug/",
      "permanent": true
    }
  ]
}
```

### Redirect www to apex (or vice versa)

Handle this at DNS level (CNAME both → Vercel) or in the Vercel dashboard's domain settings — **not** in `vercel.json` for static exports (rewrites can't proxy across hosts).

### Order of evaluation

Vercel evaluates in this order: `redirects` → `rewrites` → static files → `404.html`. For `output: 'export'` sites, there is no middleware or API layer, so redirects/rewrites are the only dynamic behaviour available.

---

## 7. Deploy Hooks

Deploy hooks let external systems (CMS, scripts, GitHub Actions) trigger a rebuild without a git push.

### Create a hook

**Project → Settings → Git → Deploy Hooks** → name it (e.g. `content-update`) → copy the URL.

```bash
# Trigger a rebuild manually
curl -X POST "https://api.vercel.com/v1/integrations/deploy/prj_xxxx/yyyyyyyy"
```

### Automate with a cron (example: rebuild nightly)

```bash
# crontab -e
0 3 * * * curl -s -X POST "https://api.vercel.com/v1/integrations/deploy/prj_xxxx/yyyyyyyy"
```

### GitHub Actions trigger

```yaml
- name: Trigger Vercel rebuild
  run: curl -X POST "${{ secrets.VERCEL_DEPLOY_HOOK_URL }}"
```

---

## 8. Vercel Analytics and Speed Insights

Only `Analytics` is wired by default. `SpeedInsights` is **opt-in only** — add it only when the user explicitly requests it on a specific site. New sites should wire Analytics only.

Rationale: Speed Insights requires adding the site to a Vercel project, which can trigger billing on non-Pro plans. Use it only for the primary paid-traffic test site or when the user specifically asks.

### Install Analytics (default)

```bash
pnpm add @vercel/analytics
```

### `src/app/layout.tsx`

```tsx
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

- `Analytics` tracks page views and referrer data.
- The component injects a tiny script that only fires on Vercel-hosted domains — it is a no-op in local dev (no data sent, no errors).

### Optional: Speed Insights

If the user explicitly asks for Speed Insights on a specific site:

```bash
pnpm add @vercel/speed-insights
```

```tsx
import { SpeedInsights } from '@vercel/speed-insights/next'
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <SpeedInsights />
        <Analytics />
      </body>
    </html>
  )
}
```

- `SpeedInsights` sends Core Web Vitals (LCP, CLS, INP, FID, FCP, TTFB) to Vercel.
- Also requires enabling in the dashboard.

- Analytics: page views, unique visitors, referrers, top paths
- Speed Insights: p75/p90 Web Vitals per route, device breakdown

---

## 9. Rollback and Deployment History

### View deployment list

```bash
vercel ls velvet-throne
```

Or: **Project → Deployments** in dashboard — lists every deploy with timestamp, git commit, status (Ready / Error / Cancelled).

### Instant rollback

```bash
# Get deployment URL from `vercel ls`
vercel rollback https://velvet-throne-abc123.vercel.app --project velvet-throne
```

Or in dashboard: click any past deployment → **Promote to Production**.

Rollback is instant — Vercel just re-points the production alias to the old deployment. No rebuild needed. The old build artifacts are retained for 30 days (Hobby) or longer (Pro).

### Deployment aliases

Each deploy gets a unique immutable URL: `velvet-throne-<hash>.vercel.app`. The production domain (`velvet.fiction.example`) is just an alias that points to the current production deployment. You can manually re-alias any past deploy:

```bash
vercel alias set velvet-throne-abc123.vercel.app velvet.fiction.example
```

---

## 10. Team and Project Permissions

### Hobby (personal account)

- Single owner, no team roles
- All projects under one account
- Fine for personal fiction sites

### Pro Team

- **Owner**: full access, billing
- **Member**: can deploy, view logs, manage env vars
- **Viewer**: read-only (deployments, analytics, logs)

Manage at: **team.vercel.com → Settings → Members**

### Per-project access (Pro)

Projects can be restricted to specific team members via **Project → Settings → Access**. Useful if you eventually have collaborators who should only see one site.

### API tokens

For CI/CD or deploy hooks that need the Vercel API:

```bash
# Create token: vercel.com → Account Settings → Tokens
# Scope: full account or specific team
vercel --token $VERCEL_TOKEN ls
```

---

## 11. Cost: Hobby vs. Pro

| Limit                    | Hobby (Free)        | Pro ($20/mo per member) |
|--------------------------|---------------------|--------------------------|
| Bandwidth                | 100 GB/mo           | 1 TB/mo included         |
| Build minutes            | 6,000 min/mo        | 24,000 min/mo            |
| Deployments              | Unlimited           | Unlimited                |
| Team members             | 1 (personal)        | Unlimited                |
| Custom domains           | Unlimited           | Unlimited                |
| Analytics / Speed Insights | Basic            | Full (90-day retention)  |
| Deploy previews          | Unlimited           | Unlimited                |
| Deploy protection        | No                  | Yes (password/SSO)       |
| Support                  | Community           | Email                    |
| Retention (build logs)   | 7 days              | 30 days                  |

**For static fiction sites**: Hobby is sufficient unless bandwidth exceeds 100 GB/mo or you need team access. 100 GB is roughly 1 million page views if each page is ~100 KB.

Bandwidth overages on Pro: $0.40/GB. On Hobby, site is rate-limited/suspended until month resets.

---

## 12. Common Pitfalls with `output: 'export'`

| Pitfall | Explanation | Fix |
|---------|-------------|-----|
| **No API routes** | `app/api/*/route.ts` files are silently ignored or throw a build error | Remove all API routes; use external APIs only |
| **No ISR / revalidation** | `revalidate` in `fetch()` or `export const revalidate` has no effect | All pages are fully static at build time |
| **No middleware** | `middleware.ts` is not executed | Use `vercel.json` redirects/rewrites instead |
| **No `next/image` optimization** | Remote image URLs won't be optimized | Set `images: { unoptimized: true }` in next.config — already done |
| **Dynamic routes need `generateStaticParams`** | Every `[slug]` page must enumerate all params at build time | Always export `generateStaticParams` for dynamic segments |
| **`cookies()` / `headers()` crash** | These are server-only; `output: 'export'` has no server context | Don't use them; pass data via props or client-side fetch |
| **`not-found.tsx` becomes `404.html`** | Vercel auto-serves this for unmatched paths | Works correctly; just ensure the file exists |
| **Missing trailing slash** | `trailingSlash: true` must be set; without it, `/books/slug` → `out/books/slug.html`, which Vercel serves but some CDNs don't handle cleanly | Already set in next.config |
| **`content-collections` path alias** | The generated index file path must be aliased for both webpack and Turbopack | Already handled in both webpack and turbopack config blocks |
| **Build command must include post-build scripts** | `next build` alone doesn't run `scripts/preload-css.js` | Set build command to `next build && node scripts/preload-css.js` in Vercel settings |

---

## 13. Post-Deploy Monitoring Checklist

Run through this after every production deploy:

### Immediate (0–5 min)

- [ ] Deployment status is **Ready** in dashboard (not **Error**)
- [ ] Production URL resolves: `curl -I https://velvet.fiction.example` → `200 OK`
- [ ] Custom domain SSL is valid: `curl -vI https://velvet.fiction.example 2>&1 | grep "SSL certificate"`
- [ ] Homepage loads in browser, no console errors
- [ ] A cover image loads and has correct `Cache-Control: public, max-age=31536000, immutable` header:
  ```bash
  curl -sI "https://velvet.fiction.example/covers/some-book.png" | grep -i cache-control
  ```
- [ ] `.json` metadata files return 404:
  ```bash
  curl -o /dev/null -s -w "%{http_code}" "https://velvet.fiction.example/covers/some-book.json"
  # expect: 404
  ```

### Short-term (1–24 hr)

- [ ] Speed Insights tab shows incoming Web Vitals data
- [ ] Analytics tab shows page view traffic
- [ ] Check Vercel Functions tab — should be empty for static sites (no function invocations)
- [ ] Google Search Console: submit updated sitemap if books were added/removed
- [ ] Facebook Pixel Helper (browser extension): confirm `PageView` fires on load

### Ongoing

- [ ] Monitor **Bandwidth usage** in dashboard if traffic grows (Hobby: 100 GB/mo cap)
- [ ] Check **Build Logs** if a deploy fails — most common causes: missing `generateStaticParams`, broken import path, pnpm lockfile mismatch
- [ ] LCP score in Speed Insights: target < 2.5 s. If degraded, check cover image sizes and font preloading.

---

## 14. Useful CLI Commands Reference

```bash
# Deploy to production immediately (skip preview)
vercel --prod

# Deploy preview (get a unique URL for testing)
vercel

# Check current project info
vercel inspect https://velvet-throne-abc.vercel.app

# Tail real-time build logs
vercel logs https://velvet-throne-abc.vercel.app --follow

# List all projects in account
vercel ls

# List deployments for a specific project
vercel ls velvet-throne

# Remove a deployment
vercel remove velvet-throne-abc.vercel.app

# Pull latest environment variables
vercel env pull .env.local

# Add env var to production
vercel env add NEXT_PUBLIC_SITE_URL production

# Open project dashboard in browser
vercel open

# Switch team/scope
vercel switch
```
