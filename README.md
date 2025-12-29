# My Toolbox

A collection of automation scripts and utilities.

## Scripts

### check-mail-get-code.py

Automates the process of retrieving FortiClient authentication codes from macOS Mail.app.

**Features:**
- Automatically checks for new emails in Mail.app
- Extracts 6-digit verification codes from FortiClient emails
- Copies the code to clipboard automatically
- Marks emails as read after processing

**Requirements:**
- macOS (uses AppleScript and Mail.app)
- Python 3
- Mail.app configured with Exchange account

**Usage:**
```bash
python3 check-mail-get-code.py
```

The script will:
1. Check Mail.app every 5 seconds for new FortiClient authentication emails
2. Extract the verification code
3. Copy it to your clipboard
4. Stop automatically once code is found

Press `Ctrl+C` to stop the script manually.

**Configuration:**

You can modify the script parameters in the `main()` function:
- `sender_filter`: Email sender to look for (default: "DoNotReply@fortinet-notifications.com")
- `subject_filter`: Subject keyword to match (default: "AuthCode")
- `unread_only`: Only check unread emails (default: True)
- `minutes_back`: How far back to check emails (default: 10 minutes)
- `mailbox_name`: Which mailbox to check (default: "Inbox")

### Other Scripts

- `debug-mail.py`: Debug utility for Mail.app operations
- `list-mailboxes.py`: Lists available mailboxes in Mail.app

## License

MIT
