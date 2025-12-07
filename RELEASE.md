# 🚀 RELEASE.md

**How to Create and Publish a New Release of nonword-gen**

This document explains the full release process for **nonword-gen**.
It is intentionally written with clarity and low cognitive load so that future maintainers can follow it without guessing.

There are **two distinct types of “release” tasks**:

1. **Packaging** → builds the Windows EXE and bundles files  
2. **Publishing** → updates the changelog, creates a git tag, and pushes the release to GitHub

These are separate steps by design.

---

# 1️⃣ Preparing a Release

Before publishing a new release, make sure you’ve done the following:

1. **Update version** in `pyproject.toml` under:

   ```toml
   [project]
   version = "X.Y.Z"
   ```

2. **Ensure all SPDX headers are present**

   Run:

   ```bash
   nox -s spdx
   ```

   If this fails, fix it by running:

   ```bash
   nox -s spdx -- add
   ```

   SPDX header compliance is required for all releases and enforced by CI.

3. **Commit all your changes**, including the version bump:

   ```bash
   git add .
   git commit -m "Bump version to X.Y.Z"
   ```

4. Ensure working tree is clean:

   ```bash
   git status
   ```

If there are uncommitted files, the release script will refuse to run.

---

# 2️⃣ Publishing a Release (creates tag + pushes to GitHub)

This step is automated.

To create and publish a release (tag, changelog, push), run:

```bash
nox -s publish_release -- X.Y.Z
```

Or with a leading `v`:

```bash
nox -s publish_release -- vX.Y.Z
```

This command performs:

* Regenerates `CHANGELOG.md`
* Commits the updated changelog (if changed)
* Verifies the version matches `pyproject.toml`
* Verifies SPDX compliance if CI has not already done so
* Creates a git tag (`vX.Y.Z`)
* Pushes the current branch & tag to GitHub

Once the tag is pushed, **GitHub Actions automatically builds release artifacts**.

You do **not** need to manually create a Release on GitHub – the workflow handles it.

---

# 3️⃣ Packaging a Release (build artifacts)

This step is handled by GitHub Actions when a tag is pushed.

But you *can* build the Windows EXE locally if you need to test it:

```bash
nox -s bundle_release
```

This will:

* Build the Windows executable
* Create the versioned release directory
* Bundle files into a ZIP archive
* Generate a SHA-256 checksum

Most contributors will never need to run this manually.

---

# 4️⃣ What Happens in CI (GitHub Actions)

When you push a tag that matches:

```text
v*.*.*
```

GitHub Actions automatically:

1. Runs SPDX header validation (`nox -s spdx`)
2. Runs tests, linting, typechecking
3. Builds the Python packages (sdist/wheel)
4. Regenerates `CHANGELOG.md` inside the build environment
5. Builds the Windows EXE
6. Bundles all artifacts
7. Creates or updates a GitHub Release and uploads everything

If the SPDX check fails, the release will not proceed.

**No manual steps needed.**

---

# 5️⃣ Notes About Maintenance & Energy Levels

This project is maintained by **one person**, and availability may vary.
The release process has been intentionally automated so that:

* You don’t need to manually edit changelogs
* You don’t need to manually create tags
* You don’t need to remember cryptic steps
* You can perform a release with a single predictable command
* CI does all the building for you

If you return to this project after months away, don’t worry – just follow this file.

---

# 6️⃣ Full Example Workflow

Assume you want to release version `0.5.0`.

```bash
# Step 1: Update version
edit pyproject.toml → version = "0.5.0"

# Step 2: Check SPDX compliance
nox -s spdx

# Step 3: Commit
git add pyproject.toml
git commit -m "Bump version to 0.5.0"

# Step 4: Publish the release (tag + changelog + push)
nox -s publish_release -- 0.5.0
```

GitHub Actions now builds everything and publishes the release.

You are done. 🎉

---

# 7️⃣ Troubleshooting

### ❌ Error: SPDX validation failed

Run:

```bash
nox -s spdx -- add
git add .
git commit -m "Add missing SPDX headers"
```

### ❌ Error: working tree not clean

Commit or stash your changes.

### ❌ Error: version mismatch

You ran `publish_release` with a version that isn’t in `pyproject.toml`.

### ❌ Error: tag already exists

You attempted to re-release a version that already has a tag.
Use a new version number.

### ✔ I pushed the tag but no release appeared

Check Actions – if the workflow failed early, you may need to fix the issue and push the tag again (deleting old tags if necessary).

---

# 8️⃣ File Overview

| File                            | Purpose                                   |
| ------------------------------- | ----------------------------------------- |
| `tools/make_release.py`         | Automates changelog → commit → tag → push |
| `tools/generate_changelog.py`   | Builds `CHANGELOG.md` from git history    |
| `nox -s publish_release`        | Wrapper for the release script            |
| `nox -s bundle_release`         | Builds Windows EXE + ZIP bundle           |
| `nox -s spdx`                   | Validates required SPDX headers           |
| `.github/workflows/release.yml` | CI pipeline that builds artifacts on tags |

---

# 9️⃣ SPDX Requirements (New Section)

To ensure transparent and consistent licensing, every source file in this repository must include:

```text
# SPDX-License-Identifier: MIT
```

This applies to:

* All Python files under `src/`
* All scripts under `tools/`
* Any other text-based source files (YAML, TOML, Markdown, etc.)

You can validate or automatically add missing headers using:

```bash
nox -s spdx
nox -s spdx -- add
```

SPDX compliance is enforced in CI for every branch and for all tagged releases.
