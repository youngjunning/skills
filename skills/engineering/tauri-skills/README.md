# Tauri Skills

An Agent Skill for designing, implementing, reviewing, and verifying secure Tauri 2 desktop applications with:

- a Rust trusted core;
- scoped capabilities, permissions, and typed IPC;
- isolated local and remote WebViews;
- a managed Node.js sidecar;
- contract, security, build, and packaging gates.

## Install

```bash
npx skills add youngjunning/skills --skill tauri-skills -g -y
```

This directory is the Skill package: [`SKILL.md`](SKILL.md) contains the workflow, with detailed guidance under [`references/`](references/).

## Design goal

This project combines broad Tauri 2 engineering guidance with the security and sidecar boundaries needed by Agent-host desktop applications. Tauri's official v2 documentation remains authoritative for version-sensitive APIs and release behavior.

## Community Skill references

This Skill was designed after evaluating the following community Skills:

| Skill | What was evaluated |
|---|---|
| [`nodnarbnitram/claude-code-extensions@tauri-v2`](https://skills.sh/nodnarbnitram/claude-code-extensions/tauri-v2) | General Tauri 2 development workflow, commands, IPC, capabilities, plugins, updater, and sidecar coverage |
| [`dchuk/claude-code-tauri-skills@configuring-tauri-permissions`](https://skills.sh/dchuk/claude-code-tauri-skills/configuring-tauri-permissions) | Capability decomposition, permission scope, window boundaries, and least-privilege review topics |
| [`dchuk/claude-code-tauri-skills@running-nodejs-sidecar-in-tauri`](https://skills.sh/dchuk/claude-code-tauri-skills/running-nodejs-sidecar-in-tauri) | Node.js sidecar packaging, execution, and lifecycle topics |

The `tauri-v2` source is MIT-licensed and is attributed in [`NOTICE`](NOTICE). The referenced `dchuk` repository did not publish an explicit license when this project was created, so its text was not copied or redistributed. This repository provides an original synthesis based primarily on the official Tauri v2 documentation.

## License

MIT. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
