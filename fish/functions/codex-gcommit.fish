function codex-gcommit --description "Commit current changes with Codex git-logical-commits skill"
    codex exec --profile git-logical-commit --ephemeral --ignore-rules \
        -c 'mcp_servers={}' \
        'Use $git-logical-commits. Commit the current working tree changes now. Use only this skill. Do not use MCP, apps, connectors, web search, subagents, browser, computer use, or any other skill. Do not edit source files. Do not run lint, tests, build, typecheck, commitlint, or validation checks. Skip git hooks/checks by using git commit --no-verify. Use only git status, git diff, git diff --staged, git add, git commit, and final git status. Split into logical Conventional Commits if needed. Do not add tool, model, or vendor footers.'
end
