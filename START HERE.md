# Test AI Builder

1. Open LM Studio and start its local server on port 1234. Load a coding model.
2. Double-click **AI Builder** on your Desktop, or **AI Builder.app** inside this folder.
3. Drag **Try C Library.md** into the app for a C library and demo program, **Try C.md** for a C example, or **Try First.md** for Python.
4. Enter a project name, choose its output parent folder, select your model, and click **Start build**.
5. Wait for the checks to finish. Use **Test project** to verify again, **Run project** to see output, or **Run in Terminal** for keyboard input. **Open in VS Code** opens all the source files as a project.
6. Describe a small adjustment under **Make a change** and click **Apply change**.

Finished and in-progress project folders are currently stored at:

`~/Documents/AI Builder Projects` (inside your home folder)

The **Finished Projects** shortcut in this folder opens that default location. If you choose a different destination, the exact path appears in the app. Use **Open folder** to find it or **Recent projects** to reopen it.

To test on a Linux laptop, use **Export source ZIP**, transfer and extract the ZIP, then open a terminal in the extracted project and run `python3 project.py test` followed by `python3 project.py run`. Install a C compiler and Python 3 on the laptop first. The helper rebuilds C source for that machine. A Mac executable cannot simply be renamed to .exe or run on Linux.

You can instead put the generated source in its own GitHub repository and clone that onto the laptop. Both transfer methods work; GitHub is not required. The AI Builder app itself runs on this Mac.

Use the example plans to build a small program. The Word project-plan document describes how to develop the builder itself; it is not the recommended first test input.

This Desktop folder is the working copy for testing and future improvements. The earlier copy in the original project workspace has been retained as a snapshot. The Desktop launch icon points to the app inside this folder, so keep them together.

Read **POLISH ROADMAP.md** for the prioritized work list and **README.md** for current support and limitations. Record observations in **TEST NOTES.md**.
