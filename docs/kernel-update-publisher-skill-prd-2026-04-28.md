# PRD: Kernel Update Publisher Skill

Date: 2026-04-28

Status: implemented - optional publishing workflow documented

Last updated: 2026-05-11

## Purpose

Create a Codex skill that lets an operator publish article and Telegram updates
about the current `agent-engineering-kernel` GitHub project through the existing
`dudarik.com` article and Telegram system, while explicitly preventing the work
from entering the `yotubol` media pipeline.

The skill must support two modes:

- first run: create and publish the initial article about
  `alexxety/agent-engineering-kernel`;
- later runs: check meaningful GitHub updates and publish an incremental article
  update plus Telegram notification only when there is substantive change.

## GitHub Issues

- Epic: not created yet
- Task: #46

Implementation status as of 2026-05-11:

- the local Codex skill exists at `~/.codex/skills/publish-kernel-update/`;
- the skill validates with `quick_validate.py`;
- article publication, dudarik content mutation, and production Telegram sends
  are not part of this completed slice and should happen only after a separate
  explicit operator request.

## User Requirements

The operator request is:

- target GitHub repository: `alexxety/agent-engineering-kernel`;
- use the existing `~/Work/Vs/g3/dudarik.com` article and Telegram publication
  system;
- create an article and Telegram notification;
- use a GitHub-sourced image/card for Telegram;
- do not generate media;
- do not create infographic media;
- do not create audio;
- do not create video;
- do not upload to YouTube;
- do not involve NotebookLM or any laptop/media generation path;
- do not enqueue the article into `yotubol`;
- on later launches, report only meaningful project updates.

## Definitions

`Kernel project`
: The current repository, `~/Work/Vs/agent-engineering-kernel`, remote
  `https://github.com/alexxety/agent-engineering-kernel.git`.

`Dudarik`
: The content system in `~/Work/Vs/g3/dudarik.com`.

`Fast line`
: The existing dudarik article + Telegram route the operator wants to reuse.
  In implementation terms this means the `dudarik.com` article generation,
  content, deployment, and Telegram post path, not the `yotubol` media pack.

`Media pack`
: Any `yotubol`/NotebookLM/audio/infographic/video/YouTube path. This PRD
  treats the entire media pack as out of scope and forbidden for this skill.

## Current State

### Kernel repository

Verified local facts:

- path: `~/Work/Vs/agent-engineering-kernel`;
- remote: `alexxety/agent-engineering-kernel`;
- current repo already follows PRD-first engineering conventions;
- current docs live under `docs/*-prd-YYYY-MM-DD.md`;
- this PRD is a design document for a new operator skill, not an implementation.

### Dudarik article creation

`dudarik.com` currently has these article lanes:

1. Automated scheduled lane:
   discovery -> approval -> generation -> publish queue -> scheduled publish.
2. Telegram urgent lane:
   manual urgent intake -> urgent workflow -> deploy/publish.
3. Manual Claude drafting lane:
   operator-local drafting state, not production runtime truth.

Relevant files:

- `scripts/generate-article.py`
- `scripts/drain-article-generation.py`
- `data/tool_candidates.yaml`
- `data/publish_queue.yaml`
- `data/manual_article_queue.yaml`
- `data/manual_article_queue_archive.yaml`
- `.github/workflows/drain-article-lane.yml`
- `.github/workflows/manual-article.yml`

`scripts/generate-article.py` supports:

- approved candidate generation through `--candidate` and topic config;
- manual generation through `--manual-url`, `--manual-title`,
  `--manual-topic`, and related manual flags;
- source metadata injection through `apply_source_reference_metadata()`;
- GitHub README fetch for GitHub-backed articles;
- `update_policy: tracked-repo` for GitHub-backed generated articles;
- `publish_policy: scheduled` for normal approved articles;
- `publish_policy: immediate` for manual urgent articles.

### GitHub image handling

`scripts/lib/source_media.py` already resolves GitHub repository images:

- first it tries page metadata / OpenGraph image;
- if needed it falls back to:
  `https://opengraph.githubassets.com/dudarik/<owner>/<repo>`.

For this project, the fallback image is:

```text
https://opengraph.githubassets.com/dudarik/alexxety/agent-engineering-kernel
```

The skill must not generate, edit, localize, or upload a new image.

### Telegram publishing

`scripts/telegram-publish.py` is the Telegram publication surface.

Relevant behavior:

