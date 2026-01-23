<p align="center">
  <img src="assets/scribd.svg" alt="Scribd" width="200">
</p>

<h1 align="center">Scribd Downloader</h1>

<p align="center">
  <b>Download Scribd documents as PDF for free - Fast, automated, and runs in background!</b>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.7+">
  </a>
  <a href="https://pypi.org/project/selenium/">
    <img src="https://img.shields.io/badge/Selenium-4.0+-green?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium 4.0+">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-orange?style=for-the-badge" alt="MIT License">
  </a>
</p>

<p align="center">
  <a href="https://buymeacoffee.com/mrsami">
    <img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me A Coffee">
  </a>
  <a href="https://github.com/sponsors/themrsami">
    <img src="https://img.shields.io/badge/Sponsor-ea4aaa?style=for-the-badge&logo=github-sponsors&logoColor=white" alt="GitHub Sponsors">
  </a>
  <a href="https://github.com/themrsami/scribd-downloader/stargazers">
    <img src="https://img.shields.io/github/stars/themrsami/scribd-downloader?style=for-the-badge&logo=github" alt="GitHub Stars">
  </a>
</p>

---

## Features

- **One-click download** - Just paste the Scribd URL and get your PDF
- **Runs in background** - Headless Chrome, no browser window pops up
- **Fast processing** - Optimized scrolling and minimal wait times
- **Clean PDFs** - No cookie banners, toolbars, or watermarks
- **Custom page size** - Executive size (7.25" x 10.5") with no margins
- **Auto filename** - PDF named after the document URL automatically
- **No login required** - Works without Scribd account

---

## Requirements

- Python 3.7 or higher
- Google Chrome browser installed
- Chrome WebDriver (auto-managed by Selenium)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/themrsami/scribd-downloader.git
   cd scribd-downloader
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. **Run the script**
   ```bash
   python scribd-downloader.py
   ```

2. **Paste the Scribd document URL** when prompted:
   ```
   Input link Scribd: https://www.scribd.com/document/123456789/Document-Title
   ```

3. **Wait for the download** - The script will:
   - Open the document in headless Chrome
   - Scroll through all pages to load content
   - Remove unwanted elements (toolbars, cookie banners)
   - Save as PDF in the current directory

4. **Done!** Your PDF will be saved with the document name from the URL.

---

## Example Output

```
$ python scribd-downloader.py
Input link Scribd: https://www.scribd.com/document/863374232/Ultimate-Web-Development-Bundle

Link embed: https://www.scribd.com/embeds/863374232/content
Output filename: Ultimate-Web-Development-Bundle.pdf

🚀 Starting headless Chrome browser...
✅ Cookie dialogs hidden
📄 Found 45 pages, scrolling...
   Scrolled 10/45 pages...
   Scrolled 20/45 pages...
   Scrolled 30/45 pages...
   Scrolled 40/45 pages...
✅ All 45 pages loaded
✅ Top toolbar removed
✅ Bottom toolbar removed
✅ Cleaned 1 scroll containers
✅ Print CSS injected

📥 Saving PDF as: Ultimate-Web-Development-Bundle.pdf
   Page size: Executive (7.25" x 10.5")
   Margins: None
   Headers/Footers: Disabled
✅ PDF saved successfully to: C:\Users\...\Ultimate-Web-Development-Bundle.pdf
🔒 Browser closed
```

---

## PDF Settings

| Setting | Value |
|---------|-------|
| Page Size | Executive (7.25" x 10.5") |
| Margins | None (0) |
| Headers/Footers | Disabled |
| Background Graphics | Enabled |

---

## How It Works

1. **URL Conversion** - Converts Scribd document URL to embeddable format
2. **Headless Browser** - Opens Chrome in background (invisible)
3. **Page Loading** - Scrolls through all pages to trigger lazy-loading
4. **Cleanup** - Removes toolbars, cookie banners, and overlays
5. **PDF Generation** - Uses Chrome DevTools Protocol to generate PDF directly
6. **Auto Close** - Browser closes automatically after saving

---

## Troubleshooting

### "ChromeDriver not found" error
The script uses Selenium Manager to auto-download ChromeDriver. If you face issues:
```bash
pip install --upgrade selenium
```

### PDF not saving
- Ensure you have write permissions in the current directory
- Check if the Scribd URL is valid and accessible

### Blank pages in PDF
- Some documents may have DRM protection
- Try increasing the scroll delay in the script if pages aren't loading

---

## Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Support the Project

If you find this tool useful, consider supporting its development:

<p align="center">
  <a href="https://buymeacoffee.com/mrsami">
    <img src="assets/buymeacoffee.svg" alt="Buy Me A Coffee" width="40" height="40">
  </a>
</p>

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Disclaimer

This tool is for educational purposes only. Please respect copyright laws and Scribd's Terms of Service. Only download documents you have the right to access.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/themrsami">Usama Nazir</a>
</p>

<p align="center">
  If you find this useful, please consider giving it a ⭐
</p>
