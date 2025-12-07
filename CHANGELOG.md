# SPDX-License-Identifier: MIT
# Changelog

All notable changes to this project will be documented in this file.

This changelog is **automatically generated** from git tags and commit messages using `tools/generate_changelog.py`.

## [Unreleased]

- Bump to version v1.2.2 (ca12694)
- - Fix type hints and behavior of WordfreqDictionary (#25) (6e7b81c)
- - Fix type hints and behavior of WordfreqDictionary - Make WordfreqDictionary subclass DictionaryBackend so it can be used in composite backends without mypy errors. - Extend WordfreqDictionary.__init__ to accept real_word_min_zipf (used by language plugins) and expose an available flag. - Handle missing wordfreq gracefully by disabling the backend instead of failing. - Update initialization and is_real_word to fall back when zipf_frequency stubs donâ€™t accept a wordlist keyword, ensuring dictionary tests pass. (5496ea9)
- Spdx support (#23) (9937d7e)
- Added changes to account for egg-info (bfd87be)
- Added testing check for spdx in pr template. (458ce84)
- **feat(ci,spdx): integrate SPDX validation into tooling, CI, and release process** (30e77b0)
- SPDX support for all files. (f8b4298)
- Added PR and Issue Labels, fixed repo url, added code bracket types. (#22) (4b94d72)
- Added PR and Issue Labels, fixed repo url, added code bracket types. (51f3226)
- **feat: add community standards and automated PR labeling** (#21) (0564a7a)
- Modified labeler.yml layout to support newer standard. (cda069f)
- **feat: add community standards and automated PR labeling** (16be50b)
- Updated Platforms (#20) (3a3be77)
- Updated Platforms - Notes for MacOS, not support, should work, but... I has no mac to test or build with. - Updated badges too reflect that. (395178d)
- chore(ci, metadata): update release workflow and expand project metadata (#19) (6a34225)
- chore(ci, metadata): update release workflow and expand project metadata (7f43839)
- Modified permissions of ci.yml to follow the rule of "least privilege" (#18) (1f00139)
- Modified permissions of ci.yml to follow the rule of "least privilege" (1fa70ab)

---

## [v1.2.1]

- Update changelog for v1.2.1 (399ee5e)
- Bump to version 1.2.1 (7ecbdca)
- Better docs (#16) (b12bbb7)

## [v1.2.0]

- Bump (451871e)
- Error handling (#15) (10966f3)

## [v1.1.2]

- Badges fun (#13) (eeaeb82)
- Packaging zip (#12) (b95c8ff)

## [v1.1.1]

- Version Bump (49b9dff)
- Fixes (#11) (e527f3b)

## [v1.1.0]

- Automation attempts. (#10) (0052f3c)
- Src migration 2 (#9) (fb4fadd)
- Moved the package directory: nonwordgen/ â†’ src/nonwordgen/. (#8) (c99be19)
- Attempted to get ALL files to pull version from single source of truth. (#7) (b1c0aea)
- Nox automation testing (#6) (3b75e8b)
- Binary dictionary fix (#5) (b54c1c2)
- Binary dictionary fix (#4) (b7bd926)
- Enhance README with detailed project information (#2) (ec106fe)
- Binary builder (#1) (8fbb8ff)

## [v1.0.1]

- version bump, minor changes, and setting default language. (0cd479f)
- Attempt to detect default language with English as default. (fb93bc4)
- Added libraries to build windows executable, included third party notifications including for PyQt6. Added links to source repo. (df3a8d6)

## [v1.0.0]

- Removed Depriciated calls in toml file. (0faaebe)
- Updated description a bit to make it more user friendly. (69ce820)
- Added notification for users. (2565c61)
- Notes to me for development build process cycles. (8c78941)
- Resized icon in help. (db4b273)
- Added icon and help. (c3eb4c3)
- Added copyright and license informatin. (20e635f)
- Malay (ish) (7a1a12c)
- Serbian / Croatian / Bosnian (SCB) (964cc81)
- Hebrew (ish) (62cfe26)
- Thai (ish) (7091adf)
- Greek (ish) (53236db)
- Hungarian (ish) (fc9dafb)
- Czech (ish) (66b4e37)
- Polish (ish) (6d4abae)
- Yoruba (ish) (07a0413)
- Afrikaans (ish) (c4f4dea)
- Danish (ish) (253c7f7)
- Norwegian (ish) (2c1df51)
- Swedish (ish) (93ff4c2)
- Romanian (ish) (ef1ab43)
- Filipino / Tagalog (ish) (bf95f88)
- Dutch (c90f28b)
- Itallian(ish) (1293df6)
- Added Gui! (a162346)
- Korean(ish) (48a5c25)
- Hindi/Marathi (1b884d7)
- Vietnamese(ish) (b1a6df1)
- Russian(ish) (139dd81)
- Turkish(ish) (17ac014)
- Updates to include full charsets and dictionaries. (70e5213)
- German(ish) (d3a5902)
- Swahili(ish) (2ac7c8a)
- Indonesian(ish) (af8f4d9)
- Portuguese(ish) (452852e)
- Added French-ish words (52b94c2)
- Added spanish-ish options (1ed9342)
- Created plugin structure for multilingual nonword generation. (0727b41)
- First run. (332fc87)
