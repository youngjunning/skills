#!/usr/bin/env node

import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { existsSync, readdirSync, realpathSync } from "node:fs";
import { spawn } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { homedir, tmpdir } from "node:os";
import { createServer } from "node:net";
import path from "node:path";

function parseArgs(argv) {
  const result = { strict: false, minGap: 24, edgeClearance: 0, markerClearance: 0, arrowJoinTolerance: 0, arrowTangentTolerance: 0, markerShaftTolerance: 0.25, labelClearance: 0, labelGap: 0, connectorLabelClearance: 0, accentBorderClearance: 0, accentTextClearance: 0, boundaryClearance: 0, dividerNodeClearance: 0, textNodeClearance: 0, canvasClearance: 0, minFontSize: 0, maxEdgeCrossings: -1, minEdgeLength: 0, maxMarkerSize: 0, width: 1600, height: 900, scale: 1, screenshot: "", html: "" };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--strict") result.strict = true;
    else if (arg === "--min-gap") result.minGap = Number(argv[++i]);
    else if (arg === "--edge-clearance") result.edgeClearance = Number(argv[++i]);
    else if (arg === "--marker-clearance") result.markerClearance = Number(argv[++i]);
    else if (arg === "--arrow-join-tolerance") result.arrowJoinTolerance = Number(argv[++i]);
    else if (arg === "--arrow-tangent-tolerance") result.arrowTangentTolerance = Number(argv[++i]);
    else if (arg === "--marker-shaft-tolerance") result.markerShaftTolerance = Number(argv[++i]);
    else if (arg === "--label-clearance") result.labelClearance = Number(argv[++i]);
    else if (arg === "--label-gap") result.labelGap = Number(argv[++i]);
    else if (arg === "--connector-label-clearance") result.connectorLabelClearance = Number(argv[++i]);
    else if (arg === "--accent-border-clearance") result.accentBorderClearance = Number(argv[++i]);
    else if (arg === "--accent-text-clearance") result.accentTextClearance = Number(argv[++i]);
    else if (arg === "--boundary-clearance") result.boundaryClearance = Number(argv[++i]);
    else if (arg === "--divider-node-clearance") result.dividerNodeClearance = Number(argv[++i]);
    else if (arg === "--text-node-clearance") result.textNodeClearance = Number(argv[++i]);
    else if (arg === "--canvas-clearance") result.canvasClearance = Number(argv[++i]);
    else if (arg === "--min-font-size") result.minFontSize = Number(argv[++i]);
    else if (arg === "--max-edge-crossings") result.maxEdgeCrossings = Number(argv[++i]);
    else if (arg === "--min-edge-length") result.minEdgeLength = Number(argv[++i]);
    else if (arg === "--max-marker-size") result.maxMarkerSize = Number(argv[++i]);
    else if (arg === "--width") result.width = Number(argv[++i]);
    else if (arg === "--height") result.height = Number(argv[++i]);
    else if (arg === "--scale") result.scale = Number(argv[++i]);
    else if (arg === "--screenshot") result.screenshot = argv[++i];
    else if (!result.html) result.html = arg;
    else throw new Error(`Unexpected argument: ${arg}`);
  }
  if (!result.html) throw new Error("Usage: validate_diagram_layout.mjs <diagram.html-or-svg> [--strict] [--min-gap 24] [--edge-clearance 0] [--marker-clearance 0] [--arrow-join-tolerance 0] [--arrow-tangent-tolerance 0] [--marker-shaft-tolerance 0.25] [--label-clearance 0] [--label-gap 0] [--connector-label-clearance 0] [--accent-border-clearance 0] [--accent-text-clearance 0] [--boundary-clearance 0] [--divider-node-clearance 0] [--text-node-clearance 0] [--canvas-clearance 0] [--min-font-size 0] [--max-edge-crossings -1] [--min-edge-length 0] [--max-marker-size 0] [--width 1600] [--height 900] [--scale 1] [--screenshot output.png]");
  if (result.strict) {
    if (result.textNodeClearance === 0) result.textNodeClearance = 18;
    if (result.boundaryClearance === 0) result.boundaryClearance = 24;
    if (result.dividerNodeClearance === 0) result.dividerNodeClearance = 16;
    if (result.canvasClearance === 0) result.canvasClearance = 24;
    if (result.minFontSize === 0) result.minFontSize = 16;
    if (result.labelGap === 0) result.labelGap = 8;
    if (result.arrowJoinTolerance === 0) result.arrowJoinTolerance = 2;
    if (result.arrowTangentTolerance === 0) result.arrowTangentTolerance = 8;
    if (result.accentTextClearance === 0) result.accentTextClearance = 8;
    if (result.maxEdgeCrossings < 0) result.maxEdgeCrossings = 0;
  }
  for (const key of ["minGap", "edgeClearance", "markerClearance", "arrowJoinTolerance", "arrowTangentTolerance", "markerShaftTolerance", "labelClearance", "labelGap", "connectorLabelClearance", "accentBorderClearance", "accentTextClearance", "boundaryClearance", "dividerNodeClearance", "textNodeClearance", "canvasClearance", "minFontSize", "minEdgeLength", "maxMarkerSize", "width", "height", "scale"]) {
    if (!Number.isFinite(result[key]) || result[key] < 0) throw new Error(`Invalid --${key}: ${result[key]}`);
  }
  if (!Number.isInteger(result.maxEdgeCrossings) || result.maxEdgeCrossings < -1) throw new Error(`Invalid --max-edge-crossings: ${result.maxEdgeCrossings}`);
  if (result.scale <= 0) throw new Error(`Invalid --scale: ${result.scale}`);
  return result;
}

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function stopChrome(child) {
  if (child.exitCode !== null) return;
  const exited = new Promise((resolve) => child.once("exit", resolve));
  child.kill("SIGTERM");
  await Promise.race([exited, delay(3000)]);
  if (child.exitCode === null) {
    child.kill("SIGKILL");
    await Promise.race([exited, delay(1000)]);
  }
}

async function getFreePort() {
  const server = createServer();
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolve);
  });
  const address = server.address();
  await new Promise((resolve) => server.close(resolve));
  return address.port;
}

