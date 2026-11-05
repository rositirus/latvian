# Learn Latvian

A free, minimal web app for learning Latvian, made for expats, students and anyone new to Latvia.

**Live:** https://latvian.rositirus.com/

- 120 modules in 13 groups, from the alphabet and greetings through *Settling in* (documents, registering your address, bank, healthcare) to everyday grammar
- 1,240 words and 312 example sentences, every one with audio
- **Practice**: random cards from all modules on a split-flap "flip board", with Latvian→English or English→Latvian and Flip or Type modes
- **Modules**: Learn (list + audio), Cards, Quiz, Build (arrange words into a sentence), Write (with a Latvian letter keyboard)
- Spaced repetition: correct answers come back after 1, 3, 7, 16 and 35 days. Progress is stored in the browser (localStorage).

No framework, no build step on Vercel: it's a static site.

## Project structure

```
content/curriculum.txt      ← all vocabulary and sentences (edit this)
scripts/template.html       ← the app (HTML/CSS/JS)
scripts/build.py            ← builds index.html from the two above
scripts/generate_audio.py   ← creates missing MP3s in audio/
index.html                  ← built app (committed, served by Vercel)
audio/*.mp3                 ← one clip per word/sentence, named by a hash of the text
vercel.json                 ← long-term caching for audio
```

## Editing content

The format of `content/curriculum.txt`:

```
## Group name
# Module name
latvian word = English meaning
> Latvian sentence. = English translation.
Ā ā = long "aa" — māja (house) {say: ā. māja}   ← optional custom audio text
```

After editing:

```bash
pip install -r requirements.txt
python scripts/generate_audio.py   # only creates clips for new/changed text
python scripts/build.py
```

Then commit and push. Vercel redeploys automatically. Audio for changed text gets a new file name; you can delete the old, unused clips (the audio script lists how many there are).

## Run locally

```bash
python3 -m http.server 8000
# open http://localhost:8000/
```

## Deploying on Vercel

Import the repo in Vercel with the **Other** framework preset, no build command, and the project root as the output directory. Add `latvian.rositirus.com` under *Settings → Domains*, then create the DNS record Vercel shows you (a `CNAME` for `latvian` pointing to `cname.vercel-dns.com`) at your domain provider.

## Audio

Audio is generated with Microsoft's Latvian neural voice *Everita* (`lv-LV-EveritaNeural`) through the [`edge-tts`](https://github.com/rany2/edge-tts) package. For a commercial or high-traffic setup, consider regenerating the clips through the official [Azure AI Speech](https://azure.microsoft.com/products/ai-services/text-to-speech) service, which offers the same voice.

## License

Code and content: [MIT](LICENSE) © Rosi Tirus
