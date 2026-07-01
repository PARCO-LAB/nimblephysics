# Refactor Plan

This file is an ordered checklist for agents performing the repo cleanup from the ponytail audit. Do the steps in order. Keep each step in its own commit when practical, because most steps are independent and easy to review.

Rules for every step:

1. Start by checking the worktree with `rtk git status --short`. If `rtk` is unavailable, use `git status --short`.
2. Do not overwrite unrelated user changes. If a target file is already edited, inspect it first and preserve unrelated changes.
3. Prefer deletion and existing tooling over replacement code.
4. After each step, run the smallest relevant verification listed in that step.
5. If a step removes public files, confirm no source, tests, docs, package manifests, or CI jobs still reference them.

## 1. Record The Baseline

Goal: make later cleanup failures easy to attribute.

Actions:

1. Capture current branch and dirty files:
   ```bash
   rtk git status --short
   rtk git branch --show-current
   ```
2. Record current source counts and heavy directories:
   ```bash
   rtk find . -maxdepth 2 -type d
   du -sh data javascript/src/data python/research www/old_docs stubs javascript/src/threejs_lib 2>/dev/null
   ```
3. Run the cheapest existing checks that work in the current environment:
   ```bash
   rtk pytest python/tests/unit
   ```
   If the native extension is not built, record that and continue. Do not spend time building the whole physics engine just to start a deletion PR.

Verification:

1. A later agent can compare failures against this baseline.
2. No files changed in this step unless you intentionally write a short baseline note in the PR description.

## 2. Remove Checked-In JS Recording Fixtures

Goal: remove the biggest low-risk source weight first.

Target:

1. `javascript/src/data/movement.bin`
2. `javascript/src/data/test.bin`
3. `javascript/src/data/cartpole.txt`
4. `javascript/src/data/realtime.txt`
5. `javascript/src/data/worm.txt`
6. Keep `javascript/src/data/preview.json` for now because `javascript/src/screenshot.ts` imports it.
7. Keep `javascript/src/data/.gitignore` and `javascript/src/data/.npmignore`.

Actions:

1. Confirm references:
   ```bash
   rg -n "movement\.bin|test\.bin|cartpole\.txt|realtime\.txt|worm\.txt|preview\.json" javascript
   ```
2. Delete only files with no live import or documented packaging need.
3. Update `javascript/src/data/.gitignore` so generated recordings stay local:
   ```gitignore
   *.bin
   *.bin.gz
   *.txt
   !.gitignore
   !.npmignore
   !preview.json
   ```
4. If a deleted fixture is referenced only by a dev demo, change that demo to load a user-provided URL or `preview.json`.

Verification:

1. `rg -n "movement\.bin|test\.bin|cartpole\.txt|realtime\.txt|worm\.txt" javascript` returns no live references.
2. `npm run build-for-python` from `javascript/` still succeeds, or any pre-existing failure is documented.

## 3. Remove Or Move `python/research`

Goal: keep package source and tests, not personal experiments.

Target:

1. `python/research/marker_fit`
2. `python/research/mujoco_loader`
3. `python/research/sprinter_fit`
4. `python/research/synthetic_joint_recovery`

Actions:

1. Confirm all references outside `python/research`:
   ```bash
   rg -n "python/research|research/|synthetic_joint_recovery|synthetic_recovery|sprinter_fit|marker_fit" . \
     -g '!python/research/**' \
     -g '!build/**' \
     -g '!dist/**'
   ```
2. If tests reference research fixtures, move only the required fixtures to `data/test/...` and update those tests. Do not keep the whole research tree for a few fixtures.
3. Delete the remaining research files.
4. Add `python/research/` to `.gitignore` if local experiments are still common.

Verification:

1. The reference search above returns only intentional docs or updated test fixture paths.
2. Any touched tests still pass, or native-build preconditions are documented.

## 4. Replace Vendored Three.js Examples