async function waitForDevTools(port, child) {
  const maxAttempts = process.env.DIAGRAM_VALIDATOR_DEBUG ? 6000 : 1200;
  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    if (child.exitCode !== null) throw new Error(`Chrome exited before DevTools started: ${child.exitCode}`);
    try {
      const response = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (response.ok) return port;
    } catch {}
    await delay(50);
  }
  throw new Error(`Timed out waiting for Chrome DevTools on port ${port}`);
}

function createCdpSocket(url) {
  const socket = new WebSocket(url);
  let nextId = 1;
  const pending = new Map();
  const events = new Map();

  socket.addEventListener("message", ({ data }) => {
    const message = JSON.parse(data);
    if (message.id) {
      const waiter = pending.get(message.id);
      if (!waiter) return;
      pending.delete(message.id);
      if (message.error) waiter.reject(new Error(message.error.message));
      else waiter.resolve(message.result);
      return;
    }
    const waiters = events.get(message.method) || [];
    events.delete(message.method);
    for (const resolve of waiters) resolve(message.params);
  });

  const ready = new Promise((resolve, reject) => {
    socket.addEventListener("open", resolve, { once: true });
    socket.addEventListener("error", reject, { once: true });
  });

  return {
    ready,
    send(method, params = {}) {
      const id = nextId++;
      return new Promise((resolve, reject) => {
        pending.set(id, { resolve, reject });
        socket.send(JSON.stringify({ id, method, params }));
      });
    },
    once(method) {
      return new Promise((resolve) => {
        const waiters = events.get(method) || [];
        waiters.push(resolve);
        events.set(method, waiters);
      });
    },
    close() { socket.close(); },
  };
}

