import SwiftUI

struct GraphNode: Identifiable {
    let id: UUID
    var title: String
    var position: CGPoint
    var connections: Int
    var nodeRadius: CGFloat = 12

    init(id: UUID = UUID(), title: String, position: CGPoint, connections: Int = 0) {
        self.id = id
        self.title = title
        self.position = position
        self.connections = connections
    }
}

struct GraphEdge: Identifiable {
    let id = UUID()
    let sourceId: UUID
    let targetId: UUID
}

class GraphLayoutEngine: ObservableObject {
    @Published var nodes: [GraphNode] = []
    @Published var edges: [GraphEdge] = []

    private var velocities: [UUID: CGPoint] = [:]

    func buildGraph(from notes: [Note]) {
        nodes = notes.enumerated().map { index, note in
            let angle = Double(index) / Double(max(1, notes.count)) * 2 * .pi
            let radius: CGFloat = 150
            let centerX = UIScreen.main.bounds.width / 2
            let centerY = UIScreen.main.bounds.height / 2
            let x = centerX + radius * CGFloat(cos(angle))
            let y = centerY + radius * CGFloat(sin(angle))
            let links = extractLinks(from: note.content)
            return GraphNode(
                id: note.id,
                title: note.title.isEmpty ? "Untitled" : note.title,
                position: CGPoint(x: x, y: y),
                connections: links.count
            )
        }

        edges = []
        for note in notes {
            let linkedTitles = extractLinks(from: note.content)
            for linkedTitle in linkedTitles {
                if let linkedNote = notes.first(where: { $0.title.lowercased() == linkedTitle.lowercased() }) {
                    edges.append(GraphEdge(sourceId: note.id, targetId: linkedNote.id))
                }
            }
        }
    }

    private func extractLinks(from content: String) -> [String] {
        let pattern = "\\[\\[([^\\]]+)\\]\\]"
        guard let regex = try? NSRegularExpression(pattern: pattern, options: []) else { return [] }
        let range = NSRange(content.startIndex..., in: content)
        let matches = regex.matches(in: content, options: [], range: range)
        return matches.compactMap { match -> String? in
            guard let range = Range(match.range(at: 1), in: content) else { return nil }
            return String(content[range])
        }
    }

    func tick(canvasSize: CGSize) {
        let center = CGPoint(x: canvasSize.width / 2, y: canvasSize.height / 2)
        let repulsion: CGFloat = 5000
        let attraction: CGFloat = 0.05
        let damping: CGFloat = 0.9
        let idealEdgeLength: CGFloat = 100

        // Initialize velocities if needed
        for node in nodes {
            if velocities[node.id] == nil {
                velocities[node.id] = .zero
            }
        }

        var forces: [UUID: CGPoint] = [:]

        // Repulsion between all nodes
        for i in 0..<nodes.count {
            for j in (i+1)..<nodes.count {
                let delta = CGPoint(
                    x: nodes[i].position.x - nodes[j].position.x,
                    y: nodes[i].position.y - nodes[j].position.y
                )
                let distance = max(sqrt(delta.x * delta.x + delta.y * delta.y), 1)
                let force = repulsion / (distance * distance)
                let normalized = CGPoint(x: delta.x / distance, y: delta.y / distance)
                forces[nodes[i].id, default: .zero] = CGPoint(
                    x: forces[nodes[i].id, default: .zero].x + normalized.x * force,
                    y: forces[nodes[i].id, default: .zero].y + normalized.y * force
                )
                forces[nodes[j].id, default: .zero] = CGPoint(
                    x: forces[nodes[j].id, default: .zero].x - normalized.x * force,
                    y: forces[nodes[j].id, default: .zero].y - normalized.y * force
                )
            }
        }

        // Attraction along edges
        for edge in edges {
            guard let sourceIndex = nodes.firstIndex(where: { $0.id == edge.sourceId }),
                  let targetIndex = nodes.firstIndex(where: { $0.id == edge.targetId }) else { continue }

            let delta = CGPoint(
                x: nodes[targetIndex].position.x - nodes[sourceIndex].position.x,
                y: nodes[targetIndex].position.y - nodes[sourceIndex].position.y
            )
            let distance = sqrt(delta.x * delta.x + delta.y * delta.y)
            let force = attraction * (distance - idealEdgeLength)
            let normalized = CGPoint(x: delta.x / max(distance, 1), y: delta.y / max(distance, 1))
            forces[nodes[sourceIndex].id, default: .zero] = CGPoint(
                x: forces[nodes[sourceIndex].id, default: .zero].x + normalized.x * force,
                y: forces[nodes[sourceIndex].id, default: .zero].y + normalized.y * force
            )
            forces[nodes[targetIndex].id, default: .zero] = CGPoint(
                x: forces[nodes[targetIndex].id, default: .zero].x - normalized.x * force,
                y: forces[nodes[targetIndex].id, default: .zero].y - normalized.y * force
            )
        }

        // Apply forces
        for i in 0..<nodes.count {
            let nodeId = nodes[i].id
            let currentVel = velocities[nodeId] ?? .zero
            let force = forces[nodeId] ?? .zero
            let velocity = CGPoint(
                x: currentVel.x * damping + force.x,
                y: currentVel.y * damping + force.y
            )
            velocities[nodeId] = velocity
            nodes[i].position = CGPoint(
                x: nodes[i].position.x + velocity.x,
                y: nodes[i].position.y + velocity.y
            )
        }
    }

    func isStable() -> Bool {
        var totalVelocity: CGFloat = 0
        for velocity in velocities.values {
            totalVelocity += sqrt(velocity.x * velocity.x + velocity.y * velocity.y)
        }
        return totalVelocity < 0.5
    }
}
