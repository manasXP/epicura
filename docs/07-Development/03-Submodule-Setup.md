# Docs Submodule Setup

The `epicura` repository (this docs repo) is linked as a Git submodule in every other Epicura repository. This gives developers access to the full documentation while working on any part of the system.

## Repository Layout (with submodule)

```
epicura-firmware/          # or any other repo
├── docs/                  # ← git submodule → epicura repo
│   ├── 01-Overview/
│   ├── 02-Hardware/
│   ├── ...
│   └── README.md
├── src/
├── .gitignore
└── .gitmodules
```

## Repositories That Include the Submodule

| Repository | Stack | Submodule Path |
|-----------|-------|----------------|
| `epicura-firmware` | C / STM32 / FreeRTOS | `docs/` |
| `epicura-cm5` | Python / Docker / Yocto | `docs/` |
| `epicura-api` | TypeScript / Node / Next.js | `docs/` |
| `epicura-ios` | Swift / Xcode | `docs/` |
| `epicura-android` | Kotlin / Gradle | `docs/` |

## Adding the Submodule (when scaffolding a new repo)

Run the helper script from the new repo's root:

```bash
# From inside the new repo (e.g. epicura-firmware/)
../epicura/scripts/add-docs-submodule.sh
```

Or manually:

```bash
git submodule add git@github.com:manasXP/epicura.git docs
git commit -m "Add epicura docs as submodule"
```

## Cloning a Repo with the Submodule

New contributors must initialize the submodule after cloning:

```bash
git clone --recurse-submodules git@github.com:manasXP/epicura-firmware.git

# Or if already cloned without --recurse-submodules:
git submodule update --init
```

## Updating the Docs Submodule

When the docs repo is updated, pull the latest in each repo:

```bash
cd docs
git pull origin main
cd ..
git add docs
git commit -m "Update docs submodule"
```

Or from the parent repo:

```bash
git submodule update --remote docs
git add docs
git commit -m "Update docs submodule"
```

## Notes

- The submodule points to the `main` branch of `epicura` by default.
- The `docs/` path is in each repo's `.gitignore` template under build artifacts — **remove the `docs/` entry** if present, since it's now a tracked submodule.
- Submodule changes are committed as pointer updates in the parent repo (a SHA reference, not the files themselves).
