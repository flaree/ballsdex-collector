# Changelog

All notable changes to the Collector package are documented here.

---

## 0.0.2 — 2026-05-05

### Changed

- **Specials are now resolved by foreign key** instead of by name. `source_special` and `award_special` fields on `CollectorType` are proper `ForeignKey` references to the `Special` model, making lookups more reliable and consistent with how BallsDex handles specials elsewhere.

### Fixed

- Fixed broken `.alist()` calls in `cog.py` that prevented async querysets from resolving correctly (contributed by [@dormieriancitizen](https://github.com/dormieriancitizen)).

---

## 0.0.1 — 2026-05-05

Initial release.

### Added

- `CollectorType` Django model with configurable `min`, `max`, `gap`, `rarity_min`, `rarity_max`, `source_special`, and `enabled` fields.
- Dynamic `/claim <name> <ball>` slash commands registered at bot startup — one sub-command per enabled `CollectorType`.
- Rarity-scaled threshold calculation: required ball count is linearly interpolated between `min` and `max` based on the ball's rarity, then rounded to the nearest `gap`.
- Optional `source_special` filter — only ball instances carrying the specified special count toward the threshold.
- 24-hour background revocation loop that removes collector balls from players who no longer meet the threshold.
- Django admin registration for `CollectorType` with list display, filters, and autocomplete for special fields.