- `sync` builds queues from Hugo content;
- `post-slug --slug <slug> --lang all` publishes one article to RU and EN;
- production default queues live in `data/telegram_queue.yaml`;
- sandbox queues live in `data/telegram_sandbox_queue.yaml`;
- default production channels are:
  - RU: `@alexeydudarik`
  - EN: `@alexeydudarikeng`
- `send_primary_telegram_post()` publishes a photo when
  `hero_media_type: photo` and `hero_media_url` are present;
- if scheduled content lacks hero media, Telegram can resolve source media from
  `source_url` / `source_github`.

The skill should use the existing Telegram path, not a direct custom bot call,
except for reading dry-run output or workflow status.

### Article updates

`scripts/scan-updates.py` reads:

- `data/mcp_repos.yaml`;
- `data/tracked_repos.yaml`.

It writes pending findings into:

- `data/update_log.yaml`.

`scripts/update-articles.py` reads pending findings and updates existing
articles only when:

- the article slug can be resolved from repo tracking data;
- the article is not `manual_only`;
- the article has `update_policy: tracked-repo`.

It writes an incremental section:

- RU: `## Что изменилось после публикации`;
- EN: `## What's new since publication`.

It intentionally does not rewrite the full article.

Kernel Line supersedes this normal path for `agent-engineering-kernel`. The
kernel article must not be registered in `data/mcp_repos.yaml`,
`data/tracked_repos.yaml`, or `data/update_log.yaml`.

### Media and yotubol risk

The main deployment workflow contains a media enqueue step:

- `.github/workflows/deploy.yml`
- step: `Enqueue new articles in yotubol backlog`
- script: `scripts/queue-yotubol.py`

`scripts/queue-yotubol.py` enqueues newly published articles into `yotubol`.
Its payload enables:

- `generate_audio_pair: true`;
- `generate_infographic_pair: true`;
- `upload_to_youtube` according to workflow environment;
- language pair generation.

This is exactly what the operator does not want.

The existing guardrail is:

```yaml
skip_media_pack: true
```

`queue-yotubol.py` excludes articles when frontmatter has:

- `draft: true`;
- `skip_media_pack: true`;
- `manual_only: true`.

For this skill, `skip_media_pack: true` is mandatory on every generated or
updated `agent-engineering-kernel` article variant.

## Problem

An agent can easily reuse the visible article and Telegram commands but miss the
hidden deployment side effect: a normal published article push can automatically
enter `yotubol`, which would create the audio/infographic/video/YouTube work the
operator explicitly forbids.

The future skill must encode the full operational route and its guardrails so an
agent does not rely on chat memory or broad guesses.

## Target State

The operator can say something like:

```text
Запусти скилл publish-kernel-update
```

The agent then follows a deterministic workflow:

1. Audit the target GitHub repository state.
2. Audit the existing dudarik article state.
3. Decide whether this is first publication or update.
4. Create or update the RU+EN article content using the dudarik system.
5. Ensure the article uses the GitHub social preview image.
6. Ensure the article is excluded from all media pack automation.
7. Publish or refresh Telegram through the existing Telegram pipeline.
8. Verify that no `yotubol`, audio, infographic, video, or YouTube path was
   invoked.

## Proposed Skill

### Name

`publish-kernel-update`

### Skill location

Preferred location:

```text
~/.codex/skills/publish-kernel-update/SKILL.md
```

This should be a local operator skill because it coordinates two local projects
and production publication behavior.

If later generalized for other repositories, it can become a parameterized skill
or a small script-backed skill.

### Trigger description

Use when the operator wants to publish or update a dudarik.com article and
Telegram post about `alexxety/agent-engineering-kernel`, while excluding
NotebookLM, yotubol, audio, infographic, video, and YouTube media automation.

### Skill responsibilities

The skill must instruct the agent to:

- inspect `~/Work/Vs/agent-engineering-kernel`;
- inspect `~/Work/Vs/g3/dudarik.com`;
- use existing dudarik scripts/workflows where possible;
- preserve all production safety constraints;
- require `skip_media_pack: true`;
- require GitHub-sourced `hero_media_url`;
- verify no media pipeline was triggered.

### Skill non-responsibilities

The skill must not:

- implement an independent article generator;
- call YouTube;
- call `yotubol`;
- run audio or infographic sync workflows;
- create local media files;
- use generated images;
- mutate production secrets;
- bypass dudarik Telegram queue state.

## Article Content Contract

The initial article should be a stable overview of the kernel project:

