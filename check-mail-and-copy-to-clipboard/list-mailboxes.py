#!/usr/bin/env python3
import subprocess

# Tüm mailbox'ları listele
script = '''
tell application "Mail"
    set mailboxList to {}
    repeat with acc in accounts
        set accName to name of acc
        set end of mailboxList to "Account: " & accName

        repeat with mbox in mailboxes of acc
            set mboxName to name of mbox
            set end of mailboxList to "  - " & mboxName
        end repeat
    end repeat

    return mailboxList as string
end tell
'''

result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
print("📬 Mevcut mailbox'lar:\n")
print(result.stdout)
if result.stderr:
    print("\n❌ Hata:", result.stderr)
