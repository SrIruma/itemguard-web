# Community Addons

This document explains how community addons work and how to submit yours to the official catalog.

---

## What Are Community Addons?

Community addons are bridges/integrations created by third-party developers that extend ItemGuard's functionality. They use the free **Addon API** to integrate with ItemGuard's protection system.

Examples:
- Protection for other plugins' blocks/items
- Custom flag behaviors
- Integration with economy, shops, or RPG plugins
- Custom recovery mechanics

---

## Catalog Inclusion

Accepted addons are listed on the **Community Addons** page of the documentation site:
https://sriruma.github.io/itemguard-web/#addons

Each entry shows:
- Name, version, author
- Description
- Required plugins
- Download link (JAR)
- Link to source code

---

## Submission Process

### 1. Build Your Addon
- Use `itemguard-addon-api` as `provided` dependency
- Implement `ItemGuardIntegration`
- Register in `META-INF/services/dev.mugi.itemguard.addon.ItemGuardIntegration`
- Build JAR + Source ZIP

### 2. Test Thoroughly
- Test on Paper 1.21+ (and Folia if possible)
- Verify with and without required plugins
- Test all integration points (flags, ownership, recovery, etc.)

### 3. Open Submission Issue
Use the **Addon Submission** template on GitHub:
https://github.com/SrIruma/itemguard-web/issues/new?template=addon_submission.yml
- Fill all required fields
- Provide source code link (public repo)
- Provide direct download links (JAR + Source ZIP)
- List tested versions

### 4. Review Process
- We verify the addon works as described
- Check for malicious code or hidden functionality
- Test on a clean server
- Usually 1-3 business days

### 5. Approval & Publication
- We add the `approved` label to your issue
- Your addon JAR goes into the `addons/` folder of this repository
- It's added to the site's addon list and deployed with the next build

---

## Requirements Checklist

- [ ] Implements `ItemGuardIntegration`
- [ ] Declares service in `META-INF/services/dev.mugi.itemguard.addon.ItemGuardIntegration`
- [ ] Uses `itemguard-addon-api` as `provided` dependency
- [ ] Has unique, stable `name()` (lowercase, hyphens)
- [ ] Source code is publicly available (GitHub/GitLab)
- [ ] Provides direct download links (JAR + Source ZIP)
- [ ] Tested on Paper 1.21+ (Folia if possible)
- [ ] Documents required plugins
- [ ] No malicious code, backdoors, or data collection

---

## Guidelines

### Do
- Keep dependencies soft (use `isAvailable()` and `requiredPlugins()`)
- Report failures via `logger()` - ItemGuard will disable gracefully
- Use unique, stable `name()` values
- Document any custom placeholders or flags

### Don't
- Assume other plugins are present without checking
- Modify ItemGuard internals via reflection
- Collect user data without explicit consent
- Distribute modified ItemGuard core files

---

## Support

- **Questions:** GitHub Discussions — https://github.com/SrIruma/itemguard-web/discussions
- **Bug Reports:** GitHub Issues (use the "Bug Report" template)
- **Direct Contact:** MrTsumugi@proton.me

---

## Disclaimer

ItemGuard is not responsible for community addons. They are third-party software provided "as is" without warranty. Server administrators should review addon code before installing on production servers.