Goal: stop vendoring `three` examples while already depending on `three`.

Target:

1. `javascript/src/threejs_lib`
2. Imports in:
   - `javascript/src/components/View.ts`
   - `javascript/src/NimbleView.ts`

Actions:

1. List current local imports:
   ```bash
   rg -n "threejs_lib" javascript/src
   ```
2. Replace standard Three.js example imports with package imports:
   ```ts
   import { EffectComposer } from "three/examples/jsm/postprocessing/EffectComposer.js";
   import { SSAOPass } from "three/examples/jsm/postprocessing/SSAOPass.js";
   import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
   ```
3. For `CapsuleBufferGeometry`, first check whether the installed `three` version already provides an equivalent in examples. If not, keep only `CapsuleBufferGeometry` in a small local file under `javascript/src/geometry/`.
4. Delete `javascript/src/threejs_lib` after imports are gone.
5. Do not upgrade `three` in this step. Dependency upgrades are a separate risk.

Verification:

1. `rg -n "threejs_lib" javascript/src` returns nothing.
2. `npm run build` and `npm run build-for-python` from `javascript/` compile.
3. The visualizer still loads a simple recording or `preview.json`.

## 5. Stop Tracking Generated Pybind Stubs

Goal: remove generated stub trees from source while keeping stub generation in the build.

Target:

1. `stubs/_nimblephysics`
2. `stubs/_nimblephysics-stubs`
3. `generate_pyi_stubs.sh`
4. Stub-copying block in `setup.py`

Actions:

1. Confirm the build script still generates stubs:
   ```bash
   sed -n '1,220p' generate_pyi_stubs.sh
   rg -n "generate_pyi_stubs|stubs/_nimblephysics" setup.py MANIFEST.in pyproject.toml .gitignore
   ```
2. Delete tracked generated stubs.
3. Add generated stub outputs to `.gitignore`:
   ```gitignore
   stubs/_nimblephysics/
   stubs/_nimblephysics-stubs/
   ```
4. Keep `generate_pyi_stubs.sh`.
5. Keep the `setup.py` copy step only if the wheel needs generated `.pyi` files inside `nimblephysics_libs`. If the copy step is kept, make sure build failure is explicit when stub generation fails.
6. Fix the repeated `nimblephysics_libs.nimblephysics_libs...` path rewrite in `generate_pyi_stubs.sh` if it still appears after regeneration.

Verification:

1. A local build regenerates stubs.
2. The generated wheel still contains usable `.pyi` files and `py.typed` if typed distribution is intended.
3. `git status --short` does not show generated stubs after a build.

## 6. Delete Old Docs

Goal: keep one docs tree.

Target:

1. `www/old_docs`
2. Any links pointing at `old_docs`

Actions:

1. Confirm references:
   ```bash
   rg -n "old_docs|www/old_docs" README.md www .github ci CMakeLists.txt
   ```
2. Move any still-useful source `.rst` content into `www/docs` only if current docs lack it and it is still accurate.
3. Delete `www/old_docs`.

Verification:

1. `rg -n "old_docs|www/old_docs" . -g '!build/**' -g '!dist/**'` returns nothing.
2. Current docs build or static docs check still works if the repo has one.

## 7. Use One JavaScript Lockfile

Goal: avoid split npm/yarn dependency state.

Target:

1. `javascript/yarn.lock`
2. `javascript/package-lock.json`
3. `javascript/README.md`

Actions:

1. Keep `package-lock.json` because scripts and docs use npm.
2. Delete `javascript/yarn.lock`.
3. Update docs that mention yarn, if any, to npm.
4. Add a short package-manager note to `javascript/README.md` if helpful:
   ```md
   Use npm. Do not commit yarn.lock.
   ```

Verification:

1. `npm ci` from `javascript/` works.
2. `git status --short javascript/yarn.lock` shows deletion only.

## 8. Collapse Webpack Config Duplication

