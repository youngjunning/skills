#!/usr/bin/env swift
// OCR candidate masks for macOS. Never print recognized text or image metadata.
import Foundation
import ImageIO
import Vision

guard CommandLine.arguments.count == 2 else {
    fputs("Usage: swift scan_macos.swift <image>\n", stderr)
    exit(2)
}

let path = CommandLine.arguments[1]
let url = URL(fileURLWithPath: path)
guard let source = CGImageSourceCreateWithURL(url as CFURL, nil),
      let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
    fputs("Could not read image\n", stderr)
    exit(1)
}

let patterns = [
    #"(?i)\b(?:authorization|bearer|api[ _-]?key|app[ _-]?secret|client[ _-]?secret|cookie|token|password|secret|access[ _-]?key)\b"#,
    #"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"#,
    #"(?<!\d)1[3-9]\d{9}(?!\d)"#,
    #"(?i)\b(?:sk-|gh[pousr]_|vkt_|AKIA|eyJ)[A-Za-z0-9_./+-]{4,}"#,
    #"(?i)[?&](?:token|key|secret|auth|signature)="#,
    #"(?:手机号|工号|邮箱|身份证|姓名|账号|账户|密钥|凭证)"#
].compactMap { try? NSRegularExpression(pattern: $0) }

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = false
request.recognitionLanguages = ["zh-Hans", "en-US"]
do {
    try VNImageRequestHandler(cgImage: image).perform([request])
} catch {
    fputs("OCR failed\n", stderr)
    exit(1)
}

var regions: [[String: Any]] = []
for observation in request.results ?? [] {
    guard let text = observation.topCandidates(1).first?.string else { continue }
    let range = NSRange(text.startIndex..<text.endIndex, in: text)
    guard patterns.contains(where: { $0.firstMatch(in: text, range: range) != nil }) else { continue }
    let box = observation.boundingBox
    let padding = 8
    let x = max(0, Int(floor(Double(box.minX) * Double(image.width))) - padding)
    let y = max(0, Int(floor((1 - Double(box.maxY)) * Double(image.height))) - padding)
    let right = min(image.width, Int(ceil(Double(box.maxX) * Double(image.width))) + padding)
    let bottom = min(image.height, Int(ceil((1 - Double(box.minY)) * Double(image.height))) + padding)
    if right > x && bottom > y {
        regions.append(["x": x, "y": y, "width": right - x, "height": bottom - y,
                        "mode": "solid"])
    }
}
let result: [String: Any] = ["width": image.width, "height": image.height,
                             "regions": regions, "reviewed": false]
guard let bytes = try? JSONSerialization.data(withJSONObject: result, options: [.prettyPrinted, .sortedKeys]),
      let output = String(data: bytes, encoding: .utf8) else {
    fputs("Could not serialize masks\n", stderr)
    exit(1)
}
print(output)