- what the engineering kernel is;
- what problems it solves for agent-led engineering;
- how it structures PRDs, plans, GitHub issues, verification, and delivery;
- why it matters for Codex/GPT/Claude-style agents;
- what is currently included;
- what kind of teams or operators should care.

The update section should be incremental:

- summarize meaningful new PRDs, references, scripts, policies, or releases;
- ignore trivial formatting, typo-only, dependency noise, and internal churn;
- include dates and concrete change names where available;
- avoid hype;
- avoid claiming runtime success unless verified.

## Article Frontmatter Contract

Every RU and EN article variant for this skill must include equivalent identity
and guardrail metadata.

Required fields:

```yaml
slug: agent-engineering-kernel
draft: false
publish_policy: immediate
update_policy: kernel-line-manual
skip_media_pack: true
source_url: https://github.com/alexxety/agent-engineering-kernel
hero_media_type: photo
hero_media_url: https://opengraph.githubassets.com/dudarik/alexxety/agent-engineering-kernel
image: https://opengraph.githubassets.com/dudarik/alexxety/agent-engineering-kernel
```

Recommended category/topic:

```yaml
categories:
- Claude Code
tags:
- claude-code
- developer-tools
- automation
- ai-agents
- documentation
```

If implementation chooses a different slug, it must be explicit in the plan and
must update all tracking and Telegram commands consistently.

## Tracking Contract

To support future update runs, Kernel Line owns manual state in
`data/kernel_line_state.yaml`.

```yaml
kernel_update_line:
  repo: alexxety/agent-engineering-kernel
  article_slug: agent-engineering-kernel
  last_published_commit: "<full sha at last successful Kernel Line publish>"
```

The normal scanner must not own this repo. The following files must not contain
`agent-engineering-kernel` or `alexxety/agent-engineering-kernel`:

- `data/tracked_repos.yaml`;
- `data/mcp_repos.yaml`;
- `data/update_log.yaml`;
- `data/publish_queue.yaml`.

## Publication Flow

### First run

1. In `agent-engineering-kernel`, collect source evidence:
   - `git remote -v`;
   - current HEAD;
   - recent commits;
   - `README.md`;
   - `SKILL.md`;
   - `ENGINEERING_KERNEL.yaml`;
   - key references under `references/`;
   - current `CHANGELOG.md`.
2. In `dudarik.com`, check whether
   `content/ru/blog/agent-engineering-kernel.md` and
   `content/en/blog/agent-engineering-kernel.md` already exist.
3. If they do not exist, generate the article pair using the existing dudarik
   article style and editorial rules.
4. Ensure both files have the required frontmatter contract.
5. Ensure `data/kernel_line_state.yaml` records the Kernel Line cursor and the
   normal scanner files do not contain `alexxety/agent-engineering-kernel`.
6. Run local validation.
7. Publish via existing Telegram command:

```bash
python3 scripts/telegram-publish.py post-slug --slug agent-engineering-kernel --lang all
```

8. Commit only the expected dudarik state changes.
9. Verify deployment did not enqueue `yotubol`.

### Later run

1. Check existing article files and the Kernel Line state entry.
2. Compare current GitHub repo state with the tracked
   `last_published_commit`.
3. Identify meaningful changes:
   - accepted PRDs;
   - new/changed references;
   - new scripts or workflow canon;
   - changelog entries;
   - release tags if they exist.
4. If no meaningful changes exist, report no-op and do not post Telegram.
5. If meaningful changes exist, create pending findings or directly apply the
   existing update section flow.
6. Update RU and EN article sections only; do not create a second article or a
   new slug.
7. Preserve frontmatter guardrails.
8. Send a separate Telegram update notification that lists what changed and
   links to the stable article. Do not reuse `post-slug` for later update runs,
   because that would duplicate the article announcement.

## Implementation Options

### Option A: Skill-only orchestration

The skill contains step-by-step instructions and relies on existing scripts plus
careful file edits.

Pros:

- fastest to create;
- minimal code churn;
- keeps behavior easy to inspect.

Cons:

- depends on agent discipline;
- repeated runs may vary unless the skill is very explicit;
- harder to test end to end.

### Option B: Skill plus helper script

Use the dedicated dudarik Kernel Line helper:

```text
scripts/kernel-line.py
```

The skill calls the helper after doing human-level review and verification.

Pros:

- deterministic YAML and frontmatter updates;
- easier regression tests;
- safer duplicate handling;
- easier no-op behavior.

Cons:

