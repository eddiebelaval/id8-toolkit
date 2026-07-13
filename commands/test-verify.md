# Test and Verify

You are executing the **test-verify** workflow - runs tests and verifies the application works.

## Pre-computed Context

```bash
# Detect project type and test framework
HAS_PACKAGE_JSON=$(test -f package.json && echo "yes" || echo "no")
TEST_SCRIPT=$(cat package.json 2>/dev/null | jq -r '.scripts.test // "none"')
TYPECHECK_SCRIPT=$(cat package.json 2>/dev/null | jq -r '.scripts["type-check"] // .scripts.typecheck // "none"')
LINT_SCRIPT=$(cat package.json 2>/dev/null | jq -r '.scripts.lint // "none"')
BUILD_SCRIPT=$(cat package.json 2>/dev/null | jq -r '.scripts.build // "none"')
HAS_PLAYWRIGHT=$(test -f playwright.config.ts && echo "yes" || echo "no")
HAS_VITEST=$(grep -q "vitest" package.json 2>/dev/null && echo "yes" || echo "no")
HAS_JEST=$(grep -q "jest" package.json 2>/dev/null && echo "yes" || echo "no")
```

**Package.json:** $HAS_PACKAGE_JSON
**Test Script:** $TEST_SCRIPT
**Type Check:** $TYPECHECK_SCRIPT
**Lint Script:** $LINT_SCRIPT
**Build Script:** $BUILD_SCRIPT
**Has Playwright:** $HAS_PLAYWRIGHT
**Has Vitest:** $HAS_VITEST
**Has Jest:** $HAS_JEST

## User Intent

$ARGUMENTS

## Full Verification Workflow

### Phase 1: Static Analysis
Run in parallel where possible:

1. **Type Check** (if TypeScript project)
```bash
npm run type-check || npx tsc --noEmit
```

2. **Lint Check**
```bash
npm run lint
```

### Phase 2: Unit/Integration Tests
```bash
npm test
```

If specific test file requested in $ARGUMENTS:
```bash
npm test -- [file-pattern]
```

### Phase 3: E2E Tests (if Playwright exists)
```bash
npx playwright test
```

For specific test:
```bash
npx playwright test [test-name]
```

### Phase 4: Build Verification
```bash
npm run build
```

### Phase 5: Visual Verification (if requested or if UI changes)
Use Playwright MCP to:
1. Start dev server if not running
2. Navigate to relevant pages
3. Take screenshots
4. Verify UI renders correctly

## Reporting

After each phase, report:
```
Phase 1 (Static Analysis): PASS/FAIL
  - TypeScript: X errors
  - ESLint: X warnings, X errors

Phase 2 (Tests): PASS/FAIL
  - X tests passed
  - X tests failed
  - X tests skipped

Phase 3 (E2E): PASS/FAIL (if applicable)
  - X specs passed

Phase 4 (Build): PASS/FAIL
  - Build time: Xs

Overall: PASS/FAIL
```

## Quick Modes

If $ARGUMENTS contains:
- "quick" or "fast": Only run type-check + lint (skip tests)
- "unit": Only run unit tests
- "e2e": Only run Playwright tests
- "build": Only verify build
- "all" or empty: Full verification

## Error Handling

On failure:
1. Capture full error output
2. Identify the failing test/check
3. Show relevant code context
4. Suggest fix if obvious

Do NOT proceed to later phases if earlier phases fail (unless user says "continue anyway").

## Integration with Playwright MCP

For visual verification:
```
1. browser_navigate to localhost:3000 (or dev server URL)
2. browser_snapshot to capture page state
3. browser_take_screenshot for visual record
4. Compare with expected behavior
```
