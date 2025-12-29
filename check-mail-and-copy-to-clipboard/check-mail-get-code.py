#!/usr/bin/env python3
import subprocess
import re
import time
from datetime import datetime, timedelta

def get_forticlient_code(
    sender_filter=None,
    subject_filter=None,
    unread_only=True,
    minutes_back=10,
    mailbox_name="Inbox"
):
    """
    Extract FortiClient code from Mail

    Args:
        sender_filter: Sender email address (e.g., "noreply@company.com")
        subject_filter: Subject keyword (e.g., "verification")
        unread_only: Check only unread emails
        minutes_back: How many minutes back to check emails
        mailbox_name: Mailbox folder to check
    """
    
    # AppleScript command
    script = f'''
    tell application "Mail"
        set resultList to {{}}
        set targetMailbox to mailbox "{mailbox_name}" of account "Exchange"

        repeat with msg in messages of targetMailbox
    '''
    
    if unread_only:
        script += 'if (read status of msg) is false then\n'
    
    script += f'''
            set msgDate to date received of msg
            set msgSender to sender of msg
            set msgSubject to subject of msg
            set msgContent to content of msg

            set shouldProcess to true
    '''
    
    if sender_filter:
        script += f'''
            if msgSender does not contain "{sender_filter}" then
                set shouldProcess to false
            end if
        '''
    
    if subject_filter:
        script += f'''
            if msgSubject does not contain "{subject_filter}" then
                set shouldProcess to false
            end if
        '''
    
    script += '''
            if shouldProcess then
                set read status of msg to true
                return msgSubject & "|SEPARATOR|" & msgContent
            end if
        end if
        end repeat
    end tell
    '''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout:
            # Extract code (6-digit number from subject or content)
            match = re.search(r'\b(\d{6})\b', result.stdout)
            if match:
                return match.group(1)
            else:
                # Search for alphanumeric code
                match = re.search(r'\b([A-Z0-9]{6})\b', result.stdout)
                return match.group(1) if match else None
        else:
            print("❌ Could not read mail or code not found")
            return None

    except subprocess.TimeoutExpired:
        print("❌ Mail reading timed out")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def copy_code_to_clipboard(code):
    """
    Copy code to clipboard
    """
    try:
        # Use macOS pbcopy command
        subprocess.run(
            ['pbcopy'],
            input=code.encode('utf-8'),
            check=True
        )
        print(f"📋 Code copied to clipboard: {code}")
        print("👉 You can now paste into FortiClient (Cmd+V)")
        return True

    except Exception as e:
        print(f"❌ Clipboard error: {e}")
        print(f"Manual code: {code}")
        return False


def check_new_mail():
    """
    Check for new mail in Mail.app
    """
    try:
        script = '''
        tell application "Mail"
            check for new mail
        end tell
        '''
        subprocess.run(['osascript', '-e', script], capture_output=True)
        return True
    except Exception as e:
        print(f"⚠️  Mail check error: {e}")
        return False


def main():
    print("🔄 Starting mail check loop...")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            # Check for new mail
            check_new_mail()
            print("🔍 Checking mail...")

            # Search for code
            code = get_forticlient_code(
                sender_filter="DoNotReply@fortinet-notifications.com",
                subject_filter="AuthCode",
                unread_only=True,
                minutes_back=10,
                mailbox_name="Inbox"
            )

            if code:
                print(f"✅ Code found: {code}")
                copy_code_to_clipboard(code)
                print("\n✨ Process completed! Stopping script.")
                break
            else:
                print("⏳ Code not found, retrying in 5 seconds...\n")
                time.sleep(5)

    except KeyboardInterrupt:
        print("\n\n⛔ Script stopped.")


if __name__ == "__main__":
    main()
