#Requires AutoHotkey v2.0

#SingleInstance Force
SetWorkingDir A_ScriptDir
Persistent

holdMs := 500
serverPid := 0
ctrlDownAt := 0
monitoringCtrl := false

OnExit(exitFunc)

exitFunc(*) {
    if (serverPid) {
        try ProcessWaitClose(serverPid, 1)
        try ProcessClose(serverPid)
    }
}

; Win+T 测试：直接触发划词功能
#t::
{
    TrayTip "划词助手", "Win+T 测试触发", 2000
    Sleep 300
    ensureServerRunning()
    text := getSelectedText()
    if (text == "") {
        TrayTip "划词助手", "未检测到选中文本", 2000
        return
    }
    TrayTip "划词助手", "获取到:" SubStr(text, 1, 30), 2000
    showPopup(text)
}

; 长按 Ctrl 检测
~Ctrl::
{
    global ctrlDownAt, monitoringCtrl
    ctrlDownAt := A_TickCount
    if (!monitoringCtrl) {
        monitoringCtrl := true
        SetTimer(ctrlCheck, 50)
    }
}

ctrlCheck()
{
    global ctrlDownAt, monitoringCtrl, holdMs
    if (!GetKeyState("Ctrl", "P")) {
        elapsed := A_TickCount - ctrlDownAt
        monitoringCtrl := false
        SetTimer(ctrlCheck, 0)
        if (elapsed >= holdMs) {
            TrayTip "划词助手", "长按触发！时长:" elapsed "ms", 2000
            Sleep 300
            ensureServerRunning()
            text := getSelectedText()
            if (text == "") {
                TrayTip "划词助手", "未检测到选中文本", 2000
                return
            }
            TrayTip "划词助手", "获取到:" SubStr(text, 1, 30), 2000
            showPopup(text)
        }
    }
}

getSelectedText()
{
    prevClip := ClipboardAll()
    A_Clipboard := ""
    Send "{Ctrl down}c{Ctrl up}"
    if !ClipWait(0.5)
    {
        A_Clipboard := prevClip
        return ""
    }
    text := Trim(A_Clipboard)
    A_Clipboard := prevClip
    return text
}

ensureServerRunning()
{
    try
    {
        whr := ComObject("WinHttp.WinHttpRequest.5.1")
        whr.Open("GET", "http://127.0.0.1:5000/health", true)
        whr.Send()
        whr.WaitForResponse()
        if (whr.Status == 200)
            return
    }
    scriptPath := A_ScriptDir . "\server.py"
    Run("pythonw.exe `"" . scriptPath . "`"", , "Hide", &serverPid)
    Sleep(1500)
}

showPopup(text)
{
    global popupText
    popupText := text

    encoded := UriEncode(text)
    url := "http://127.0.0.1:5000/popup?text=" . encoded

    ; 查找 Chrome
    chromePaths := [
        A_AppData . "\..\Local\Google\Chrome\Application\chrome.exe",
        "C:\Program Files\Google\Chrome\Application\chrome.exe",
        "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]

    browser := ""
    for p in chromePaths {
        if FileExist(p) {
            browser := p
            break
        }
    }

    if (browser != "") {
        MonitorGet(1, &MonLeft, &MonTop, &MonRight, &MonBottom)
        x := (MonRight - MonLeft - 490) // 2 + MonLeft
        y := (MonBottom - MonTop - 420) // 2 + MonTop
        Run("`"" . browser . "`" --user-data-dir=`"" . A_Temp . "\text-helper-chrome`" --app=`"" . url . "`" --window-size=490,420 --window-position=" . x . "," . y, , , &pid)
        Sleep 1200
        WinMove(x, y, 490, 420, "划词助手")
    } else {
        Run(url)
    }
}

UriEncode(str)
{
    result := ""
    buf := Buffer(StrPut(str, "UTF-8"))
    StrPut(str, buf, "UTF-8")
    Loop buf.Size - 1
    {
        b := NumGet(buf, A_Index - 1, "UChar")
        if ((b >= 0x41 && b <= 0x5A) || (b >= 0x61 && b <= 0x7A) || (b >= 0x30 && b <= 0x39) || b == 0x2D || b == 0x5F || b == 0x2E || b == 0x7E)
            result .= Chr(b)
        else
            result .= Format("%{:02X}", b)
    }
    return result
}