- touches `dudarik.com` codebase;
- requires PRD/plan/tests there;
- slightly larger implementation.

### Option C: Fold into normal scheduled pipeline

Add `agent-engineering-kernel` to the normal scanner and let existing scheduled
generation/update/publish handle it.

Pros:

- reuses the most existing automation;
- least custom logic.

Cons:

- highest risk of accidental media enqueue;
- harder to keep immediate Telegram semantics;
- not a clean fit for an operator-triggered skill.
- rejected by the implemented skill because Kernel Line must stay manual-only
  and scanner-isolated.

## Recommended Approach

Use Option B.

Reason:

The dangerous part is not article text generation; it is repeatable state
mutation around frontmatter, tracking YAML, Telegram queue state, and media
exclusion. A small helper script with tests gives the skill a deterministic
execution surface while still reusing dudarik's existing article and Telegram
systems.

The first implementation can be staged:

1. create the skill as documentation;
2. create a dudarik PRD and helper script;
3. add tests for frontmatter/media exclusion/tracking behavior;
4. run a dry run;
5. perform the first publication only after operator approval.

## Write Scope

### In `agent-engineering-kernel`

Recorded:

- `docs/kernel-update-publisher-skill-prd-2026-04-28.md`
- `docs/superpowers/plans/2026-04-28-kernel-update-publisher-skill.md`

Implemented locally outside this repository:

- `~/.codex/skills/publish-kernel-update/SKILL.md`
- `~/.codex/skills/publish-kernel-update/agents/openai.yaml`
- `~/.codex/skills/publish-kernel-update/references/dudarik-kernel-update-flow.md`

### In `dudarik.com`

Potential future implementation:

- `scripts/kernel-line.py` changes only if the existing helper cannot cover a
  required mode;
- `data/kernel_line_state.yaml`;
- `content/ru/blog/agent-engineering-kernel.md`
- `content/en/blog/agent-engineering-kernel.md`
- `.github/workflows/kernel-line.yml` only if the manual workflow contract
  changes;
- Telegram state only after explicit production approval.

Forbidden write scope:

- `scripts/queue-yotubol.py` unless implementing only a guardrail test/fix;
- `scripts/article-audio-sync.py`;
- `scripts/article-infographic-sync.py`;
- `scripts/drain-yotubol-backlog.py`;
- `yotubol` repository;
- YouTube credentials or publication state;
- generated media artifacts.

## Safety Requirements

### Media exclusion

Every article variant must include:

```yaml
skip_media_pack: true
```

Verification must prove `scripts/queue-yotubol.py` ignores the article.

### Telegram-only publish

Publishing must go through `scripts/telegram-publish.py`.

The skill must not use direct Bot API publication as the primary path because
that would bypass queue state and duplicate protection.

### Image source

The only allowed image for the first version is GitHub-sourced:

```text
https://opengraph.githubassets.com/dudarik/alexxety/agent-engineering-kernel
```

No generated image, infographic, local upload, or article-media localization is
required.

### No-op behavior

If there are no meaningful updates, the skill must stop with a clear no-op
summary and must not publish Telegram.

### Secret handling

The skill must not print:

- bot tokens;
- private chat IDs not already committed as public channel names;
- GitHub tokens;
- deployment keys;
- production server secrets.

## Error Handling

If article generation fails:

- do not publish Telegram;
- keep any generated draft changes uncommitted or clearly staged for review;
- report the failing command and log path.

If Telegram dry-run fails:

- do not call production Telegram;
- fix copy/frontmatter first.

If `queue-yotubol.py --dry-run` would enqueue the slug:

- treat as a blocking failure;
- fix `skip_media_pack: true` or queue detection before publishing.

If the helper finds duplicate tracking entries:

- stop and ask for cleanup;
- do not run update publication.

## Testing Strategy

### Unit tests in `dudarik.com`

Add tests that prove:

- `agent-engineering-kernel` frontmatter includes `skip_media_pack: true`;
- `queue-yotubol.py` does not enqueue an article with `skip_media_pack: true`;
- tracking entry upsert is idempotent;
- GitHub OpenGraph URL is deterministic;
- Telegram queue discovery sees `hero_media_type: photo` and the GitHub image;
- update mode preserves frontmatter guardrails;
- no-op update mode does not modify Telegram queue.

### Dry-run checks

Expected dry-run commands:

```bash
python3 scripts/telegram-publish.py post-slug --slug agent-engineering-kernel --lang all --dry-run
python3 scripts/queue-yotubol.py --base <base> --head <head> --dry-run
```

