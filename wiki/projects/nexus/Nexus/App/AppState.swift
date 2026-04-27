import SwiftUI

@Observable
final class AppState {
    var selectedNote: Note?
    var isShowingEditor: Bool = false
    var isShowingGraph: Bool = false
    var isShowingSearch: Bool = false
    var isShowingSettings: Bool = false
    var isShowingFolders: Bool = false
    var isShowingSubscription: Bool = false
    var isSubscribed: Bool = false
    var freeNoteCount: Int = 0
    let maxFreeNotes: Int = 50

    var canCreateNote: Bool {
        isSubscribed || freeNoteCount < maxFreeNotes
    }
}
