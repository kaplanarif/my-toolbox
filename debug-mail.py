#!/usr/bin/env python3
import subprocess

# Mail.app'teki son 5 maili listele
script = '''
tell application "Mail"
    set resultList to {}
    set targetMailbox to mailbox "Inbox" of account "Exchange"

    set msgCount to 0
    repeat with msg in messages of targetMailbox
        set msgCount to msgCount + 1
        if msgCount > 5 then exit repeat

        set msgSender to sender of msg
        set msgSubject to subject of msg
        set msgRead to read status of msg

        set end of resultList to "---"
        set end of resultList to "Sender: " & msgSender
        set end of resultList to "Subject: " & msgSubject
        set end of resultList to "Read: " & (msgRead as string)
    end repeat

    return resultList as string
end tell
'''

result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
print("📧 Son 5 mail:\n")
print(result.stdout)
if result.stderr:
    print("\n❌ Hata:", result.stderr)