The `post-slug` dry run applies only to first publication. Later update runs
must dry-run the dedicated dudarik update-notification path; if that path does
not exist yet, implementation must add it before production update posting.

The `queue-yotubol.py` dry run must not output a payload for
`agent-engineering-kernel`.

### Build checks

Expected:

```bash
hugo --minify --gc
```

or the repository's canonical verifier if broader checks are required.

### Skill checks

The skill file should be validated for:

- correct YAML frontmatter;
- concise trigger description;
- no workflow summary shortcut in `description`;
- explicit forbidden media actions;
- references to exact paths and commands.

## Verification Matrix

| Area | Verification |
| --- | --- |
| Article files | RU and EN files exist and validate as Hugo markdown |
| Frontmatter | Required metadata present in both languages |
| Media exclusion | `queue-yotubol.py --dry-run` does not enqueue the slug |
| Telegram preview | first run uses `telegram-publish.py post-slug --dry-run`; update run uses a dedicated update-notification dry run |
| Tracking | `data/kernel_line_state.yaml` records the Kernel Line commit cursor; the normal tracked-repo scanner is not used |
| Updates | later run inserts or replaces only the update section and does not create another article slug |
| No-op | no meaningful update produces no content or Telegram mutation |
| Build | Hugo build or canonical verifier passes |
| Secrets | no token/chat secret printed or committed |

## Acceptance Criteria

The implementation is acceptable when:

1. A `publish-kernel-update` skill exists and is discoverable by Codex.
2. The skill points to the current target repo:
   `alexxety/agent-engineering-kernel`.
3. The skill blocks the normal tracked-repo scanner and routes later updates
   through Kernel Line.
4. The initial article can be created as RU+EN content after operator approval.
5. Telegram can publish RU+EN posts with the GitHub social preview image.
6. The article cannot be enqueued into `yotubol` because
   `skip_media_pack: true` is present and verified.
7. Audio, infographic, video, NotebookLM, and YouTube paths are not called.
8. Later runs detect meaningful GitHub updates and publish only when needed.
9. Later runs preserve the media exclusion and source image metadata.
10. Tests or dry-run checks cover the media exclusion and Kernel Line tracking
    behavior.
11. The operator receives a clear no-op summary when nothing changed.

## Rollout Plan

Completed:

1. Created GitHub Task #46.
2. Created the local `publish-kernel-update` Codex skill.
3. Added the detailed dudarik Kernel Line reference.
4. Validated the skill with `quick_validate.py`.

If the operator explicitly requests production publication later:

1. In `dudarik.com`, add or update a local PRD if code changes are needed
   there.
2. Implement helper changes only if Kernel Line does not already cover the
   required mode.
3. Add tests or dry-run checks for media exclusion and Kernel Line tracking.
4. Run dry-run publication checks.
5. Generate the initial article only after operator approval.
6. Verify media exclusion.
7. Publish Telegram through the existing path only after explicit approval.
8. Commit and push only after verification.
9. Monitor the next deploy and confirm no `yotubol` backlog row was created.

## Rollback

If the article was generated but not published:

- delete or revert the content files and tracking entry;
- leave no Telegram state changes.

If Telegram was posted incorrectly:

- use existing `telegram-publish.py edit-slug` when safe;
- otherwise use the current Telegram operational recovery process.

If `yotubol` was accidentally enqueued:

- stop media drain immediately;
- remove or cancel the backlog row using the existing guarded `yotubol`
  operational path;
- add a regression test before retrying publication.

If the skill causes unsafe behavior:

- remove or disable `~/.codex/skills/publish-kernel-update`;
- keep this PRD as the audit source for the failed attempt;
- revise the skill before re-enabling it.

## Resolved Questions

1. First publication should use sandbox proof before production Telegram.
2. Later-run update notices are owned by Kernel Line, not duplicate
   `post-slug` article announcements.
3. The helper lives in `dudarik.com` as `scripts/kernel-line.py`.
4. The article uses the existing `claude-code` topic/category unless editorial
   categorization changes later.

Still pending:

- production publication has not been approved or run;
- first article content has not been generated in this slice.

## Kernel Impact

This PRD is project-specific to the operator's local `agent-engineering-kernel`
and `dudarik.com` publication workflow.

Kernel impact decision:

- `not_applicable` for the universal kernel unless this pattern becomes a
  reusable canon for publishing kernel release notes across many consumer
  projects.
