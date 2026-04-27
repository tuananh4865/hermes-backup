import SwiftUI

struct GraphView: View {
    let notes: [Note]
    @Binding var isPresented: Bool
    @State private var layoutEngine = GraphLayoutEngine()
    @State private var scale: CGFloat = 1.0
    @State private var offset: CGSize = .zero
    @State private var selectedNodeId: UUID?
    @State private var isFullscreen = false
    @State private var timer: Timer?

    var body: some View {
        ZStack {
            Color(hex: "0A0A0F")
                .ignoresSafeArea()

            // Top bar
            VStack {
                HStack {
                    Button("Done") {
                        isPresented = false
                    }
                    .foregroundColor(Color(hex: "6366F1"))

                    Spacer()

                    Text("Graph")
                        .font(.headline)
                        .foregroundColor(.white)

                    Spacer()

                    Button {
                        withAnimation {
                            isFullscreen.toggle()
                        }
                    } label: {
                        Image(systemName: isFullscreen ? "arrow.down.right.and.arrow.up.left" : "arrow.up.left.and.arrow.down.right")
                            .foregroundColor(Color(hex: "8E8E9A"))
                    }
                }
                .padding(.horizontal, 16)
                .padding(.vertical, 12)

                Spacer()
            }

            // Graph Canvas
            GeometryReader { geometry in
                let canvasSize = geometry.size

                ZStack {
                    // Edges
                    ForEach(layoutEngine.edges) { edge in
                        if let source = layoutEngine.nodes.first(where: { $0.id == edge.sourceId }),
                           let target = layoutEngine.nodes.first(where: { $0.id == edge.targetId }) {
                            Path { path in
                                path.move(to: source.position)
                                path.addLine(to: target.position)
                            }
                            .stroke(Color(hex: "6366F1").opacity(0.4), lineWidth: 0.5)
                        }
                    }

                    // Nodes
                    ForEach(layoutEngine.nodes) { node in
                        GraphNodeView(
                            node: node,
                            isSelected: selectedNodeId == node.id
                        )
                        .position(node.position)
                        .onTapGesture {
                            withAnimation(.easeInOut(duration: 0.2)) {
                                selectedNodeId = selectedNodeId == node.id ? nil : node.id
                            }
                        }
                        .gesture(
                            DragGesture()
                                .onChanged { value in
                                    if let index = layoutEngine.nodes.firstIndex(where: { $0.id == node.id }) {
                                        layoutEngine.nodes[index].position = value.location
                                    }
                                }
                        )
                    }
                }
                .scaleEffect(scale)
                .offset(offset)
                .gesture(
                    MagnificationGesture()
                        .onChanged { value in
                            scale = min(max(0.5, value), 3.0)
                        }
                )
                .simultaneousGesture(
                    DragGesture()
                        .onChanged { value in
                            offset = CGSize(
                                width: offset.width + value.translation.width,
                                height: offset.height + value.translation.height
                            )
                        }
                )
                .onAppear {
                    layoutEngine.buildGraph(from: notes)
                    startSimulation(canvasSize: canvasSize)
                }
                .onDisappear {
                    timer?.invalidate()
                }
            }

            // Minimap
            if !isFullscreen {
                VStack {
                    Spacer()
                    HStack {
                        minimap
                        Spacer()
                    }
                    .padding(16)
                    .padding(.bottom, 40)
                }
            }

            // Selected node info
            if let selectedId = selectedNodeId,
               let node = layoutEngine.nodes.first(where: { $0.id == selectedId }) {
                VStack {
                    Spacer()
                    nodeInfoCard(for: node)
                        .padding(.horizontal, 16)
                        .padding(.bottom, 120)
                }
            }
        }
        .preferredColorScheme(.dark)
    }

    private var minimap: some View {
        RoundedRectangle(cornerRadius: 8)
            .fill(Color(hex: "1A1A24"))
            .frame(width: 80, height: 60)
            .overlay {
                GeometryReader { geometry in
                    let scaleX: CGFloat = 80 / 500
                    let scaleY: CGFloat = 60 / 500

                    ForEach(layoutEngine.nodes) { node in
                        Circle()
                            .fill(Color(hex: "6366F1"))
                            .frame(width: 4, height: 4)
                            .position(
                                x: node.position.x * scaleX,
                                y: node.position.y * scaleY
                            )
                    }
                }
            }
            .opacity(isFullscreen ? 0 : 0.8)
    }

    private func nodeInfoCard(for node: GraphNode) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(node.title)
                .font(.headline)
                .foregroundColor(.white)
            Text("\(node.connections) connection\(node.connections == 1 ? "" : "s")")
                .font(.caption)
                .foregroundColor(Color(hex: "8E8E9A"))
        }
        .padding(16)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(Color(hex: "1A1A24"))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private func startSimulation(canvasSize: CGSize) {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0 / 60.0, repeats: true) { _ in
            layoutEngine.tick(canvasSize: canvasSize)
            if layoutEngine.isStable() {
                timer?.invalidate()
            }
        }
    }
}

struct GraphNodeView: View {
    let node: GraphNode
    let isSelected: Bool

    var body: some View {
        VStack(spacing: 4) {
            Circle()
                .fill(
                    RadialGradient(
                        colors: [
                            Color(hex: "6366F1"),
                            Color(hex: "818CF8")
                        ],
                        center: .center,
                        startRadius: 0,
                        endRadius: node.nodeRadius
                    )
                )
                .frame(width: node.nodeRadius * 2, height: node.nodeRadius * 2)
                .overlay {
                    if isSelected {
                        Circle()
                            .stroke(Color.white, lineWidth: 2)
                    }
                }
                .shadow(color: Color(hex: "6366F1").opacity(0.5), radius: isSelected ? 12 : 6)

            Text(node.title)
                .font(.system(size: 10))
                .foregroundColor(.white)
                .lineLimit(1)
                .frame(maxWidth: 60)
        }
    }
}
