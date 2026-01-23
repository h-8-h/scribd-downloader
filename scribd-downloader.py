"""
Scribd Document Downloader
==========================
A Python script that downloads documents from Scribd as PDF files.

How it works:
1. Converts the Scribd document URL to an embeddable format
2. Opens the document in a headless Chrome browser
3. Scrolls through all pages to trigger lazy-loading of content
4. Removes unwanted UI elements (toolbars, cookie banners, overlays)
5. Generates a clean PDF using Chrome DevTools Protocol
6. Saves the PDF with the document name from the URL

Author: Usama Nazir (@themrsami)
Repository: https://github.com/themrsami/scribd-downloader
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import base64
import os
import re
from urllib.parse import urlparse, unquote


# =============================================================================
# CONFIGURATION - Chrome Browser Options
# =============================================================================
options = Options()

# Run Chrome in headless mode (no visible browser window)
# This makes the script run silently in the background
options.add_argument("--headless=new")

# Disable automation detection flags
# These options prevent websites from detecting that the browser is automated
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def convert_scribd_link(url):
    """
    Convert a standard Scribd document URL to an embeddable content URL.

    The embed URL provides direct access to the document content without
    the Scribd website UI, making it easier to extract the document.

    Args:
        url: Standard Scribd URL (e.g., https://www.scribd.com/document/123456/Title)

    Returns:
        Embed URL (e.g., https://www.scribd.com/embeds/123456/content)
        or "Invalid Scribd URL" if the URL format is not recognized
    """
    match = re.search(r'https://www\.scribd\.com/document/(\d+)/', url)
    if match:
        doc_id = match.group(1)
        return f'https://www.scribd.com/embeds/{doc_id}/content'
    else:
        return "Invalid Scribd URL"


def get_filename_from_url(url):
    """
    Extract a clean filename from the Scribd document URL.

    Uses the last path segment of the URL as the filename, which typically
    contains the document title in a URL-friendly format.

    Args:
        url: Scribd document URL

    Returns:
        Filename with .pdf extension (e.g., "Document-Title.pdf")
    """
    parsed = urlparse(url)
    path = parsed.path.rstrip('/')
    last_segment = path.split('/')[-1] if path else 'scribd_document'
    # Decode URL-encoded characters (e.g., %20 -> space)
    last_segment = unquote(last_segment)
    return f"{last_segment}.pdf"


def save_pdf_directly(driver, filename="scribd_document.pdf"):
    """
    Generate and save a PDF using Chrome DevTools Protocol (CDP).

    This method bypasses the print dialog entirely and gives us full control
    over the PDF output settings including page size, margins, and headers.

    Args:
        driver: Selenium WebDriver instance
        filename: Output filename for the PDF

    Returns:
        Absolute path to the saved PDF file, or None if saving failed
    """
    # PDF generation settings
    # Using Executive page size (7.25" x 10.5") which works well for documents
    pdf_options = {
        'landscape': False,              # Portrait orientation
        'displayHeaderFooter': False,    # No page headers/footers
        'printBackground': True,         # Include background colors/images
        'scale': 1,                       # 100% scale (no zoom)
        'paperWidth': 7.25,              # Executive width in inches
        'paperHeight': 10.5,             # Executive height in inches
        'marginTop': 0,                  # No margins for full-page content
        'marginBottom': 0,
        'marginLeft': 0,
        'marginRight': 0,
        'preferCSSPageSize': False,      # Use our specified size, not CSS
    }

    try:
        # Execute Chrome DevTools Protocol command to generate PDF
        result = driver.execute_cdp_cmd('Page.printToPDF', pdf_options)

        # Decode the base64-encoded PDF data
        pdf_data = base64.b64decode(result['data'])

        # Write PDF to file
        with open(filename, 'wb') as f:
            f.write(pdf_data)

        return os.path.abspath(filename)
    except Exception as e:
        print(f"❌ Error saving PDF: {e}")
        return None


# =============================================================================
# MAIN SCRIPT EXECUTION
# =============================================================================

# Get Scribd document URL from user
input_url = input("Input link Scribd: ")

# Convert to embed URL and generate output filename
converted_url = convert_scribd_link(input_url)
pdf_filename = get_filename_from_url(input_url)

print(f"Link embed: {converted_url}")
print(f"Output filename: {pdf_filename}")

# Validate URL before proceeding
if converted_url == "Invalid Scribd URL":
    print("❌ Error: Please provide a valid Scribd document URL")
    print("   Example: https://www.scribd.com/document/123456789/Document-Title")
    exit(1)


# =============================================================================
# STEP 1: Initialize Browser and Load Document
# =============================================================================
print("\n🚀 Starting headless Chrome browser...")
driver = webdriver.Chrome(options=options)

# Navigate to the embed URL
driver.get(converted_url)

# Brief wait for initial page load
time.sleep(1)


# =============================================================================
# STEP 2: Remove Cookie Consent Dialogs and Banners
# =============================================================================
# Cookie dialogs can appear in the PDF if not removed. This step:
# 1. Clicks any close/dismiss buttons on cookie popups
# 2. Removes cookie-related elements from the DOM
# 3. Removes fixed-position banners containing privacy-related text

driver.execute_script("""
    // Attempt to click close/dismiss buttons on cookie dialogs
    var closeButtonSelectors = [
        '[class*="cookie"] [class*="close"]',
        '[class*="cookie"] [class*="dismiss"]',
        '[class*="cookie"] button[aria-label*="close"]',
        '[class*="cookie"] button[aria-label*="Close"]',
        '[class*="cookie"] .close',
        '[class*="cookie"] .dismiss',
        '[class*="consent"] [class*="close"]',
        '[class*="consent"] [class*="dismiss"]',
        '[class*="banner"] [class*="close"]',
        '[class*="banner"] [class*="dismiss"]',
        '[class*="notice"] [class*="close"]',
        '[class*="notice"] [class*="dismiss"]',
        'button[class*="close"]',
        'button[aria-label="Close"]',
        'button[aria-label="close"]',
        'button[aria-label="Dismiss"]',
        '[class*="cookie"] svg',
        '[class*="banner"] svg',
        '.close-button',
        '.dismiss-button',
        '[data-dismiss]',
        '[class*="cookie"] [class*="icon"]',
        'button:has(svg)',
        '[role="button"][class*="close"]'
    ];

    // Click all matching close buttons
    closeButtonSelectors.forEach(function(selector) {
        try {
            document.querySelectorAll(selector).forEach(function(btn) {
                btn.click();
            });
        } catch(e) {}
    });

    // After a brief delay, remove any remaining cookie-related elements
    setTimeout(function() {
        var cookieSelectors = [
            '[class*="cookie"]',
            '[class*="Cookie"]',
            '[class*="consent"]',
            '[class*="Consent"]',
            '[class*="gdpr"]',
            '[class*="GDPR"]',
            '[id*="cookie"]',
            '[id*="Cookie"]',
            '[id*="consent"]',
            '[id*="gdpr"]',
            '[class*="privacy-notice"]',
            '[class*="Privacy"]',
            '[class*="cookie-banner"]',
            '[class*="cookie-notice"]',
            '[class*="cookie-popup"]',
            '[class*="cookie-modal"]',
            '[class*="CookieConsent"]',
            '[class*="notice-banner"]',
            '.cc-window',
            '.cc-banner',
            '#onetrust-consent-sdk',
            '#onetrust-banner-sdk',
            '.evidon-banner',
            '.truste_box_overlay'
        ];

        cookieSelectors.forEach(function(selector) {
            try {
                document.querySelectorAll(selector).forEach(function(el) {
                    el.remove();
                });
            } catch(e) {}
        });
    }, 100);
""")

# Wait for cookie dialog removal to complete
time.sleep(0.3)

# Second pass: Remove fixed/sticky banners containing privacy-related keywords
driver.execute_script("""
    // Find and remove fixed-position elements at the top of the page
    // that contain cookie/privacy-related text content
    document.querySelectorAll('*').forEach(function(el) {
        try {
            var style = getComputedStyle(el);
            var rect = el.getBoundingClientRect();

            // Check if element is fixed/sticky and positioned at top of viewport
            if ((style.position === 'fixed' || style.position === 'sticky') && rect.top < 100) {
                var text = el.innerText.toLowerCase();

                // Remove if contains privacy-related keywords
                if (text.includes('cookie') || text.includes('privacy') || text.includes('consent') ||
                    text.includes('analytics') || text.includes('advertising') || text.includes('personalization')) {
                    el.remove();
                }
            }
        } catch(e) {}
    });
""")
print("✅ Cookie dialogs hidden")


# =============================================================================
# STEP 3: Scroll Through All Pages to Load Content
# =============================================================================
# Scribd uses lazy-loading for document pages. We need to scroll through
# the entire document to ensure all pages are rendered before generating PDF.

page_elements = driver.find_elements("css selector", "[class*='page']")
total_pages = len(page_elements)
print(f"📄 Found {total_pages} pages, scrolling...")

# Scroll through each page with minimal delay
# Using 'instant' scroll behavior for speed
for i, page in enumerate(page_elements):
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant'});", page)

    # Brief pause to allow content to render (150ms is usually sufficient)
    time.sleep(0.15)

    # Display progress for longer documents
    if (i + 1) % 10 == 0:
        print(f"   Scrolled {i + 1}/{total_pages} pages...")

print(f"✅ All {total_pages} pages loaded")

# Brief pause after scrolling to ensure final renders complete
time.sleep(0.5)


# =============================================================================
# STEP 4: Remove Scribd UI Elements
# =============================================================================
# Remove toolbars and reset scroll container classes that could interfere
# with PDF generation. This is done in a single JavaScript call for efficiency.

result = driver.execute_script("""
    var removed = {toolbar_top: false, toolbar_bottom: false, containers: 0};

    // Remove top toolbar (navigation, share buttons, etc.)
    var toolbarTop = document.querySelector('.toolbar_top');
    if (toolbarTop) {
        toolbarTop.remove();
        removed.toolbar_top = true;
    }

    // Remove bottom toolbar (page navigation, zoom controls, etc.)
    var toolbarBottom = document.querySelector('.toolbar_bottom');
    if (toolbarBottom) {
        toolbarBottom.remove();
        removed.toolbar_bottom = true;
    }

    // Reset document scroller class to prevent scroll-related CSS issues
    document.querySelectorAll('.document_scroller').forEach(function(el) {
        el.setAttribute('class', '');
        removed.containers++;
    });

    return removed;
""")

# Log what was removed
if result['toolbar_top']:
    print("✅ Top toolbar removed")
if result['toolbar_bottom']:
    print("✅ Bottom toolbar removed")
print(f"✅ Cleaned {result['containers']} scroll containers")


# =============================================================================
# STEP 5: Inject Print-Optimized CSS
# =============================================================================
# Add CSS rules to ensure clean PDF output:
# - Hide any remaining cookie/consent elements
# - Set proper page size and margins for print
# - Remove browser default print headers/footers

driver.execute_script("""
    var style = document.createElement('style');
    style.id = 'scribd-print-styles';
    style.textContent = `
        /* Hide cookie/consent elements on screen (backup) */
        [class*="cookie"],
        [class*="Cookie"],
        [class*="consent"],
        [class*="Consent"],
        [class*="gdpr"],
        [class*="privacy-notice"],
        [class*="notice-banner"],
        [id*="cookie"],
        [id*="consent"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            height: 0 !important;
            overflow: hidden !important;
        }

        /* Print-specific styles */
        @media print {
            /* Page configuration: Executive size with no margins */
            @page {
                size: 7.25in 10.5in;
                margin: 0;
            }

            /* Ensure toolbars are hidden */
            .toolbar_top, .toolbar_bottom {
                display: none !important;
            }

            /* Remove default browser margins */
            html {
                margin: 0 !important;
                padding: 0 !important;
            }

            /* Hide all privacy/cookie elements in print output */
            [class*="cookie"],
            [class*="Cookie"],
            [class*="consent"],
            [class*="Consent"],
            [class*="gdpr"],
            [class*="privacy"],
            [class*="notice"],
            [class*="banner"],
            [id*="cookie"],
            [id*="consent"],
            [id*="gdpr"] {
                display: none !important;
                visibility: hidden !important;
            }
        }
    `;
    document.head.appendChild(style);
""")
print("✅ Print CSS injected")


# =============================================================================
# STEP 6: Generate and Save PDF
# =============================================================================
# Scroll back to top before generating PDF to ensure proper page order

driver.execute_script("window.scrollTo(0, 0);")

# Display PDF settings
print(f"\n📥 Saving PDF as: {pdf_filename}")
print("   Page size: Executive (7.25\" x 10.5\")")
print("   Margins: None")
print("   Headers/Footers: Disabled")

# Generate and save the PDF
saved_path = save_pdf_directly(driver, pdf_filename)

if saved_path:
    print(f"✅ PDF saved successfully to: {saved_path}")

    # Clean up: close the browser
    driver.quit()
    print("🔒 Browser closed")
else:
    # Fallback: open print dialog if direct PDF save fails
    print("⚠️ Auto-save failed. Opening print dialog as fallback...")
    driver.execute_script("window.print();")
