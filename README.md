
# FileToLink Bot

**FileToLink Bot** is a Telegram bot and web player system that lets users upload images or videos and instantly get:
- A direct CDN download link
- An online web player link
- Quick links to open the file in popular external video players (MX Player, Playit)

The project also includes a modern, responsive web player (Next.js, deployable to Vercel) for seamless online streaming.

---

## 🚀 Features

- **Upload**: Send images or videos to the bot and get instant CDN hosting.
- **Direct Download**: Receive a direct, globally distributed CDN link for your file.
- **Online Streaming**: Get a one-click web player link for instant streaming (works on all devices).
- **External Player Links**: Open your video in MX Player or Playit on Android with a single tap.
- **User-Friendly**: Greetings, help command, navigation keyboard, and error handling.
- **Open Source**: Easily customizable and extensible.

---

## 🏗️ Architecture

```
/ (root)
│
├── bot/                  # Python Telegram bot code
│   └── pybot.py
│   └── requirements.txt
│
├── web/                  # Next.js frontend (web player)
│   ├── app/
│   │   └── player/page.tsx
│   ├── components/
│   │   └── VideoPlayer.js (optional, for advanced player)
│   ├── public/
│   └── package.json
│
├── .env                  # Bot and CDN credentials
├── README.md
```

- **Telegram Bot**: Handles uploads, calls CDN API, and returns all links.
- **Web Player**: Next.js app, streams video from CDN, responsive on all devices.

---

## ⚡ Quickstart

### 1. **Clone the Repo**

```
git clone https://github.com/yourusername/FileToLink-Bot.git
cd FileToLink-Bot
```

### 2. **Bot Setup**

```
cd bot
pip install -r requirements.txt
```

Create a `.env` file in the `bot/` directory:

```
BOT_TOKEN=your_telegram_bot_token
CDN_ACCESS_TOKEN=your_cdn_access_token
```

Run the bot:

```
python pybot.py
```

### 3. **Web Player Setup**

```
cd ../web
npm install
npm run dev
```

Access the player at:  
`http://localhost:3000/player?url=`

---

## 🌐 Deploying the Web Player to Vercel

1. Push your repo to GitHub (or GitLab/Bitbucket).
2. Go to [vercel.com](https://vercel.com), sign in, and import your repo.
3. Set the project root to `/web` during setup.
4. Deploy. Vercel will give you a live URL like:  
   `https://your-vercel-app.vercel.app/player?url=`
5. Update `WEB_PLAYER_BASE` in your bot code to use your deployed Vercel URL.

---

## 🤖 Usage

1. **Start the bot** on Telegram.
2. **Send an image or video**.
3. **Receive:**
   - Direct CDN download link
   - Online streaming link (web player)
   - MX Player and Playit links (as clickable buttons)
4. **Click any link or button** to open or stream your file.

---

## 🛠️ Advanced Customization

- **Web Player**: Enhance with [Video.js](https://videojs.com/) or [Plyr](https://plyr.io/).
- **Bot**: Add support for more file types, analytics, or user authentication.
- **CDN**: Integrate with other CDN providers by updating the upload logic in `pybot.py`.

---

## 🐞 Troubleshooting

| Problem                  | Solution                                                            |
|--------------------------|---------------------------------------------------------------------|
| Links not clickable      | Use latest code with MarkdownV2 and InlineKeyboard buttons          |
| Newlines not working     | Only use `\n` for newlines in Python strings, not `\\n`             |
| Bot token issues         | Check `.env` file and load order in `pybot.py`                      |
| CDN upload fails         | Check your `CDN_ACCESS_TOKEN` and API endpoint                      |
| Web player not streaming | Make sure your CDN link is public and uses HTTPS                    |

---

## 🙏 Credits

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [Next.js](https://nextjs.org/)
- [Video.js](https://videojs.com/) (optional)
- [Your CDN Provider](https://snapzion.com/)
- [Vercel](https://vercel.com/)

---

## 📄 License

MIT License.  
Feel free to use, modify, and share!

---

## 💬 Support

For questions, suggestions, or bug reports, open an issue or contact [@YourSupportHandle](https://t.me/YourSupportHandle).

**Happy sharing! 🚀**
```
This markdown is fully compatible with GitHub and other markdown renderers[1].  
Let me know if you want a sample screenshot section or further customization!

[1] programming.documentation