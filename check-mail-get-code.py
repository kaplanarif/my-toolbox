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
    Mail'den FortiClient kodunu çıkart
    
    Args:
        sender_filter: Gönderici email adresi (örn: "noreply@company.com")
        subject_filter: Konu anahtar kelimesi (örn: "verification")
        unread_only: Sadece okunmamış mailleri kontrol et
        minutes_back: Son kaç dakikadaki mailleri kontrol et
        mailbox_name: Kontrol edilecek mail klasörü
    """
    
    # AppleScript komutu
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
            # Kod çıkart (subject veya content'ten 6 haneli sayı)
            match = re.search(r'\b(\d{6})\b', result.stdout)
            if match:
                return match.group(1)
            else:
                # Alphanumeric kod ara
                match = re.search(r'\b([A-Z0-9]{6})\b', result.stdout)
                return match.group(1) if match else None
        else:
            print("❌ Mail okunamadı veya kod bulunamadı")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ Mail okuma zaman aşımına uğradı")
        return None
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None


def copy_code_to_clipboard(code):
    """
    Kodu clipboard'a kopyala
    """
    try:
        # macOS pbcopy komutu kullan
        subprocess.run(
            ['pbcopy'],
            input=code.encode('utf-8'),
            check=True
        )
        print(f"📋 Kod clipboard'a kopyalandı: {code}")
        print("👉 Şimdi FortiClient'e yapıştırabilirsin (Cmd+V)")
        return True

    except Exception as e:
        print(f"❌ Clipboard hatası: {e}")
        print(f"Manuel kod: {code}")
        return False


def check_new_mail():
    """
    Mail.app'te yeni mail kontrolü yap
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
        print(f"⚠️  Mail check hatası: {e}")
        return False


def main():
    print("🔄 Mail kontrol döngüsü başlatılıyor...")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            # Yeni mail kontrol et
            check_new_mail()
            print("🔍 Mail kontrol ediliyor...")

            # Kod ara
            code = get_forticlient_code(
                sender_filter="DoNotReply@fortinet-notifications.com",
                subject_filter="AuthCode",
                unread_only=True,
                minutes_back=10,
                mailbox_name="Inbox"
            )

            if code:
                print(f"✅ Kod bulundu: {code}")
                copy_code_to_clipboard(code)
                print("\n✨ İşlem tamamlandı! Script durduruluyor.")
                break
            else:
                print("⏳ Kod bulunamadı, 5 saniye sonra tekrar denenecek...\n")
                time.sleep(5)

    except KeyboardInterrupt:
        print("\n\n⛔ Script durduruldu.")


if __name__ == "__main__":
    main()
