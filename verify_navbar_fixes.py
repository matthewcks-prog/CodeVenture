"""
Manual verification script for navbar and layout fixes.
Tests:
1. Body background color (whitesmoke) extends to bottom
2. Profile picture displays (not SVG placeholder)
3. Profile dropdown toggle behavior
"""

import asyncio
from playwright.async_api import async_playwright
import json

async def verify_fixes():
    results = {
        "body_background": {},
        "profile_dropdown": {},
        "pages_tested": []
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        pages_to_test = [
            "http://127.0.0.1:8000/learning/basic_module/",
            "http://127.0.0.1:8000/learning/concept_module/",
            "http://127.0.0.1:8000/quiz/modules/"
        ]

        for url in pages_to_test:
            print(f"\n🔍 Testing: {url}")
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(1000)

            # Test 1: Body background color
            body_bg = await page.evaluate("() => getComputedStyle(document.body).backgroundColor")
            body_height = await page.evaluate("() => document.body.scrollHeight")
            viewport_height = await page.evaluate("() => window.innerHeight")

            print(f"   Body background: {body_bg}")
            print(f"   Body height: {body_height}px, Viewport: {viewport_height}px")

            results["pages_tested"].append({
                "url": url,
                "body_bg": body_bg,
                "body_height": body_height,
                "viewport_height": viewport_height,
                "has_whitespace": body_height < viewport_height
            })

            # Test 2: Profile picture (only if authenticated)
            profile_pic = page.locator("#profilePic img")
            if await profile_pic.is_visible():
                pic_src = await profile_pic.get_attribute("src")
                is_svg_data_uri = pic_src.startswith("data:image/svg+xml")

                print(f"   Profile picture: {'SVG data URI (BAD)' if is_svg_data_uri else 'Image file (GOOD)'}")
                results["profile_dropdown"]["has_profile_pic"] = True
                results["profile_dropdown"]["uses_data_uri"] = is_svg_data_uri
                results["profile_dropdown"]["pic_src"] = pic_src[:100] + "..." if len(pic_src) > 100 else pic_src

                # Test 3: Dropdown toggle
                dropdown = page.locator("#dropView")

                # Click profile pic - should open
                await profile_pic.click()
                await page.wait_for_timeout(300)
                is_open_after_first_click = await dropdown.evaluate("el => el.style.display === 'flex'")

                # Click again - should close
                await profile_pic.click()
                await page.wait_for_timeout(300)
                is_closed_after_second_click = await dropdown.evaluate("el => el.style.display === 'none'")

                # Open again and test Escape
                await profile_pic.click()
                await page.wait_for_timeout(300)
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(300)
                is_closed_after_escape = await dropdown.evaluate("el => el.style.display === 'none'")

                print(f"   Dropdown opens on click: {is_open_after_first_click}")
                print(f"   Dropdown closes on second click: {is_closed_after_second_click}")
                print(f"   Dropdown closes on Escape: {is_closed_after_escape}")

                results["profile_dropdown"]["toggle_works"] = is_open_after_first_click and is_closed_after_second_click
                results["profile_dropdown"]["escape_works"] = is_closed_after_escape

            # Take screenshot
            screenshot_path = f"screenshots/verify_{url.split('/')[-2]}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"   Screenshot saved: {screenshot_path}")

        await browser.close()

    # Save results
    with open("verification_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n✅ Verification complete! Results saved to verification_results.json")
    return results

if __name__ == "__main__":
    asyncio.run(verify_fixes())