Goal: replace five near-identical configs with one config plus env switches.

Target:

1. `javascript/webpack.config.js`
2. `javascript/webpack.config.python.js`
3. `javascript/webpack.config.devserver.js`
4. `javascript/webpack.config.devserver-python.js`
5. `javascript/webpack.config.devserver-screenshot.js`
6. `javascript/package.json`

Actions:

1. Create one `webpack.config.js` that exports a function:
   ```js
   module.exports = (_env = {}, argv = {}) => {
     const target = _env.target || "package";
     // choose entries, externals, devServer, and mode from target
   };
   ```
2. Preserve existing entry sets:
   - `package`: `NimbleStandaloneReact`, `NimbleStandalone`, `NimbleRemote`
   - `python`: `live`, `embeddable`
   - `dev`: `embedded_dev`, `NimbleStandaloneReact`, `NimbleStandalone`, `NimbleRemote`
   - `dev-python`: `live`, `NimbleStandaloneReact`, `NimbleStandalone`, `NimbleRemote`
   - `dev-screenshot`: `screenshot`, `NimbleStandaloneReact`, `NimbleStandalone`, `NimbleRemote`
3. Update scripts:
   ```json
   {
     "dev": "webpack-dev-server --env target=dev",
     "dev-python": "webpack-dev-server --env target=dev-python",
     "dev-screenshot": "webpack-dev-server --env target=dev-screenshot",
     "prod": "webpack --mode=production --env target=package",
     "build-for-python": "webpack --env target=python"
   }
   ```
4. Delete the four extra webpack config files.

Verification:

1. `npm run build`
2. `npm run build-for-python`
3. One dev-server command starts without config errors.

## 9. Replace Webpack Loader Dependencies With Asset Modules

Goal: use Webpack 5 native asset handling.

Target dependencies:

1. `raw-loader`
2. `file-loader`
3. `arraybuffer-loader`

Actions:

1. Replace inline imports:
   ```ts
   import playSvg from "!!raw-loader!./play.svg";
   ```
   with normal imports:
   ```ts
   import playSvg from "./play.svg";
   ```
2. Add webpack rules:
   ```js
   { test: /\.svg$/i, type: "asset/source" },
   { test: /\.(bin|gz)$/i, type: "asset/resource" },
   { test: /\.txt$/i, type: "asset/source" }
   ```
3. Remove the loader dependencies from `javascript/package.json`.
4. Regenerate `package-lock.json` with `npm install --package-lock-only` or `npm install`.

Verification:

1. `npm run build`
2. `npm run build-for-python`
3. SVG icons still render in the player.

## 10. Delete Small Unused JavaScript Dependencies

Goal: remove dependency clutter after the loader cleanup.

Targets:

1. `path` in `javascript/package.json`
2. `declaration-bundler-webpack-plugin` in `javascript/package.json`
3. `sha256-uint8array` in `javascript/package.json`
4. `DeclarationBundlerPlugin` imports in webpack configs
5. `createHash`, `lastRecordingHash`, and related unused hash code in `javascript/src/NimbleStandalone.ts`

Actions:

1. Confirm each symbol is unused:
   ```bash
   rg -n "DeclarationBundlerPlugin|declaration-bundler|sha256-uint8array|createHash|lastRecordingHash|from ['\"]path|require\\(['\"]path" javascript
   ```
2. Remove unused imports, fields, and dependencies.
3. Keep Node's built-in `require("path")` in webpack config. Remove only the npm package dependency named `path`.
4. Regenerate `package-lock.json`.

Verification:

1. The search above returns only intended built-in `require("path")`.
2. `npm ci` and `npm run build` work.

## 11. Replace Local Boost Usage With C++17 Standard Library

Goal: remove Boost from core code where C++17 already covers the need.

Target local Boost uses:

1. `boost::filesystem` in:
   - `dart/common/SharedLibrary.*`
   - `dart/common/detail/SharedLibraryManager.*`
   - `dart/server/GUIStateMachine.cpp`
   - `dart/server/GUIWebsocketServer.cpp`
