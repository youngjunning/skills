#!/usr/bin/env node

import { realpathSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { validateDiagramFromArgv } from "./validate_diagram_layout.mjs";

const FORMAL_ARCHITECTURE_PRESET = [
  "--strict",
  "--min-gap", "48",
  "--edge-clearance", "12",
  "--marker-clearance", "12",
  "--arrow-join-tolerance", "2",
  "--arrow-tangent-tolerance", "8",
  "--marker-shaft-tolerance", "0.25",
  "--label-clearance", "8",
  "--label-gap", "8",
  "--connector-label-clearance", "16",
  "--accent-border-clearance", "12",
  "--accent-text-clearance", "8",
  "--boundary-clearance", "24",
  "--divider-node-clearance", "16",
  "--text-node-clearance", "18",
  "--canvas-clearance", "24",
  "--min-font-size", "16",
  "--max-edge-crossings", "0",
  "--min-edge-length", "48",
  "--max-marker-size", "16",
];

export async function validateArchitectureDiagramFromArgv(argv) {
  if (argv.length === 0) {
    throw new Error("Usage: validate_architecture_diagram.mjs <diagram.html-or-svg> [layout overrides] [--screenshot output.png]");
  }
  const [input, ...overrides] = argv;
  return validateDiagramFromArgv([input, ...FORMAL_ARCHITECTURE_PRESET, ...overrides]);
}

if (process.argv[1] && realpathSync(fileURLToPath(import.meta.url)) === realpathSync(process.argv[1])) {
  validateArchitectureDiagramFromArgv(process.argv.slice(2)).then((report) => {
    console.log(JSON.stringify(report, null, 2));
    if (!report.ok) process.exitCode = 1;
  }).catch((error) => {
    console.error(error.stack || error.message);
    process.exitCode = 2;
  });
}
