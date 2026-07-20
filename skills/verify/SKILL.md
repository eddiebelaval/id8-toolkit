---
name: verify
version: 1.0.0
description: |
  Unified verification skill — chains static analysis, tests, and visual/browser
  verification into one loop (Boris Cherny's verify-app pattern). Use when: "verify",
  "/verify", after completing a feature, before a PR, after merging main, or debugging.
  Modes: /verify (full suite), /verify quick (static only), /verify visual (browser),
  /verify deploy <url> (production curl + Playwright + Vercel/CF).
---

# /verify - Unified Verification Skill

A comprehensive verification skill that chains static analysis, tests, and visual verification. Inspired by Boris Cherny's "verify-app" subagent pattern.

## Trigger
- `/verify` - Run full verification suite
- `/verify quick` - Static analysis only
- `/verify visual` - Browser-based visual verification
- `/verify deploy <url>` - Production deployment verification (curl + Playwright + Vercel/CF)
- `/verify [component]` - Verify specific component/feature

## Philosophy

> "The most important thing to get great results out of Claude Code -- give Claude a way to verify its work."
> — Boris Cherny, Creator of Claude Code

This skill provides that verification loop. It should be run:
1. After completing a feature
2. Before creating a PR
3. After merging from main
4. When debugging issues

## Verification Layers

```
┌─────────────────────────────────────┐
│  Layer 1: Static Analysis           │
│  - TypeScript compilation           │
│  - ESLint/Biome linting             │
│  - Prettier formatting check        │
├─────────────────────────────────────┤
│  Layer 2: Unit Tests                │
│  - Jest/Vitest unit tests           │
│  - Component tests                  │
│  - Utility function tests           │
├─────────────────────────────────────┤
│  Layer 3: Integration Tests         │
│  - API route tests                  │
│  - Database integration             │
│  - Service layer tests              │
├─────────────────────────────────────┤
│  Layer 4: E2E Tests                 │
│  - Playwright browser tests         │
│  - Critical user flows              │
│  - Cross-browser verification       │
├─────────────────────────────────────┤
│  Layer 5: Visual Verification       │
│  - Live browser inspection          │
│  - Screenshot comparison            │
│  - Console error detection          │
│  - Network request validation       │
├─────────────────────────────────────┤
│  Layer 6: Build Verification        │
│  - Production build succeeds        │
│  - Bundle size check                │
│  - No build warnings                │
└─────────────────────────────────────┘
```

## Execution Protocol

### Full Verification (`/verify`)

```
1. STATIC ANALYSIS
   ├── Run: npm run type-check || npx tsc --noEmit
   ├── Run: npm run lint
   └── GATE: Must pass before continuing

2. UNIT TESTS
   ├── Run: npm test
   ├── Collect: Coverage report
   └── GATE: Must pass before continuing

3. E2E TESTS (if playwright.config exists)
   ├── Run: npx playwright test
   └── GATE: Must pass before continuing

4. VISUAL VERIFICATION (using Playwright MCP)
   ├── Start dev server if not running
   ├── Navigate to key pages
   ├── Take screenshots
   ├── Check console for errors
   ├── Verify no network failures
   └── GATE: No critical issues

5. BUILD
   ├── Run: npm run build
   └── GATE: Must succeed

6. REPORT
   └── Summary of all layers
```

### Quick Mode (`/verify quick`)
Only runs Layer 1 (Static Analysis).

### Visual Mode (`/verify visual`)
Only runs Layer 5 (Visual Verification) using Playwright MCP.

### Deploy Mode (`/verify deploy <url>`)

Verifies a PRODUCTION deployment is actually live and working. This closes the
"HTTP 200 ≠ working" and "pushed ≠ deployed" gap. Git push success and a 200
response from the origin do NOT mean the app is functioning.

**Required argument:** the production URL (e.g. `https://parallax.id8labs.tech`).

**Optional flags:**
- `--vercel <project>`: also query Vercel for the latest deployment timestamp
- `--cf <zone>`: also query Cloudflare for the latest deployment
- `--expect "<text>"`: assert specific text appears on the rendered page
- `--routes "/a,/b,/c"`: also check additional routes beyond root

**Process:**

1. **Server-side check** via `curl -sS -o /dev/null -w "%{http_code} %{time_total}s" <url>`
   - Status code, response time, redirects.
   - GATE: 200 (or 308→200) within 5 seconds.

2. **Client-side render check** (Playwright MCP)
   - Navigate to the URL.
   - `browser_console_messages` → check for any `error` level messages.
   - Wait for network-idle (or 3s, whichever first).
   - `browser_snapshot` → confirm the page actually rendered DOM (not a blank shell).
   - If `--expect` is set, assert that text is present.
   - For each route in `--routes`, repeat.
   - GATE: zero console errors, expected text present, DOM has > 500 chars.

3. **Deploy-platform timestamp check** (if `--vercel` or `--cf` provided)
   - Query the platform API for the latest deployment.
   - Confirm the deploy completed (state=READY for Vercel; success for CF).
   - Compare timestamp to git HEAD. Warn if origin commit is newer than deploy.
   - GATE: latest deploy is in READY state.

4. **Report**, a single PASS/FAIL with evidence:
   ```
   ╔══════════════════════════════════════════════════════════╗
   ║              DEPLOY VERIFICATION: <url>                  ║
   ╠══════════════════════════════════════════════════════════╣
   ║ Server (HTTP)         ✅ PASS  200 in 0.42s              ║
   ║ Client (rendered)     ✅ PASS  no console errors         ║
   ║ Routes (/, /login)    ✅ PASS  3/3 rendered              ║
   ║ Vercel deploy state   ✅ PASS  READY @ 2026-05-21T15:08Z ║
   ║ Git HEAD vs deploy    ✅ PASS  in sync (sha 4a9b21c)     ║
   ╠══════════════════════════════════════════════════════════╣
   ║ OVERALL: ✅ DEPLOYMENT VERIFIED                          ║
   ╚══════════════════════════════════════════════════════════╝
   ```

   On FAIL, lead with the worst signal (e.g., "console crash on hydration"),
   include the error text, and name what to check next.

**Why this exists:** Parallax went down with a client-side hydration crash
while origin returned HTTP 200 (see the Apr-May 2026 outage). The retro
flagged it; this mode prevents the recurrence. Run before claiming any
deploy is "live" or "shipped".

## Playwright MCP Integration

For visual verification, use these MCP tools:

```typescript
// 1. Start by checking if dev server is running
mcp__playwright-server__browser_navigate({ url: "http://localhost:3000" })

// 2. Capture page state
mcp__playwright-server__browser_snapshot()

// 3. Check for console errors
mcp__playwright-server__browser_console_messages({ level: "error" })

// 4. Take screenshot for visual record
mcp__playwright-server__browser_take_screenshot({ filename: "verify-{timestamp}.png" })

// 5. Check network requests
mcp__playwright-server__browser_network_requests()

// 6. Navigate to key routes and repeat
```

## Key Pages to Verify

For Next.js apps, automatically check:
- `/` - Homepage
- `/login` or `/auth` - Authentication (if exists)
- Key feature pages based on recent changes

## Error Classification

| Severity | Action |
|----------|--------|
| CRITICAL | Stop verification, report immediately |
| ERROR | Log and continue, fail at end |
| WARNING | Log and continue, pass with warnings |
| INFO | Log for reference |

## Output Format

```
╔══════════════════════════════════════════════════════════╗
║                   VERIFICATION REPORT                     ║
╠══════════════════════════════════════════════════════════╣
║ Layer 1 - Static Analysis     ✅ PASS                    ║
║   TypeScript: 0 errors                                    ║
║   ESLint: 0 errors, 2 warnings                           ║
╠══════════════════════════════════════════════════════════╣
║ Layer 2 - Unit Tests          ✅ PASS                    ║
║   42 tests passed                                         ║
║   Coverage: 78%                                           ║
╠══════════════════════════════════════════════════════════╣
║ Layer 3 - E2E Tests           ✅ PASS                    ║
║   12 specs passed                                         ║
╠══════════════════════════════════════════════════════════╣
║ Layer 4 - Visual Verification ✅ PASS                    ║
║   3 pages checked                                         ║
║   0 console errors                                        ║
║   Screenshots: verify-20240102-143022.png                ║
╠══════════════════════════════════════════════════════════╣
║ Layer 5 - Build               ✅ PASS                    ║
║   Build time: 12.3s                                       ║
╠══════════════════════════════════════════════════════════╣
║                                                           ║
║ OVERALL: ✅ VERIFICATION PASSED                          ║
║                                                           ║
╚══════════════════════════════════════════════════════════╝
```

## Integration with Other Skills

This skill works with:
- `/commit-push-pr` - Run verify before creating PR
- `/test-verify` - Subset focused on testing
- `code-reviewer` subagent - Code quality checks

## Automation Hook

Can be triggered automatically via Stop hook for long-running tasks:
```bash
# ~/.claude/hooks/stop/verify-on-complete.sh
# Runs /verify when Claude finishes a significant task
```
