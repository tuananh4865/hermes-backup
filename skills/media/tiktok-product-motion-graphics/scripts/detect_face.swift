// detect_face.swift — Apple Vision framework face detection for HyperFrames PIP crop
// Compile: swiftc detect_face.swift -o detect_face
// Usage: ./detect_face <frame.jpg>
// Output: FACE x y w h (normalized 0-1, Vision bottom-left origin)
// Convert y_top = 1.0 - y - h before using as ffmpeg crop coords.

import Foundation
import Vision
import AppKit

guard CommandLine.arguments.count >= 2 else {
    print("Usage: detect_face <frame.jpg>")
    exit(1)
}

let url = URL(fileURLWithPath: CommandLine.arguments[1])
guard let image = NSImage(contentsOf: url),
      let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("ERROR: cannot load image at \(CommandLine.arguments[1])")
    exit(1)
}

let request = VNDetectFaceRectanglesRequest { request, _ in
    guard let observations = request.results as? [VNFaceObservation] else {
        print("NO_FACES")
        return
    }
    // Sort by area, take largest
    let sorted = observations.sorted { $0.boundingBox.size.area > $1.boundingBox.size.area }
    for obs in sorted {
        let b = obs.boundingBox
        // Vision: y=0 is BOTTOM, y=1 is TOP (normalized 0-1)
        print("FACE \(b.origin.x) \(b.origin.y) \(b.size.width) \(b.size.height)")
    }
}

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
do {
    try handler.perform([request])
} catch {
    print("ERROR: \(error)")
    exit(1)
}