function gateExpression({ strict, minGap, edgeClearance, markerClearance, arrowJoinTolerance, arrowTangentTolerance, markerShaftTolerance, labelClearance, labelGap, connectorLabelClearance, accentBorderClearance, accentTextClearance, boundaryClearance, dividerNodeClearance, textNodeClearance, canvasClearance, minFontSize, maxEdgeCrossings, minEdgeLength, maxMarkerSize, width, height }) {
  return `(() => {
    const config = ${JSON.stringify({ strict, minGap, edgeClearance, markerClearance, arrowJoinTolerance, arrowTangentTolerance, markerShaftTolerance, labelClearance, labelGap, connectorLabelClearance, accentBorderClearance, accentTextClearance, boundaryClearance, dividerNodeClearance, textNodeClearance, canvasClearance, minFontSize, maxEdgeCrossings, minEdgeLength, maxMarkerSize, width, height })};
    const errors = [];
    const root = document.documentElement;
    if (root.tagName.toLowerCase() === 'svg') {
      root.setAttribute('width', String(config.width));
      root.setAttribute('height', String(config.height));
      root.style.width = config.width + 'px';
      root.style.height = config.height + 'px';
    }
    const round = (value) => Math.round(value * 10) / 10;
    const rectOf = (element) => {
      const r = element.getBoundingClientRect();
      return { left: r.left, top: r.top, right: r.right, bottom: r.bottom, width: r.width, height: r.height };
    };
    const nameOf = (element) => element.dataset.layoutNode || element.dataset.layoutText || element.dataset.layoutLabel || element.dataset.layoutAccent || element.dataset.layoutDivider || element.dataset.layoutBoundary || element.id || element.tagName;
    const intersects = (a, b, inset = 0) =>
      Math.min(a.right - inset, b.right - inset) > Math.max(a.left + inset, b.left + inset) &&
      Math.min(a.bottom - inset, b.bottom - inset) > Math.max(a.top + inset, b.top + inset);
    const overlap = (a, b) => ({
      x: Math.min(a.right, b.right) - Math.max(a.left, b.left),
      y: Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top),
    });
    const pointDistanceToRect = (point, rect) => {
      const dx = Math.max(rect.left - point.x, 0, point.x - rect.right);
      const dy = Math.max(rect.top - point.y, 0, point.y - rect.bottom);
      return Math.hypot(dx, dy);
    };
    const isVisible = (element) => {
      const style = getComputedStyle(element);
      return style.display !== 'none' && style.visibility !== 'hidden' && Number.parseFloat(style.opacity || '1') > 0;
    };
    const layoutRoot = document.querySelector('[data-layout-kind]');
    const layoutKind = layoutRoot?.dataset.layoutKind || '';
    const edgelessLayoutKinds = new Set(['matrix', 'comparison', 'status-board']);
    const nodes = [...document.querySelectorAll('[data-layout-node]')].map((element) => ({ element, name: element.dataset.layoutNode || '', rect: rectOf(element) }));
    const labels = [...document.querySelectorAll('[data-layout-label]')].map((element) => ({ element, name: element.dataset.layoutLabel || '', rect: rectOf(element) }));
    const texts = [...document.querySelectorAll('[data-layout-text]')].map((element) => ({ element, name: element.dataset.layoutText || '', rect: rectOf(element) }));
    const boundaries = [...document.querySelectorAll('[data-layout-boundary]')].map((element) => ({ element, name: element.dataset.layoutBoundary || '', rect: rectOf(element) }));
    const dividers = [...document.querySelectorAll('[data-layout-divider]')].map((element) => ({ element, name: element.dataset.layoutDivider || '', rect: rectOf(element) }));
    const edgeElements = [...document.querySelectorAll('path[data-layout-edge]')];
    const arrows = [...document.querySelectorAll('[data-arrow-for]')].map((element) => ({ element, name: element.dataset.arrowFor, rect: rectOf(element) }));
    const accents = [...document.querySelectorAll('[data-layout-accent]')].map((element) => ({
      element,
      name: element.dataset.layoutAccent || '',
      nodeName: element.dataset.forNode,
      rect: rectOf(element),
    }));
    for (const accent of accents) {
      const shortSide = Math.min(accent.rect.width, accent.rect.height);
      const longSide = Math.max(accent.rect.width, accent.rect.height);
      if (shortSide > 0 && longSide / shortSide >= 4) {
        errors.push({
          type: 'decorative-accent-bar', accent: accent.name,
          size: [round(accent.rect.width), round(accent.rect.height)],
          aspectRatio: round(longSide / shortSide), maximumExclusive: 4,
        });
      }
    }
    if (nodes.length === 0) errors.push({ type: 'missing-layout-annotations', element: 'data-layout-node' });
    const edgeCount = edgeElements.length;
    if (edgeCount === 0 && !edgelessLayoutKinds.has(layoutKind)) {
      errors.push({ type: 'missing-layout-annotations', element: 'data-layout-edge' });
    }

    if (config.strict) {
      const requireUniqueNames = (items, kind) => {
        const counts = new Map();
        for (const item of items) counts.set(item.name, (counts.get(item.name) || 0) + 1);
        for (const [name, count] of counts) {
          if (!name) errors.push({ type: 'semantic-id-empty', kind });
          else if (count > 1) errors.push({ type: 'semantic-id-duplicate', kind, name, count });
        }
      };
      requireUniqueNames(nodes, 'node');
      requireUniqueNames(texts, 'text');
      requireUniqueNames(labels, 'label');
      requireUniqueNames(boundaries, 'boundary');
      requireUniqueNames(dividers, 'divider');
      requireUniqueNames(accents, 'accent');

      const edgeNames = edgeElements.map((edge) => edge.dataset.layoutEdge || '');
      const edgeNameSet = new Set(edgeNames);
      for (const name of new Set(edgeNames)) {
        const count = edgeNames.filter((candidate) => candidate === name).length;
        if (!name) errors.push({ type: 'semantic-id-empty', kind: 'edge' });
        else if (count > 1) errors.push({ type: 'semantic-id-duplicate', kind: 'edge', name, count });
      }
      for (const edge of edgeElements) {
        const edgeName = edge.dataset.layoutEdge || null;
        if (!edge.dataset.from || !edge.dataset.to) errors.push({ type: 'edge-endpoint-annotation', edge: edgeName, from: edge.dataset.from || null, to: edge.dataset.to || null });
        if (!edge.dataset.flow) errors.push({ type: 'edge-flow-annotation', edge: edgeName });
      }
      for (const label of labels) {
        const edgeRef = label.element.dataset.edgeRef;
        if (!edgeRef) errors.push({ type: 'label-edge-annotation', label: label.name });
        else if (!edgeNameSet.has(edgeRef)) errors.push({ type: 'label-edge-missing', label: label.name, edge: edgeRef });
      }
      const arrowNames = arrows.map((arrow) => arrow.name || '');
      for (const name of new Set(arrowNames)) {
        const count = arrowNames.filter((candidate) => candidate === name).length;
        if (!name) errors.push({ type: 'semantic-id-empty', kind: 'arrow' });
        else if (count > 1) errors.push({ type: 'semantic-id-duplicate', kind: 'arrow', name, count });
        if (name && !edgeNameSet.has(name)) errors.push({ type: 'arrow-edge-missing', arrow: name });
      }
      const allowedTextRoles = new Set(['title', 'subtitle', 'legend', 'note', 'footer']);
      for (const text of texts) {
        const owners = [text.element.dataset.nodeRef, text.element.dataset.boundaryRef, text.element.dataset.layoutRole].filter(Boolean);
        if (owners.length === 0) errors.push({ type: 'text-owner-annotation', text: text.name });
        if (owners.length > 1 && !text.element.dataset.boundaryRef) errors.push({ type: 'text-owner-ambiguous', text: text.name });
        const role = text.element.dataset.layoutRole;
        if (role && !allowedTextRoles.has(role)) errors.push({ type: 'text-role-invalid', text: text.name, role, allowed: [...allowedTextRoles] });
      }
      for (const node of nodes) {
        if (!texts.some((text) => text.element.dataset.nodeRef === node.name)) errors.push({ type: 'node-text-annotation', node: node.name });
      }
      const walker = document.createTreeWalker(document.body || root, NodeFilter.SHOW_TEXT);
      const looseParents = new Set();
      while (walker.nextNode()) {
        const value = walker.currentNode.nodeValue?.trim();
        if (!value) continue;
        const parent = walker.currentNode.parentElement;
        if (!parent || parent.closest('style,script,title,desc,defs,marker')) continue;
        if (!parent.closest('[data-layout-text],[data-layout-label]')) looseParents.add(parent);
      }
      for (const parent of looseParents) errors.push({ type: 'unannotated-layout-text', element: nameOf(parent), sample: (parent.textContent || '').trim().slice(0, 80) });
    }

    if (config.boundaryClearance > 0) {
      for (const text of texts) {
        const boundaryRef = text.element.dataset.boundaryRef;
        if (!boundaryRef) continue;
        const boundary = boundaries.find((candidate) => candidate.name === boundaryRef);
        if (!boundary) {
          errors.push({ type: 'text-boundary-missing', text: text.name, boundary: boundaryRef });
          continue;
        }
        const side = text.element.dataset.boundarySide;
        const actual = side === 'left' ? boundary.rect.left - text.rect.right
          : side === 'right' ? text.rect.left - boundary.rect.right
          : side === 'above' ? boundary.rect.top - text.rect.bottom
          : side === 'below' ? text.rect.top - boundary.rect.bottom
          : Number.NaN;
        if (!Number.isFinite(actual)) {
          errors.push({ type: 'text-boundary-side', text: text.name, boundary: boundary.name, side: side || null, allowed: ['left', 'right', 'above', 'below'] });
        } else if (actual < config.boundaryClearance) {
          errors.push({ type: 'text-boundary-clearance', text: text.name, boundary: boundary.name, side, actual: round(actual), required: config.boundaryClearance });
        }
      }
    }

    if (config.dividerNodeClearance > 0) {
      for (const divider of dividers) {
        for (const node of nodes) {
          const dx = Math.max(divider.rect.left - node.rect.right, node.rect.left - divider.rect.right, 0);
          const dy = Math.max(divider.rect.top - node.rect.bottom, node.rect.top - divider.rect.bottom, 0);
          const actual = Math.hypot(dx, dy);
          if (actual < config.dividerNodeClearance) {
            errors.push({
              type: 'divider-node-clearance', divider: divider.name, node: node.name,
              actual: round(actual), required: config.dividerNodeClearance,
            });
          }
        }
      }
    }

    if (config.textNodeClearance > 0) {
      for (const text of texts) {
        const nodeRef = text.element.dataset.nodeRef;
        if (!nodeRef) continue;
        const node = nodes.find((candidate) => candidate.name === nodeRef);
        if (!node) {
          errors.push({ type: 'text-node-missing', text: text.name, node: nodeRef });
          continue;
        }
        const clearances = {
          left: text.rect.left - node.rect.left,
          top: text.rect.top - node.rect.top,
          right: node.rect.right - text.rect.right,
          bottom: node.rect.bottom - text.rect.bottom,
        };
        const actual = Math.min(...Object.values(clearances));
        if (actual < config.textNodeClearance) {
          errors.push({
            type: 'text-node-clearance', text: text.name, node: node.name,
            actual: round(actual), required: config.textNodeClearance,
            sides: Object.fromEntries(Object.entries(clearances).map(([key, value]) => [key, round(value)])),
          });
        }
      }
    }

    for (let i = 0; i < nodes.length; i += 1) {
      for (let j = i + 1; j < nodes.length; j += 1) {
        const a = nodes[i], b = nodes[j], o = overlap(a.rect, b.rect);
        if (o.x > 1 && o.y > 1) {
          errors.push({ type: 'node-overlap', elements: [a.name, b.name], overlap: { x: round(o.x), y: round(o.y) } });
          continue;
        }
        const verticalProjection = o.y > 1;
        const horizontalProjection = o.x > 1;
        const horizontalGap = Math.max(b.rect.left - a.rect.right, a.rect.left - b.rect.right, 0);
        const verticalGap = Math.max(b.rect.top - a.rect.bottom, a.rect.top - b.rect.bottom, 0);
        if (verticalProjection && horizontalGap < config.minGap) {
          errors.push({ type: 'node-gap', elements: [a.name, b.name], axis: 'horizontal', actual: round(horizontalGap), required: config.minGap });
        } else if (horizontalProjection && verticalGap < config.minGap) {
          errors.push({ type: 'node-gap', elements: [a.name, b.name], axis: 'vertical', actual: round(verticalGap), required: config.minGap });
        }
      }
    }

    for (const label of labels) {
      for (const node of nodes) {
        const expanded = {
          left: label.rect.left - config.labelClearance,
          top: label.rect.top - config.labelClearance,
          right: label.rect.right + config.labelClearance,
          bottom: label.rect.bottom + config.labelClearance,
        };
        if (intersects(expanded, node.rect, 1)) {
          errors.push({
            type: config.labelClearance > 0 ? 'label-node-clearance' : 'label-node-overlap',
            elements: [label.name, node.name],
            required: config.labelClearance,
          });
        }
      }
    }

    if (config.labelGap > 0) {
      for (let i = 0; i < labels.length; i += 1) {
        for (let j = i + 1; j < labels.length; j += 1) {
          const a = labels[i], b = labels[j];
          const expandedA = { left: a.rect.left - config.labelGap, top: a.rect.top - config.labelGap, right: a.rect.right + config.labelGap, bottom: a.rect.bottom + config.labelGap };
          if (intersects(expandedA, b.rect)) errors.push({ type: 'label-label-clearance', elements: [a.name, b.name], required: config.labelGap });
        }
      }
    }

    if (config.accentBorderClearance > 0) {
      for (const accent of accents) {
        const node = nodes.find((candidate) => candidate.name === accent.nodeName);
        if (!node) {
          errors.push({ type: 'accent-missing-node', accent: accent.name, node: accent.nodeName || null });
          continue;
        }
        const clearances = {
          left: accent.rect.left - node.rect.left,
          top: accent.rect.top - node.rect.top,
          right: node.rect.right - accent.rect.right,
          bottom: node.rect.bottom - accent.rect.bottom,
        };
        const actual = Math.min(...Object.values(clearances));
        if (actual < config.accentBorderClearance) {
          errors.push({
            type: 'accent-border-clearance', accent: accent.name, node: node.name,
            actual: round(actual), required: config.accentBorderClearance,
            sides: Object.fromEntries(Object.entries(clearances).map(([key, value]) => [key, round(value)])),
          });
        }
      }
    }

    if (config.accentTextClearance > 0) {
      for (const accent of accents) {
        const ownedTexts = texts.filter((text) => text.element.dataset.nodeRef === accent.nodeName);
        for (const text of ownedTexts) {
          const dx = Math.max(text.rect.left - accent.rect.right, accent.rect.left - text.rect.right, 0);
          const dy = Math.max(text.rect.top - accent.rect.bottom, accent.rect.top - text.rect.bottom, 0);
          const actual = Math.hypot(dx, dy);
          if (actual < config.accentTextClearance) {
            errors.push({
              type: 'accent-text-clearance', accent: accent.name, text: text.name, node: accent.nodeName || null,
              actual: round(actual), required: config.accentTextClearance,
            });
          }
        }
      }
    }

    const overflowElements = [...document.querySelectorAll('[data-layout-node], [data-layout-text], [data-layout-label], [data-layout-accent], [data-layout-divider], [data-arrow-for]')];
    for (const element of overflowElements) {
      const r = rectOf(element);
      if (config.strict && isVisible(element) && (r.width <= 0.5 || r.height <= 0.5)) {
        errors.push({ type: 'semantic-element-empty', element: nameOf(element), rect: { width: round(r.width), height: round(r.height) } });
      }
      if (element.scrollWidth > element.clientWidth + 1 || element.scrollHeight > element.clientHeight + 1) {
        errors.push({
          type: 'content-overflow', element: nameOf(element),
          client: [element.clientWidth, element.clientHeight], scroll: [element.scrollWidth, element.scrollHeight],
        });
      }
      if (r.left < -1 || r.top < -1 || r.right > config.width + 1 || r.bottom > config.height + 1) {
        errors.push({ type: 'canvas-overflow', element: nameOf(element), rect: Object.fromEntries(Object.entries(r).map(([k,v]) => [k, round(v)])) });
      } else if (config.canvasClearance > 0 && (r.left < config.canvasClearance || r.top < config.canvasClearance || r.right > config.width - config.canvasClearance || r.bottom > config.height - config.canvasClearance)) {
        errors.push({ type: 'canvas-clearance', element: nameOf(element), required: config.canvasClearance, rect: Object.fromEntries(Object.entries(r).map(([k,v]) => [k, round(v)])) });
      }
    }

    if (config.minFontSize > 0) {
      for (const item of [...texts, ...labels]) {
        const walker = document.createTreeWalker(item.element, NodeFilter.SHOW_TEXT);
        const measured = [];
        while (walker.nextNode()) {
          if (!walker.currentNode.nodeValue?.trim()) continue;
          const parent = walker.currentNode.parentElement;
          if (!parent || !isVisible(parent)) continue;
          const size = Number.parseFloat(getComputedStyle(parent).fontSize);
          if (Number.isFinite(size)) measured.push(size);
        }
        const actual = measured.length ? Math.min(...measured) : Number.parseFloat(getComputedStyle(item.element).fontSize);
        if (Number.isFinite(actual) && actual < config.minFontSize) errors.push({ type: 'font-size-minimum', element: item.name, actual: round(actual), required: config.minFontSize });
      }
    }

    const sampledEdges = [];
    for (const edge of edgeElements) {
      const edgeName = edge.dataset.layoutEdge || 'edge';
      const allowed = new Set([edge.dataset.from, edge.dataset.to].filter(Boolean));
      const matrix = edge.getScreenCTM();
      const length = edge.getTotalLength();
      if (config.minEdgeLength > 0 && length < config.minEdgeLength) {
        errors.push({ type: 'edge-too-short', edge: edgeName, actual: round(length), required: config.minEdgeLength });
      }
      const strokeWidth = Number.parseFloat(getComputedStyle(edge).strokeWidth) || 1;
      const markerInfo = (property) => {
        const markerValue = getComputedStyle(edge)[property] || '';
        const markerId = markerValue.match(/#([^\")]+)/)?.[1];
        const marker = markerId ? document.getElementById(markerId) : null;
        if (!marker) return null;
        const scale = marker.markerUnits?.baseVal === 2 ? strokeWidth : 1;
        const size = Math.max(marker.markerWidth.baseVal.value, marker.markerHeight.baseVal.value) * scale;
        const boxes = [...marker.querySelectorAll('path, polygon, polyline, rect, circle, ellipse')].map((shape) => {
          try { return shape.getBBox(); } catch { return null; }
        }).filter(Boolean);
        const bbox = boxes.length ? {
          left: Math.min(...boxes.map((box) => box.x)),
          top: Math.min(...boxes.map((box) => box.y)),
          right: Math.max(...boxes.map((box) => box.x + box.width)),
          bottom: Math.max(...boxes.map((box) => box.y + box.height)),
        } : null;
        const viewBox = marker.viewBox?.baseVal;
        const scaleX = scale * (viewBox?.width > 0 ? marker.markerWidth.baseVal.value / viewBox.width : 1);
        const scaleY = scale * (viewBox?.height > 0 ? marker.markerHeight.baseVal.value / viewBox.height : 1);
        return {
          size, extent: size + strokeWidth / 2, bbox, scaleX, scaleY,
          refX: marker.refX.baseVal.value, refY: marker.refY.baseVal.value,
        };
      };
      const markerStart = markerInfo('markerStart');
      const markerEnd = markerInfo('markerEnd');
      const explicitArrow = document.querySelector('[data-arrow-for="' + CSS.escape(edgeName) + '"]');
      const sourceNode = nodes.find((candidate) => candidate.name === edge.dataset.from);
      const targetNode = nodes.find((candidate) => candidate.name === edge.dataset.to);
      const startPoint = edge.getPointAtLength(0).matrixTransform(matrix);
      const endPoint = edge.getPointAtLength(length).matrixTransform(matrix);
      const flow = edge.dataset.flow;
      const lineCap = getComputedStyle(edge).strokeLinecap;
      const capExtension = ['round', 'square'].includes(lineCap) ? strokeWidth / 2 : 0;
      if (!sourceNode) errors.push({ type: 'edge-missing-source', edge: edgeName, source: edge.dataset.from || null });
      if (!targetNode) errors.push({ type: 'edge-missing-target', edge: edgeName, target: edge.dataset.to || null });
      if (flow) {
        if (!['down', 'up', 'left', 'right'].includes(flow)) {
          errors.push({ type: 'edge-invalid-flow', edge: edgeName, flow });
        }
        if (markerStart || (!markerEnd && !explicitArrow) || (markerEnd && explicitArrow)) {
          errors.push({ type: 'edge-arrow-target', edge: edgeName, required: 'exactly one target-end marker or explicit arrow', markerStart: Boolean(markerStart), markerEnd: Boolean(markerEnd), explicitArrow: Boolean(explicitArrow) });
        }
        if (sourceNode && targetNode && ['down', 'up', 'left', 'right'].includes(flow)) {
          const epsilon = 1;
          const projectionContains = (rect, point, axis) => axis === 'x'
            ? point.x >= rect.left - epsilon && point.x <= rect.right + epsilon
            : point.y >= rect.top - epsilon && point.y <= rect.bottom + epsilon;
          let ordered = true;
          let anchored = true;
          if (flow === 'down') {
            ordered = endPoint.y > startPoint.y + epsilon;
            anchored = projectionContains(sourceNode.rect, startPoint, 'x') && projectionContains(targetNode.rect, endPoint, 'x') && startPoint.y >= sourceNode.rect.bottom - epsilon && endPoint.y <= targetNode.rect.top + epsilon;
          } else if (flow === 'up') {
            ordered = endPoint.y < startPoint.y - epsilon;
            anchored = projectionContains(sourceNode.rect, startPoint, 'x') && projectionContains(targetNode.rect, endPoint, 'x') && startPoint.y <= sourceNode.rect.top + epsilon && endPoint.y >= targetNode.rect.bottom - epsilon;
          } else if (flow === 'right') {
            ordered = endPoint.x > startPoint.x + epsilon;
            anchored = projectionContains(sourceNode.rect, startPoint, 'y') && projectionContains(targetNode.rect, endPoint, 'y') && startPoint.x >= sourceNode.rect.right - epsilon && endPoint.x <= targetNode.rect.left + epsilon;
          } else if (flow === 'left') {
            ordered = endPoint.x < startPoint.x - epsilon;
            anchored = projectionContains(sourceNode.rect, startPoint, 'y') && projectionContains(targetNode.rect, endPoint, 'y') && startPoint.x <= sourceNode.rect.left + epsilon && endPoint.x >= targetNode.rect.right - epsilon;
          }
          if (!ordered) errors.push({ type: 'edge-direction', edge: edgeName, flow, start: { x: round(startPoint.x), y: round(startPoint.y) }, end: { x: round(endPoint.x), y: round(endPoint.y) } });
          if (!anchored) errors.push({ type: 'edge-anchor', edge: edgeName, flow, source: sourceNode.name, target: targetNode.name });
        }
      }
      if (flow && ['down', 'up', 'left', 'right'].includes(flow)) {
        if (explicitArrow && config.arrowTangentTolerance > 0) {
          const tangentAngleAt = (distanceFromEnd) => {
            const center = Math.max(0, length - Math.min(distanceFromEnd, length));
            const radius = Math.min(3, center, length - center);
            const before = edge.getPointAtLength(Math.max(0, center - radius)).matrixTransform(matrix);
            const after = edge.getPointAtLength(Math.min(length, center + radius)).matrixTransform(matrix);
            const dx = after.x - before.x;
            const dy = after.y - before.y;
            const primary = flow === 'right' ? dx : flow === 'left' ? -dx : flow === 'down' ? dy : -dy;
            const cross = flow === 'right' || flow === 'left' ? Math.abs(dy) : Math.abs(dx);
            return primary > 0 ? Math.atan2(cross, primary) * 180 / Math.PI : 180;
          };
          // Check both the arrow-base join and the approach before it. A tiny
          // axis-aligned tail must not hide a diagonal curve-to-shaft kink.
          const probes = [3, 9]
            .map(distance => Math.min(distance, length / 2))
            .filter((distance, index, values) => index === 0 || distance !== values[index - 1]);
          const measured = probes.map(distance => ({ distance, angle: tangentAngleAt(distance) }));
          const worst = measured.reduce((current, candidate) => candidate.angle > current.angle ? candidate : current);
          if (worst.angle > config.arrowTangentTolerance) {
            errors.push({
              type: 'arrow-tangent-misaligned', edge: edgeName, flow,
              actual: round(worst.angle), allowed: config.arrowTangentTolerance,
              sampleDistance: round(worst.distance),
            });
          }
        }
        if (markerEnd?.bbox) {
          if (config.arrowJoinTolerance > 0) {
            const baseOffset = (markerEnd.refX - markerEnd.bbox.left) * markerEnd.scaleX;
            if (baseOffset < -config.arrowJoinTolerance) {
              errors.push({
                type: 'arrow-shaft-gap', edge: edgeName, flow,
                actual: round(-baseOffset), allowed: config.arrowJoinTolerance,
                marker: true,
              });
            } else if (baseOffset > config.arrowJoinTolerance) {
              errors.push({
                type: 'arrow-shaft-overlap', edge: edgeName, flow,
                actual: round(baseOffset), allowed: config.arrowJoinTolerance,
                marker: true,
              });
            }
            const centerOffset = Math.abs(markerEnd.refY - (markerEnd.bbox.top + markerEnd.bbox.bottom) / 2) * markerEnd.scaleY;
            if (centerOffset > config.arrowJoinTolerance) {
              errors.push({
                type: 'arrow-shaft-misaligned', edge: edgeName, flow,
                actual: round(centerOffset), allowed: config.arrowJoinTolerance,
                marker: true,
              });
            }
          }
          const tipAdvance = flow === 'right' ? (markerEnd.bbox.right - markerEnd.refX) * markerEnd.scaleX
            : flow === 'left' ? (markerEnd.refX - markerEnd.bbox.left) * markerEnd.scaleX
            : flow === 'down' ? (markerEnd.bbox.bottom - markerEnd.refY) * markerEnd.scaleY
            : (markerEnd.refY - markerEnd.bbox.top) * markerEnd.scaleY;
          const overrun = capExtension - tipAdvance;
          if (overrun > config.markerShaftTolerance) {
            errors.push({
              type: 'marker-shaft-overrun', edge: edgeName, flow, lineCap,
              actual: round(overrun), allowed: config.markerShaftTolerance,
              capExtension: round(capExtension), markerTipAdvance: round(tipAdvance),
            });
          }
        } else if (explicitArrow) {
          const arrowRect = rectOf(explicitArrow);
          const shaftTip = flow === 'right' ? endPoint.x + capExtension
            : flow === 'left' ? endPoint.x - capExtension
            : flow === 'down' ? endPoint.y + capExtension
            : endPoint.y - capExtension;
          const arrowTip = flow === 'right' ? arrowRect.right
            : flow === 'left' ? arrowRect.left
            : flow === 'down' ? arrowRect.bottom
            : arrowRect.top;
          const overrun = flow === 'right' || flow === 'down' ? shaftTip - arrowTip : arrowTip - shaftTip;
          if (overrun > config.markerShaftTolerance) {
            errors.push({
              type: 'marker-shaft-overrun', edge: edgeName, flow, lineCap,
              actual: round(overrun), allowed: config.markerShaftTolerance,
              capExtension: round(capExtension), explicitArrow: true,
            });
          }
          if (config.arrowJoinTolerance > 0) {
            const arrowBase = flow === 'right' ? arrowRect.left
              : flow === 'left' ? arrowRect.right
              : flow === 'down' ? arrowRect.top
              : arrowRect.bottom;
            const joinOffset = flow === 'right' || flow === 'down' ? shaftTip - arrowBase : arrowBase - shaftTip;
            if (joinOffset < -config.arrowJoinTolerance) {
              errors.push({
                type: 'arrow-shaft-gap', edge: edgeName, flow,
                actual: round(-joinOffset), allowed: config.arrowJoinTolerance,
              });
            } else if (joinOffset > config.arrowJoinTolerance) {
              errors.push({
                type: 'arrow-shaft-overlap', edge: edgeName, flow,
                actual: round(joinOffset), allowed: config.arrowJoinTolerance,
              });
            }
            const shaftCenter = flow === 'right' || flow === 'left' ? endPoint.y : endPoint.x;
            const arrowCenter = flow === 'right' || flow === 'left'
              ? (arrowRect.top + arrowRect.bottom) / 2
              : (arrowRect.left + arrowRect.right) / 2;
            const centerOffset = Math.abs(shaftCenter - arrowCenter);
            if (centerOffset > config.arrowJoinTolerance) {
              errors.push({
                type: 'arrow-shaft-misaligned', edge: edgeName, flow,
                actual: round(centerOffset), allowed: config.arrowJoinTolerance,
              });
            }
          }
          const edgeStroke = getComputedStyle(edge).stroke;
          const arrowFill = getComputedStyle(explicitArrow).fill;
          if (edgeStroke !== arrowFill) {
            errors.push({ type: 'arrow-color-mismatch', edge: edgeName, edgeStroke, arrowFill });
          }
        }
      }
      for (const marker of [markerStart, markerEnd].filter(Boolean)) {
        if (config.maxMarkerSize > 0 && marker.size > config.maxMarkerSize) {
          errors.push({ type: 'marker-too-large', edge: edgeName, actual: round(marker.size), requiredMax: config.maxMarkerSize });
        }
      }
      if (config.markerClearance > 0) {
        const markerChecks = [
          { info: markerStart, nodeName: edge.dataset.from, distance: 0, endpoint: 'start' },
          { info: markerEnd, nodeName: edge.dataset.to, distance: length, endpoint: 'end' },
        ];
        for (const check of markerChecks) {
          if (!check.info || !check.nodeName) continue;
          const node = nodes.find((candidate) => candidate.name === check.nodeName);
          if (!node) continue;
          const point = edge.getPointAtLength(check.distance).matrixTransform(matrix);
          const directionalExtent = check.endpoint === 'end' && check.info.bbox && ['down', 'up', 'left', 'right'].includes(flow)
            ? (flow === 'right' ? (check.info.bbox.right - check.info.refX) * check.info.scaleX
              : flow === 'left' ? (check.info.refX - check.info.bbox.left) * check.info.scaleX
              : flow === 'down' ? (check.info.bbox.bottom - check.info.refY) * check.info.scaleY
              : (check.info.refY - check.info.bbox.top) * check.info.scaleY)
            : check.info.extent;
          const markerExtent = Math.max(0, directionalExtent);
          const actual = pointDistanceToRect(point, node.rect) - markerExtent;
          if (actual < config.markerClearance) {
            errors.push({
              type: 'marker-node-clearance', edge: edgeName, node: node.name, endpoint: check.endpoint,
              actual: round(actual), required: config.markerClearance, markerExtent: round(markerExtent),
            });
          }
        }
        if (explicitArrow && targetNode && flow && ['down', 'up', 'left', 'right'].includes(flow)) {
          const arrowRect = rectOf(explicitArrow);
          const tipPoint = flow === 'right' ? { x: arrowRect.right, y: (arrowRect.top + arrowRect.bottom) / 2 }
            : flow === 'left' ? { x: arrowRect.left, y: (arrowRect.top + arrowRect.bottom) / 2 }
            : flow === 'down' ? { x: (arrowRect.left + arrowRect.right) / 2, y: arrowRect.bottom }
            : { x: (arrowRect.left + arrowRect.right) / 2, y: arrowRect.top };
          const actual = pointDistanceToRect(tipPoint, targetNode.rect);
          if (actual < config.markerClearance) {
            errors.push({
              type: 'marker-node-clearance', edge: edgeName, node: targetNode.name, endpoint: 'end',
              actual: round(actual), required: config.markerClearance, explicitArrow: true,
            });
          }
        }
      }
      const step = Math.max(2, Math.min(6, length / 100));
      const sampledPoints = [];
      const hit = new Set();
      const clearanceHit = new Set();
      const connectorLabelHit = new Map();
      for (let distance = 0; distance <= length; distance += step) {
        const point = edge.getPointAtLength(distance).matrixTransform(matrix);
        sampledPoints.push({ x: point.x, y: point.y });
        if (config.connectorLabelClearance > 0) {
          for (const label of labels) {
            const actual = pointDistanceToRect(point, label.rect) - strokeWidth / 2;
            const previous = connectorLabelHit.get(label.name);
            if (previous === undefined || actual < previous) connectorLabelHit.set(label.name, actual);
          }
        }
        for (const node of nodes) {
          const r = node.rect;
          if (allowed.has(node.name)) {
            if (config.edgeClearance > 0) {
              const dx = Math.max(r.left - point.x, 0, point.x - r.right);
              const dy = Math.max(r.top - point.y, 0, point.y - r.bottom);
              if (Math.hypot(dx, dy) < config.edgeClearance) clearanceHit.add(node.name);
            }
            continue;
          }
          if (point.x > r.left + 2 && point.x < r.right - 2 && point.y > r.top + 2 && point.y < r.bottom - 2) hit.add(node.name);
        }
      }
      if (sampledPoints.length === 0 || sampledPoints.at(-1).x !== endPoint.x || sampledPoints.at(-1).y !== endPoint.y) sampledPoints.push({ x: endPoint.x, y: endPoint.y });
      sampledEdges.push({ name: edgeName, from: edge.dataset.from, to: edge.dataset.to, points: sampledPoints });
      if (config.connectorLabelClearance > 0) {
        const markerChecks = [
          { info: markerStart, distance: 0 },
          { info: markerEnd, distance: length },
        ];
        for (const check of markerChecks) {
          if (!check.info) continue;
          const point = edge.getPointAtLength(check.distance).matrixTransform(matrix);
          for (const label of labels) {
            const actual = pointDistanceToRect(point, label.rect) - check.info.extent;
            const previous = connectorLabelHit.get(label.name);
            if (previous === undefined || actual < previous) connectorLabelHit.set(label.name, actual);
          }
        }
        for (const [labelName, actual] of connectorLabelHit) {
          if (actual < config.connectorLabelClearance) {
            errors.push({
              type: 'connector-label-clearance', edge: edgeName, label: labelName,
              actual: round(actual), required: config.connectorLabelClearance,
            });
          }
        }
      }
      for (const nodeName of hit) errors.push({ type: 'edge-node-crossing', edge: edgeName, node: nodeName });
      for (const nodeName of clearanceHit) errors.push({ type: 'edge-endpoint-clearance', edge: edgeName, node: nodeName, required: config.edgeClearance });
    }

    if (config.maxEdgeCrossings >= 0) {
      const orientation = (a, b, c) => (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
      const crosses = (a, b, c, d) => {
        const epsilon = 0.01;
        const o1 = orientation(a, b, c), o2 = orientation(a, b, d), o3 = orientation(c, d, a), o4 = orientation(c, d, b);
        const onSegment = (p, q, r) => q.x >= Math.min(p.x, r.x) - epsilon && q.x <= Math.max(p.x, r.x) + epsilon && q.y >= Math.min(p.y, r.y) - epsilon && q.y <= Math.max(p.y, r.y) + epsilon;
        const proper = ((o1 > epsilon && o2 < -epsilon) || (o1 < -epsilon && o2 > epsilon)) && ((o3 > epsilon && o4 < -epsilon) || (o3 < -epsilon && o4 > epsilon));
        return proper || (Math.abs(o1) <= epsilon && onSegment(a, c, b)) || (Math.abs(o2) <= epsilon && onSegment(a, d, b)) || (Math.abs(o3) <= epsilon && onSegment(c, a, d)) || (Math.abs(o4) <= epsilon && onSegment(c, b, d));
      };
      const crossingPairs = [];
      for (let i = 0; i < sampledEdges.length; i += 1) {
        for (let j = i + 1; j < sampledEdges.length; j += 1) {
          const a = sampledEdges[i], b = sampledEdges[j];
          if ([a.from, a.to].some((endpoint) => endpoint && (endpoint === b.from || endpoint === b.to))) continue;
          let found = false;
          for (let ai = 1; ai < a.points.length && !found; ai += 1) {
            for (let bi = 1; bi < b.points.length; bi += 1) {
              if (crosses(a.points[ai - 1], a.points[ai], b.points[bi - 1], b.points[bi])) { found = true; break; }
            }
          }
          if (found) crossingPairs.push([a.name, b.name]);
        }
      }
      if (crossingPairs.length > config.maxEdgeCrossings) errors.push({ type: 'edge-edge-crossings', actual: crossingPairs.length, requiredMax: config.maxEdgeCrossings, pairs: crossingPairs });
    }

    return {
      ok: errors.length === 0,
      viewport: { width: innerWidth, height: innerHeight, devicePixelRatio },
      counts: { nodes: nodes.length, labels: labels.length, texts: texts.length, boundaries: boundaries.length, dividers: dividers.length, accents: accents.length, edges: edgeCount, arrows: arrows.length },
      strict: config.strict,
      minGap: config.minGap,
      edgeClearance: config.edgeClearance,
      markerClearance: config.markerClearance,
      arrowJoinTolerance: config.arrowJoinTolerance,
      arrowTangentTolerance: config.arrowTangentTolerance,
      markerShaftTolerance: config.markerShaftTolerance,
      labelClearance: config.labelClearance,
      labelGap: config.labelGap,
      connectorLabelClearance: config.connectorLabelClearance,
      accentBorderClearance: config.accentBorderClearance,
      accentTextClearance: config.accentTextClearance,
      boundaryClearance: config.boundaryClearance,
      dividerNodeClearance: config.dividerNodeClearance,
      textNodeClearance: config.textNodeClearance,
      canvasClearance: config.canvasClearance,
      minFontSize: config.minFontSize,
      maxEdgeCrossings: config.maxEdgeCrossings,
      minEdgeLength: config.minEdgeLength,
      maxMarkerSize: config.maxMarkerSize,
      errors,
    };
  })()`;
}

