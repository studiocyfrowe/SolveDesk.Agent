import { app, BrowserWindow } from "electron"
import path from "path"

let mainWindow: BrowserWindow | null = null

const createWindow = () => {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, "preload.ts"),
            contextIsolation: true,
            nodeIntegration: false,
        }
    })

    if (process.env.NODE_ENV === "development") {
        mainWindow.loadURL("http://localhost:3000")
    } else {
        mainWindow.loadFile(path.join(__dirname, "../public/index.html"))
    }
}

app.whenReady().then(createWindow)

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit()
    }
})