#!/usr/bin/env node

import { mkdtemp, writeFile, rm } from "node:fs/promises";
import { spawn } from "node:child_process";
import { tmpdir } from "node:os";
import path from "node:path";

const validator = new URL("./validate_diagram_layout.mjs", import.meta.url).pathname;
const work = await mkdtemp(path.join(tmpdir(), "diagram-gate-test-"));

const base = (body) => `<!doctype html><html><head><style>*{box-sizing:border-box}html,body{margin:0;width:800px;height:450px;overflow:hidden}.node{position:absolute;width:160px;height:90px;border:1px solid}.label{position:absolute;width:48px;height:24px}svg{position:absolute;inset:0}</style></head><body>${body}</body></html>`;

const cases = [
  {
    name: "valid",
    expected: 0,
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H500"/></svg>`),
  },
  {
    name: "strict-valid-contract",
    expected: 0,
    args: ["--strict"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px;font-size:16px" data-layout-text="a-copy" data-node-ref="a">Node A</div></div><div class="node" style="left:500px;top:100px" data-layout-node="b"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px;font-size:16px" data-layout-text="b-copy" data-node-ref="b">Node B</div></div><div class="label" style="left:300px;top:60px;font-size:16px" data-layout-label="a-b-label" data-edge-ref="a-b">next</div><svg viewBox="0 0 800 450"><defs><marker id="strict-arrow" markerWidth="10" markerHeight="10" refX="0" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L9 5L0 10z"/></marker></defs><path data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M200 145H500" marker-end="url(#strict-arrow)"/></svg>`),
  },
  {
    name: "strict-valid-edgeless-matrix",
    expected: 0,
    args: ["--strict"],
    html: `<!doctype html><html data-layout-kind="matrix"><head><style>*{box-sizing:border-box}html,body{margin:0;width:800px;height:450px;overflow:hidden}.node{position:absolute;width:160px;height:90px;border:1px solid}</style></head><body><div class="node" style="left:80px;top:100px" data-layout-node="a"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px;font-size:16px" data-layout-text="a-copy" data-node-ref="a">Status A</div></div><div class="node" style="left:500px;top:100px" data-layout-node="b"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px;font-size:16px" data-layout-text="b-copy" data-node-ref="b">Status B</div></div></body></html>`,
  },
  {
    name: "strict-unannotated-text",
    expected: 1,
    expectedError: "unannotated-layout-text",
    args: ["--strict"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="a-copy" data-node-ref="a">Node A</div></div><div class="node" style="left:500px;top:100px" data-layout-node="b"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="b-copy" data-node-ref="b">Node B</div></div><p style="position:absolute;left:300px;top:240px">loose note</p><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5"><path d="M0 0L9 5L0 10z"/></marker></defs><path data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M200 145H500" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "strict-duplicate-node-id",
    expected: 1,
    expectedError: "semantic-id-duplicate",
    args: ["--strict"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="a-copy" data-node-ref="a">Node A</div></div><div class="node" style="left:500px;top:100px" data-layout-node="a"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="a-copy-2" data-node-ref="a">Node A2</div></div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5"><path d="M0 0L9 5L0 10z"/></marker></defs><path data-layout-edge="a-a" data-from="a" data-to="a" data-flow="right" d="M200 145H500" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "strict-empty-node-id",
    expected: 1,
    expectedError: "semantic-id-empty",
    args: ["--strict"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node=""><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="orphan-copy" data-layout-role="note">Orphan</div></div><div class="node" style="left:500px;top:100px" data-layout-node="b"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="b-copy" data-node-ref="b">Node B</div></div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5"><path d="M0 0L9 5L0 10z"/></marker></defs><path data-layout-edge="orphan-b" data-from="orphan" data-to="b" data-flow="right" d="M200 145H500" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "strict-label-missing-edge-ref",
    expected: 1,
    expectedError: "label-edge-annotation",
    args: ["--strict"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="a-copy" data-node-ref="a">Node A</div></div><div class="node" style="left:500px;top:100px" data-layout-node="b"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="b-copy" data-node-ref="b">Node B</div></div><div class="label" style="left:300px;top:60px" data-layout-label="a-b-label">next</div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5"><path d="M0 0L9 5L0 10z"/></marker></defs><path data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M200 145H500" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "strict-small-font",
    expected: 1,
    expectedError: "font-size-minimum",
    args: ["--strict"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px;font-size:12px" data-layout-text="a-copy" data-node-ref="a">Node A</div></div><div class="node" style="left:500px;top:100px" data-layout-node="b"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="b-copy" data-node-ref="b">Node B</div></div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5"><path d="M0 0L9 5L0 10z"/></marker></defs><path data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M200 145H500" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "strict-canvas-clearance",
    expected: 1,
    expectedError: "canvas-clearance",
    args: ["--strict"],
    html: base(`<div class="node" style="left:8px;top:100px" data-layout-node="a"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="a-copy" data-node-ref="a">Node A</div></div><div class="node" style="left:500px;top:100px" data-layout-node="b"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="b-copy" data-node-ref="b">Node B</div></div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5"><path d="M0 0L9 5L0 10z"/></marker></defs><path data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M168 145H500" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "strict-label-collision",
    expected: 1,
    expectedError: "label-label-clearance",
    args: ["--strict"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="a-copy" data-node-ref="a">Node A</div></div><div class="node" style="left:500px;top:100px" data-layout-node="b"><div style="position:absolute;left:20px;top:25px;width:100px;height:40px" data-layout-text="b-copy" data-node-ref="b">Node B</div></div><div class="label" style="left:300px;top:60px" data-layout-label="label-1" data-edge-ref="a-b">next</div><div class="label" style="left:346px;top:60px" data-layout-label="label-2" data-edge-ref="a-b">again</div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5"><path d="M0 0L9 5L0 10z"/></marker></defs><path data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M200 145H500" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "edge-edge-crossing",
    expected: 1,
    expectedError: "edge-edge-crossings",
    args: ["--max-edge-crossings", "0"],
    html: base(`<div class="node" style="left:40px;top:40px" data-layout-node="a">A</div><div class="node" style="left:500px;top:300px" data-layout-node="b">B</div><div class="node" style="left:500px;top:40px" data-layout-node="c">C</div><div class="node" style="left:40px;top:300px" data-layout-node="d">D</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M200 85L500 345"/><path data-layout-edge="c-d" data-from="c" data-to="d" d="M500 85L200 345"/></svg>`),
  },
  {
    name: "valid-boundary-clearance",
    expected: 0,
    args: ["--boundary-clearance", "16"],
    html: base(`<div style="position:absolute;left:220px;top:40px;width:2px;height:180px" data-layout-boundary="rail-divider"></div><div style="position:absolute;left:40px;top:70px;width:160px;height:60px" data-layout-text="rail-copy" data-boundary-ref="rail-divider" data-boundary-side="left">two-line rail copy</div><div class="node" style="left:300px;top:100px" data-layout-node="a">A</div><div class="node" style="left:560px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M460 145H560"/></svg>`),
  },
  {
    name: "boundary-text-crossing",
    expected: 1,
    expectedError: "text-boundary-clearance",
    args: ["--boundary-clearance", "16"],
    html: base(`<div style="position:absolute;left:220px;top:40px;width:2px;height:180px" data-layout-boundary="rail-divider"></div><div style="position:absolute;left:40px;top:70px;width:190px;height:60px" data-layout-text="rail-copy" data-boundary-ref="rail-divider" data-boundary-side="left">copy crossing divider</div><div class="node" style="left:300px;top:100px" data-layout-node="a">A</div><div class="node" style="left:560px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M460 145H560"/></svg>`),
  },
  {
    name: "valid-divider-node-clearance",
    expected: 0,
    args: ["--divider-node-clearance", "16"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><div style="position:absolute;left:40px;top:220px;width:620px;height:1px" data-layout-divider="footer-divider"></div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H500"/></svg>`),
  },
  {
    name: "divider-crosses-node",
    expected: 1,
    expectedError: "divider-node-clearance",
    args: ["--divider-node-clearance", "16"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><div style="position:absolute;left:40px;top:188px;width:620px;height:1px" data-layout-divider="footer-divider"></div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H500"/></svg>`),
  },
  {
    name: "valid-node-text-clearance",
    expected: 0,
    args: ["--text-node-clearance", "18"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a"><div style="position:absolute;left:24px;top:24px;width:96px;height:36px" data-layout-text="a-copy" data-node-ref="a">Node copy</div></div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H500"/></svg>`),
  },
  {
    name: "node-text-border-collision",
    expected: 1,
    expectedError: "text-node-clearance",
    args: ["--text-node-clearance", "18"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a"><div style="position:absolute;left:8px;top:24px;width:144px;height:36px" data-layout-text="a-copy" data-node-ref="a">Copy against border</div></div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H500"/></svg>`),
  },
  {
    name: "valid-accent-text-clearance",
    expected: 0,
    args: ["--accent-text-clearance", "8"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a"><div style="position:absolute;left:16px;top:16px;width:16px;height:16px;border-radius:50%" aria-label="ready" data-layout-accent="a-status" data-for-node="a"></div><div style="position:absolute;left:16px;top:40px;width:120px;height:32px" data-layout-text="a-copy" data-node-ref="a">Node copy</div></div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H500"/></svg>`),
  },
  {
    name: "accent-text-collision",
    expected: 1,
    expectedError: "accent-text-clearance",
    args: ["--accent-text-clearance", "8"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a"><div style="position:absolute;left:16px;top:16px;width:16px;height:16px;border-radius:50%" aria-label="ready" data-layout-accent="a-status" data-for-node="a"></div><div style="position:absolute;left:16px;top:28px;width:120px;height:32px" data-layout-text="a-copy" data-node-ref="a">Cramped copy</div></div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H500"/></svg>`),
  },
  {
    name: "decorative-accent-bar",
    expected: 1,
    expectedError: "decorative-accent-bar",
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a"><div style="position:absolute;left:16px;top:16px;width:48px;height:6px" data-layout-accent="a-bar" data-for-node="a"></div></div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H500"/></svg>`),
  },
  {
    name: "valid-spacious-stage",
    expected: 0,
    args: ["--min-gap", "80", "--edge-clearance", "20", "--marker-clearance", "20", "--label-clearance", "8", "--connector-label-clearance", "16", "--accent-border-clearance", "8", "--min-edge-length", "56", "--max-marker-size", "16"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A<div style="position:absolute;left:16px;top:16px;width:16px;height:16px;border-radius:50%" aria-label="ready" data-layout-accent="a-status" data-for-node="a"></div></div><div class="node" style="left:320px;top:100px" data-layout-node="b">B</div><div class="label" style="left:246px;top:60px" data-layout-label="a-b-label">next</div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" markerUnits="userSpaceOnUse"><path d="M1 1L11 6L1 11z"/></marker></defs><path style="stroke-width:4" data-layout-edge="a-b" data-from="a" data-to="b" d="M220 145H286" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "valid-directed-down",
    expected: 0,
    html: base(`<div class="node" style="left:300px;top:40px" data-layout-node="a">A</div><div class="node" style="left:300px;top:260px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" markerUnits="userSpaceOnUse"><path d="M0 0L9 5L0 10z"/></marker></defs><path data-layout-edge="a-b" data-from="a" data-to="b" data-flow="down" d="M380 150V235" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "valid-explicit-arrow-join",
    expected: 0,
    args: ["--arrow-join-tolerance", "2", "--marker-clearance", "20"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path style="stroke:#468b84;stroke-width:4;stroke-linecap:butt;fill:none" data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M220 145H460"/><path data-arrow-for="a-b" d="M460 137L470 145L460 153Z" fill="#468b84"/></svg>`),
  },
  {
    name: "valid-curved-arrow-terminal-tangent",
    expected: 0,
    args: ["--arrow-join-tolerance", "2", "--arrow-tangent-tolerance", "8"],
    html: base(`<div class="node" style="left:300px;top:40px" data-layout-node="a">A</div><div class="node" style="left:300px;top:260px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path style="stroke:#468b84;stroke-width:4;stroke-linecap:butt;fill:none" data-layout-edge="a-b" data-from="a" data-to="b" data-flow="down" d="M380 150C340 180 380 185 380 215L380 235"/><path data-arrow-for="a-b" d="M372 235L380 245L388 235Z" fill="#468b84"/></svg>`),
  },
  {
    name: "curved-arrow-hidden-kink-before-short-tail",
    expected: 1,
    expectedError: "arrow-tangent-misaligned",
    args: ["--arrow-join-tolerance", "2", "--arrow-tangent-tolerance", "8"],
    html: base(`<div class="node" style="left:300px;top:40px" data-layout-node="a">A</div><div class="node" style="left:300px;top:260px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path style="stroke:#468b84;stroke-width:4;stroke-linecap:butt;fill:none" data-layout-edge="a-b" data-from="a" data-to="b" data-flow="down" d="M380 150C380 190 340 210 380 225L380 235"/><path data-arrow-for="a-b" d="M372 235L380 245L388 235Z" fill="#468b84"/></svg>`),
  },
  {
    name: "curved-arrow-diagonal-terminal-tangent",
    expected: 1,
    expectedError: "arrow-tangent-misaligned",
    args: ["--arrow-join-tolerance", "2", "--arrow-tangent-tolerance", "8"],
    html: base(`<div class="node" style="left:300px;top:40px" data-layout-node="a">A</div><div class="node" style="left:300px;top:260px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path style="stroke:#468b84;stroke-width:4;stroke-linecap:butt;fill:none" data-layout-edge="a-b" data-from="a" data-to="b" data-flow="down" d="M380 150C380 190 340 210 380 235"/><path data-arrow-for="a-b" d="M372 235L380 245L388 235Z" fill="#468b84"/></svg>`),
  },
  {
    name: "marker-arrow-ref-at-tip-overlaps-shaft",
    expected: 1,
    expectedError: "arrow-shaft-overlap",
    args: ["--arrow-join-tolerance", "2"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="5" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L10 5L0 10z"/></marker></defs><path style="stroke:#468b84;stroke-width:4;stroke-linecap:butt;fill:none" data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M220 145H460" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "explicit-arrow-shaft-gap",
    expected: 1,
    expectedError: "arrow-shaft-gap",
    args: ["--arrow-join-tolerance", "2"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path style="stroke:#468b84;stroke-width:4;stroke-linecap:butt;fill:none" data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M220 145H455"/><path data-arrow-for="a-b" d="M460 137L470 145L460 153Z" fill="#468b84"/></svg>`),
  },
  {
    name: "explicit-arrow-shaft-overlap",
    expected: 1,
    expectedError: "arrow-shaft-overlap",
    args: ["--arrow-join-tolerance", "2"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path style="stroke:#468b84;stroke-width:4;stroke-linecap:butt;fill:none" data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M220 145H470"/><path data-arrow-for="a-b" d="M460 137L470 145L460 153Z" fill="#468b84"/></svg>`),
  },
  {
    name: "explicit-arrow-shaft-misaligned",
    expected: 1,
    expectedError: "arrow-shaft-misaligned",
    args: ["--arrow-join-tolerance", "2"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path style="stroke:#468b84;stroke-width:4;stroke-linecap:butt;fill:none" data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M220 140H460"/><path data-arrow-for="a-b" d="M460 137L470 145L460 153Z" fill="#468b84"/></svg>`),
  },
  {
    name: "explicit-arrow-color-mismatch",
    expected: 1,
    expectedError: "arrow-color-mismatch",
    args: ["--arrow-join-tolerance", "2"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path style="stroke:#ad6a61;stroke-width:4;stroke-linecap:butt;fill:none" data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M220 145H460"/><path data-arrow-for="a-b" d="M460 137L470 145L460 153Z" fill="#468b84"/></svg>`),
  },
  {
    name: "marker-shaft-overrun",
    expected: 1,
    expectedError: "marker-shaft-overrun",
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="11" markerHeight="11" refX="8" refY="5.5" markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L9 5.5L0 11z"/></marker></defs><path style="stroke-width:5;stroke-linecap:round" data-layout-edge="a-b" data-from="a" data-to="b" data-flow="right" d="M200 145H470" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "reversed-directed-down",
    expected: 1,
    expectedError: "edge-direction",
    html: base(`<div class="node" style="left:300px;top:40px" data-layout-node="a">A</div><div class="node" style="left:300px;top:260px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" markerUnits="userSpaceOnUse"><path d="M0 0L9 5L0 10z"/></marker></defs><path data-layout-edge="a-b" data-from="a" data-to="b" data-flow="down" d="M380 235V150" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "directed-arrow-at-source",
    expected: 1,
    expectedError: "edge-arrow-target",
    html: base(`<div class="node" style="left:300px;top:40px" data-layout-node="a">A</div><div class="node" style="left:300px;top:260px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" markerUnits="userSpaceOnUse"><path d="M0 0L9 5L0 10z"/></marker></defs><path data-layout-edge="a-b" data-from="a" data-to="b" data-flow="down" d="M380 150V235" marker-start="url(#arrow)"/></svg>`),
  },
  {
    name: "marker-card-collision",
    expected: 1,
    args: ["--min-gap", "80", "--edge-clearance", "20", "--marker-clearance", "20", "--min-edge-length", "56", "--max-marker-size", "16"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:300px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><defs><marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" markerUnits="userSpaceOnUse"><path d="M1 1L11 6L1 11z"/></marker></defs><path style="stroke-width:4" data-layout-edge="a-b" data-from="a" data-to="b" d="M220 145H276" marker-end="url(#arrow)"/></svg>`),
  },
  {
    name: "short-oversized-arrow",
    expected: 1,
    args: ["--min-edge-length", "56", "--max-marker-size", "16"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:236px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><defs><marker id="large-arrow" markerWidth="10" markerHeight="10" markerUnits="strokeWidth"><path d="M0 0L10 5L0 10z"/></marker></defs><path style="stroke-width:3.5" data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H236" marker-end="url(#large-arrow)"/></svg>`),
  },
  {
    name: "cramped-stage",
    expected: 1,
    args: ["--min-gap", "80", "--edge-clearance", "20", "--label-clearance", "8"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:244px;top:100px" data-layout-node="b">B</div><div class="label" style="left:198px;top:60px" data-layout-label="a-b-label">next</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M204 145H240"/></svg>`),
  },
  {
    name: "label-connector-collision",
    expected: 1,
    expectedError: "connector-label-clearance",
    args: ["--connector-label-clearance", "16"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><div class="label" style="left:300px;top:133px" data-layout-label="a-b-label">next</div><svg viewBox="0 0 800 450"><path style="stroke-width:4" data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H500"/></svg>`),
  },
  {
    name: "accent-border-collision",
    expected: 1,
    expectedError: "accent-border-clearance",
    args: ["--accent-border-clearance", "8"],
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A<div style="position:absolute;left:0;top:0;width:16px;height:16px;border-radius:50%" aria-label="ready" data-layout-accent="a-status" data-for-node="a"></div></div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H500"/></svg>`),
  },
  {
    name: "overlap",
    expected: 1,
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:100px;top:120px" data-layout-node="b">B</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H500"/></svg>`),
  },
  {
    name: "edge-crossing",
    expected: 1,
    html: base(`<div class="node" style="left:40px;top:100px" data-layout-node="a">A</div><div class="node" style="left:500px;top:100px" data-layout-node="b">B</div><div class="node" style="left:310px;top:100px" data-layout-node="c">C</div><svg viewBox="0 0 800 450"><path data-layout-edge="a-b" data-from="a" data-to="b" d="M200 145H500"/></svg>`),
  },
  {
    name: "missing-annotations",
    expected: 1,
    html: base(`<div>not a diagram contract</div>`),
  },
];

const requestedCases = new Set((process.env.DIAGRAM_TEST_FILTER || "").split(",").map((name) => name.trim()).filter(Boolean));
const selectedCases = requestedCases.size ? cases.filter((test) => requestedCases.has(test.name)) : cases;
if (requestedCases.size && selectedCases.length !== requestedCases.size) {
  const found = new Set(selectedCases.map((test) => test.name));
  throw new Error(`Unknown test case(s): ${[...requestedCases].filter((name) => !found.has(name)).join(", ")}`);
}

try {
  for (const test of selectedCases) {
    const file = path.join(work, `${test.name}.html`);
    await writeFile(file, test.html, "utf8");
    const result = await new Promise((resolve, reject) => {
      const child = spawn(process.execPath, [validator, file, "--width", "800", "--height", "450", ...(test.args || ["--min-gap", "24"])], { stdio: ["ignore", "pipe", "pipe"] });
      let stdout = "", stderr = "";
      child.stdout.on("data", (chunk) => stdout += chunk);
      child.stderr.on("data", (chunk) => stderr += chunk);
      child.on("error", reject);
      child.on("exit", (code) => resolve({ code, stdout, stderr }));
    });
    const normalized = result.code === 0 ? 0 : 1;
    if (normalized !== test.expected) throw new Error(`${test.name}: expected ${test.expected}, got ${result.code}\n${result.stdout}\n${result.stderr}`);
    if (test.expectedError) {
      const report = JSON.parse(result.stdout);
      if (!report.errors.some((error) => error.type === test.expectedError)) {
        throw new Error(`${test.name}: expected error ${test.expectedError}\n${result.stdout}\n${result.stderr}`);
      }
    }
    console.log(`PASS ${test.name}`);
  }
} finally {
  await rm(work, { recursive: true, force: true });
}