export async function validateDiagramFromArgv(argv) {
  const options = parseArgs(argv);
  const htmlPath = path.resolve(options.html);
  const profileRoot = process.platform === "darwin" ? "/private/tmp" : tmpdir();
  const profileDir = await mkdtemp(path.join(profileRoot, "diagram-layout-gate-"));
  const debuggingPort = await getFreePort();
  const playwrightRoot = path.join(homedir(), "Library/Caches/ms-playwright");
  const playwrightChromes = process.platform === "darwin" && existsSync(playwrightRoot)
    ? readdirSync(playwrightRoot)
      .filter((name) => name.startsWith("chromium-"))
      .sort((a, b) => b.localeCompare(a, undefined, { numeric: true }))
      .map((name) => path.join(playwrightRoot, name, "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"))
    : [];
  const chromePath = [
    process.env.CHROME_PATH,
    ...playwrightChromes,
    process.platform === "darwin" ? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" : "google-chrome",
  ].filter(Boolean).find((candidate) => candidate === "google-chrome" || existsSync(candidate));
  const chromeArgs = [
    "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--no-default-browser-check",
    `--remote-debugging-port=${debuggingPort}`, "--remote-debugging-address=127.0.0.1", `--user-data-dir=${profileDir}`, "about:blank",
  ];
  const { MallocNanoZone: _mallocNanoZone, ...chromeEnv } = process.env;
  const chrome = spawn(chromePath, chromeArgs, {
    env: chromeEnv,
    stdio: process.env.DIAGRAM_VALIDATOR_DEBUG ? ["ignore", "ignore", "inherit"] : "ignore",
  });
  if (process.env.DIAGRAM_VALIDATOR_DEBUG) console.error(`Chrome launcher pid=${chrome.pid} port=${debuggingPort} path=${chromePath}`);

  try {
    const port = await waitForDevTools(debuggingPort, chrome);
    const target = await fetch(`http://127.0.0.1:${port}/json/new?${encodeURIComponent(pathToFileURL(htmlPath).href)}`, { method: "PUT" }).then((response) => response.json());
    const cdp = createCdpSocket(target.webSocketDebuggerUrl);
    await cdp.ready;
    await cdp.send("Page.enable");
    await cdp.send("Runtime.enable");
    await cdp.send("Emulation.setDeviceMetricsOverride", {
      width: options.width, height: options.height, deviceScaleFactor: options.scale, mobile: false,
    });
    const loaded = cdp.once("Page.loadEventFired");
    await cdp.send("Page.reload", { ignoreCache: true });
    await loaded;
    await cdp.send("Runtime.evaluate", { expression: "document.fonts && document.fonts.ready", awaitPromise: true });
    const evaluation = await cdp.send("Runtime.evaluate", {
      expression: gateExpression(options), returnByValue: true, awaitPromise: true,
    });
    if (options.screenshot) {
      const screenshot = await cdp.send("Page.captureScreenshot", { format: "png", fromSurface: true });
      await writeFile(path.resolve(options.screenshot), Buffer.from(screenshot.data, "base64"));
    }
    cdp.close();
    const report = evaluation.result.value;
    return { file: htmlPath, screenshot: options.screenshot ? path.resolve(options.screenshot) : null, ...report };
  } finally {
    await stopChrome(chrome);
    await rm(profileDir, { recursive: true, force: true, maxRetries: 8, retryDelay: 100 });
  }
}

if (process.argv[1] && realpathSync(fileURLToPath(import.meta.url)) === realpathSync(process.argv[1])) {
  validateDiagramFromArgv(process.argv.slice(2)).then((report) => {
    console.log(JSON.stringify(report, null, 2));
    if (!report.ok) process.exitCode = 1;
  }).catch((error) => {
    console.error(error.stack || error.message);
    process.exitCode = 2;
  });
}