2. `boost::regex` fallback in `dart/common/Uri.cpp`
3. `boost::lexical_cast`, `boost::trim_copy`, and `boost::split` in `dart/utils/XmlHelpers.cpp`
4. Boost link setup in:
   - `cmake/DARTFindBoost.cmake`
   - `dart/CMakeLists.txt`
   - `CMakeLists.txt`

Actions:

1. Replace filesystem:
   ```cpp
   #include <filesystem>
   namespace fs = std::filesystem;
   ```
   Use `fs::path`, `fs::exists`, and `fs::canonical`.
2. Replace `std::hash<boost::filesystem::path>` specialization with the standard hash for `std::filesystem::path`, or store canonical path strings as map keys.
3. Replace `boost::regex` fallback in `Uri.cpp` with `std::regex`; this project already requires C++17.
4. Replace scalar `boost::lexical_cast` with:
   - `std::to_string` for simple numeric `toString`
   - `std::ostringstream` when formatting Eigen values
   - `std::stoi`, `std::stoul`, `std::stof`, `std::stod`
   - `str.at(0)` or stream extraction for char, matching existing behavior as closely as possible
5. Replace `boost::trim_copy` and `boost::split` with a tiny local helper in `XmlHelpers.cpp`:
   ```cpp
   static std::vector<std::string> splitWhitespace(const std::string& value)
   {
     std::istringstream input(value);
     std::vector<std::string> out;
     std::string token;
     while (input >> token)
       out.push_back(token);
     return out;
   }
   ```
6. Remove `Boost::regex`, `Boost::filesystem`, and `Boost::system` links if no remaining local source requires them.
7. Keep any vendored third-party code untouched unless it is the only remaining Boost dependency and is no longer used.

Verification:

1. `rg -n "boost::|<boost/" dart cmake CMakeLists.txt -g '!dart/server/external/**' -g '!dart/external/**'` returns nothing or only intentional third-party code.
2. CMake configure succeeds.
3. Native build reaches at least the same point as the baseline.

## 12. Remove The Single-Product Collision Factory

Goal: delete generic factory machinery if `"dart"` is the only collision detector implementation.

Target:

1. `dart/common/Factory.hpp`
2. `dart/common/detail/Factory-impl.hpp`
3. `dart/collision/CollisionDetector.hpp`
4. `dart/collision/CollisionDetector.cpp`
5. `dart/collision/dart/DARTCollisionDetector.cpp`
6. `dart/utils/SkelParser.cpp`

Actions:

1. Confirm registered implementations:
   ```bash
   rg -n "CollisionDetector::Registrar|registerCreator|getFactory\\(\\)->create|CollisionDetector::getFactory" dart
   ```
2. If only `DARTCollisionDetector` is registered, delete the registrar and factory path.
3. Replace:
   ```cpp
   collision::CollisionDetector::getFactory()->create(cdType)
   ```
   with explicit handling:
   ```cpp
   if (cdType.empty() || cdType == "dart")
     collisionDetector = collision::DARTCollisionDetector::create();
   else
     warn or fall back exactly as current behavior does;
   ```
4. Delete `common::Factory` only if no other code uses it. If other code still uses it, leave it.
5. Keep public behavior for unknown collision detector strings. Do not silently accept a value that used to warn.

Verification:

1. `rg -n "common::Factory|FactoryRegistrar|CollisionDetector::getFactory|getFactory\\(\\)->create" dart` shows no stale collision factory path.
2. Skeleton parsing still handles missing or `"dart"` collision detector config.
3. Collision unit tests compile.

## 13. Use CMake's Python3 Discovery

Goal: remove subprocess-based `distutils` Python probing.

Target:

1. `python/_nimblephysics/CMakeLists.txt`
2. `setup.py` CMake arguments if they duplicate Python discovery

