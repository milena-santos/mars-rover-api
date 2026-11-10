# Contributing

## Branches

`main` and `develop` are permanent and protected branches:

- `main` contains production-ready code.
- `develop` contains changes approved for staging.

Create short-lived branches from `develop`:

```text
feature/short-description
fix/short-description
chore/short-description
docs/short-description
refactor/short-description
test/short-description
```

Create `hotfix/short-description` from `main` only for urgent production
corrections. A merged hotfix must also be synchronized back into `develop`.

Use lowercase kebab-case and describe the intended outcome. Do not include
personal names in branch names.

## Commits

Commit messages follow the
[Conventional Commits](https://www.conventionalcommits.org/) specification:

```text
<type>(optional-scope): <description>
```

Examples:

```text
feat(probes): add left rotation
fix(api): reject unknown commands
test(domain): cover plateau boundaries
chore(ci): add quality checks
```

Keep commits focused and do not mix unrelated changes.

## Pull requests

1. Push the short-lived branch.
2. Open a pull request targeting `develop`.
3. Complete the pull request template.
4. Keep the branch updated and resolve every review conversation.
5. Merge only after all required checks and approvals pass.

Feature work is squash-merged into `develop`. Releases from `develop` to
`main` use a merge commit so the histories of the permanent branches remain
related.

## Quality

Every behavior change must include appropriate tests. Formatting, linting,
typing, migrations, tests, and coverage checks must pass before merge.

