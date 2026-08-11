# Public Repository Release Plan

## Scope

Publish both tools from the original project: the native PySide6 TCP animation window and the offline browser trajectory viewer. Include only source, vendored runtime assets, synthetic demo data, tests, documentation, CI, and MIT licensing. Exclude all recorded factory CSV files.

## Verification

1. Run all repository tests with the synthetic fixtures.
2. Load `examples/demo_episode.csv` through the desktop parser and confirm both arms.
3. Inspect the staged file list and search for recording filenames or factory paths.
4. Commit the intentional public files and push the initial `main` branch.