Actions:

1. Replace manual `find_program(PYTHON_EXECUTABLE ...)` and `execute_process(...distutils...)` with:
   ```cmake
   find_package(Python3 ${DARTPY_PYTHON_VERSION} COMPONENTS Interpreter Development REQUIRED)
   ```
2. Use:
   ```cmake
   ${Python3_EXECUTABLE}
   ${Python3_INCLUDE_DIRS}
   ${Python3_LIBRARIES}
   ```
3. Keep `DARTPY_PYTHON_VERSION` override support from `setup.py`.
4. Remove commented-out old Python discovery blocks while touching the file.
5. Do not change pybind11 version requirements in this step.

Verification:

1. CMake configure finds the active Python from the build environment.
2. Python extension build still receives the expected include and library paths.
3. macOS special casing is gone unless a real build failure proves it is needed.

## 14. Delete Dead CMake Filesystem Probe

Goal: remove an unused configure-time command that calls a missing tool.

Target:

1. The `FILESYSTEM_CASE_SENSITIVE` block in top-level `CMakeLists.txt`.

Actions:

1. Delete this block:
   ```cmake
   execute_process(COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/tools/case_sensitive_filesystem
     RESULT_VARIABLE FILESYSTEM_CASE_SENSITIVE_RETURN)
   ...
   ```
2. Do not add a replacement unless a live source reads `FILESYSTEM_CASE_SENSITIVE`.

Verification:

1. `rg -n "FILESYSTEM_CASE_SENSITIVE|case_sensitive_filesystem" . -g '!build/**' -g '!dist/**'` returns nothing.
2. CMake configure no longer reports an error or warning for the missing tool.

## 15. Remove Python Build Artifacts From Source

Goal: clean generated Python metadata and bytecode.

Target:

1. `python/nimblephysics.egg-info`
2. `python/**/__pycache__`
3. `*.pyc`
4. `python/nimblephysics_libs` if it is generated in the local worktree

Actions:

1. Confirm these are generated and not package source:
   ```bash
   git ls-files | grep -E '(egg-info|__pycache__|\\.pyc$|^python/nimblephysics_libs/)'
   ```
2. Delete tracked bytecode and egg metadata.
3. Keep `.gitignore` entries:
   ```gitignore
   python/nimblephysics_libs/
   python/**/__pycache__/
   python/*.egg-info/
   ```
4. If `python/nimblephysics_libs` contains generated stubs after a build, leave it ignored.

Verification:

1. Running tests or a build does not create tracked files.
2. `git status --short` after verification shows no generated Python artifacts except ignored files.

## 16. Final Verification

Goal: prove the repo is leaner and still builds at the same level as the baseline.

Actions:

1. Run searches for stale references:
   ```bash
   rg -n "old_docs|threejs_lib|yarn.lock|movement\\.bin|test\\.bin|python/research|FILESYSTEM_CASE_SENSITIVE" . \
     -g '!build/**' \
     -g '!dist/**'
   ```
2. Run package checks:
   ```bash
   cd javascript && npm ci && npm run build && npm run build-for-python
   ```
3. Run Python tests that do not require a fresh native build:
   ```bash
   rtk pytest python/tests/unit
   ```
4. Run CMake configure and the smallest native compile target available in the environment:
   ```bash
   cmake -S . -B build/refactor-check
   cmake --build build/refactor-check --target _nimblephysics -j2
   ```
5. Measure the cut:
   ```bash
   git diff --stat
   git ls-files | wc -l
   du -sh javascript/src/data python/research www/old_docs stubs javascript/src/threejs_lib 2>/dev/null
   ```

Done criteria:

1. Generated files are ignored, not tracked.
2. No stale references to deleted trees remain.
3. JS builds pass.
4. Native/Python checks pass or fail only for documented baseline reasons.
5. The final PR summary lists line count removed, dependency count removed, and any intentionally deferred cleanup.
