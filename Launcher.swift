import Cocoa
import WebKit
import PDFKit

if CommandLine.arguments.count == 3 && CommandLine.arguments[1] == "--extract-pdf" {
    if let document = PDFDocument(url: URL(fileURLWithPath: CommandLine.arguments[2])) {
        for i in 0..<document.pageCount { print(document.page(at: i)?.string ?? "") }
        exit(0)
    }
    exit(1)
}

class AppDelegate: NSObject, NSApplicationDelegate, WKUIDelegate {
    var window: NSWindow!
    var process: Process!
    func applicationDidFinishLaunching(_ notification: Notification) {
        let menu = NSMenu()
        let appMenuItem = NSMenuItem()
        let appMenu = NSMenu()
        appMenu.addItem(withTitle:"Quit AI Builder", action:#selector(NSApplication.terminate(_:)), keyEquivalent:"q")
        appMenuItem.submenu = appMenu; menu.addItem(appMenuItem)
        let editItem=NSMenuItem(); let editMenu=NSMenu(title:"Edit")
        editMenu.addItem(withTitle:"Copy",action:#selector(NSText.copy(_:)),keyEquivalent:"c")
        editMenu.addItem(withTitle:"Paste",action:#selector(NSText.paste(_:)),keyEquivalent:"v")
        editMenu.addItem(withTitle:"Select All",action:#selector(NSText.selectAll(_:)),keyEquivalent:"a")
        editItem.submenu=editMenu;menu.addItem(editItem);NSApp.mainMenu=menu
        let root = Bundle.main.resourceURL!
        process = Process()
        process.executableURL = URL(fileURLWithPath: "/opt/homebrew/bin/python3")
        process.arguments = ["-B", "-m", "local_builder.desktop"]
        process.currentDirectoryURL = root
        var env = ProcessInfo.processInfo.environment
        env["PYTHONUNBUFFERED"] = "1"
        env["AI_BUILDER_EXECUTABLE"] = Bundle.main.executableURL!.path
        process.environment = env
        let pipe = Pipe(); process.standardOutput = pipe
        do { try process.run() } catch {
            let alert = NSAlert(); alert.messageText = "Could not start AI Builder"; alert.informativeText = error.localizedDescription; alert.runModal(); NSApp.terminate(nil); return
        }
        let data = pipe.fileHandleForReading.availableData
        guard let address = String(data: data, encoding: .utf8)?.trimmingCharacters(in: .whitespacesAndNewlines), let url = URL(string: address) else { NSApp.terminate(nil); return }
        let web = WKWebView(frame: .zero)
        web.uiDelegate = self
        window = NSWindow(contentRect: NSRect(x: 0,y: 0,width: 1150,height: 840), styleMask: [.titled,.closable,.miniaturizable,.resizable], backing: .buffered,defer: false)
        window.title = "AI Builder"
        window.contentView = web
        window.center(); window.makeKeyAndOrderFront(nil)
        web.load(URLRequest(url: url))
        NSApp.activate(ignoringOtherApps: true)
    }
    func webView(_ webView: WKWebView, runOpenPanelWith parameters: WKOpenPanelParameters, initiatedByFrame frame: WKFrameInfo, completionHandler: @escaping ([URL]?) -> Void) {
        let panel = NSOpenPanel(); panel.allowsMultipleSelection = false; panel.canChooseDirectories = false
        panel.begin { result in completionHandler(result == .OK ? panel.urls : nil) }
    }
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { true }
    func applicationWillTerminate(_ notification: Notification) { process?.terminate() }
}
let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.regular)
app.run()
