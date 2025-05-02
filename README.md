# CineHack
A cinematic hacking terminal simulator written in Python. Designed for films, games, or demos needing a realistic red-team style command line sequence—complete with typing effects, system feedback, and believable exploit flow. Fully modular and customizable.

# 🎬 Cinematic Hack Terminal Simulator

A cinematic terminal sequence simulator written in Python—perfect for films, cutscenes, live demos, or any project that calls for a convincing but fictional hacking sequence. Unlike the cartoonish depictions you see in 99% of film and TV, this script follows a plausible, real-world attack pattern, simulating both attacker input and target system responses with authentic pacing and structure.

The idea came to me while watching a movie with my wife—yet another scene featuring a laughably unrealistic hack, all neon graphics and frantic keystrokes. I’ve seen this trope repeated in film after film, and finally decided to write something better. This script is my answer: a tool for anyone looking to portray a believable hack that actually passes the sniff test.

## ✨ Features
- 🎞️ Simulates red-team attack flow (recon, exploitation, escalation, cleanup)
- ⌨️ Realistic **typewriter effect** for attacker-typed commands
- ⚙️ System-style outputs with colour-coded response levels
- 🔁 Modular command script — easy to edit or extend
- ⚡ `--fast` mode for previewing entire scenes quickly
  

🚀 Usage
# Run in cinematic mode
python cinehack.py

# Skip delays (fast preview)
python cinehack.py --fast
🔧 Requires Python 3.7+
✨ For full Unicode and ANSI support on Windows, run from a modern terminal (Windows Terminal or WSL)

🛠️ Customizing the Script
Edit the build_session() function to rewrite the scene:

python
Copy
Edit
Cmd("nmap -T4 -p- vulnerablecorp.com", "[open ports: 22, 80, 443, 8080, 3306]"),
Cmd("python3 exploit.py", "[+] Exploit sent! Shell incoming...", "success"),

📜 License
MIT — Free for personal and commercial use. Attribution appreciated but not required.

🎥 Created For
Film scenes, hacking cutscenes, game intros, cybersecurity training intros, and hacker-style presentation effects.

🧠 Inspiration
Every movie hacking montage ever. But slightly more plausible.
