"""
Playwright tests to identify CSS and UI issues across the CodeVenture application.

Tests:
1. Whitespace issues at the bottom of learning and quiz module pages
2. Missing CSS on quiz concept_modules pages
3. Navbar alignment with page content
4. Responsive behavior across different devices
"""

import asyncio
from playwright.async_api import async_playwright
import json


async def test_page_layout(browser):
    """Test page layouts for whitespace and CSS issues."""

    context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
    page = await context.new_page()

    results = {
        'viewport': '1920x1080 (Desktop)',
        'tests': []
    }

    # Test pages
    test_urls = [
        {
            'name': 'Basic Modules Page',
            'url': 'http://127.0.0.1:8000/learning/basic_module/'
        },
        {
            'name': 'Concept Modules Page',
            'url': 'http://127.0.0.1:8000/learning/concept_module/'
        },
        {
            'name': 'Quiz Modules Page',
            'url': 'http://127.0.0.1:8000/quiz/modules/'
        },
        {
            'name': 'Quiz Concept Modules Page (example)',
            'url': 'http://127.0.0.1:8000/quiz/concept_modules/5/'
        }
    ]

    for test_url in test_urls:
        test_result = {
            'page': test_url['name'],
            'url': test_url['url'],
            'issues': []
        }

        try:
            response = await page.goto(test_url['url'], wait_until='networkidle', timeout=10000)

            if response.status != 200:
                test_result['issues'].append(f'HTTP {response.status} error')
                results['tests'].append(test_result)
                continue

            # Take screenshot
            screenshot_name = test_url['name'].lower().replace(' ', '_').replace('(', '').replace(')', '')
            await page.screenshot(path=f'screenshots/{screenshot_name}_desktop.png', full_page=True)

            # Check for whitespace at bottom
            body_height = await page.evaluate('document.body.scrollHeight')
            viewport_height = await page.evaluate('window.innerHeight')
            window_height = await page.evaluate('window.outerHeight')

            # Check background color consistency
            body_bg = await page.evaluate('window.getComputedStyle(document.body).backgroundColor')

            # Get all wrapper divs with page classes
            wrappers = await page.query_selector_all('[class*="-page"]')
            wrapper_info = []
            for wrapper in wrappers:
                class_name = await wrapper.get_attribute('class')
                computed_bg = await wrapper.evaluate('el => window.getComputedStyle(el).backgroundColor', wrapper)
                min_height = await wrapper.evaluate('el => window.getComputedStyle(el).minHeight', wrapper)
                height = await wrapper.evaluate('el => window.getComputedStyle(el).height', wrapper)
                wrapper_info.append({
                    'class': class_name,
                    'background': computed_bg,
                    'minHeight': min_height,
                    'height': height
                })

            # Check navbar
            navbar = await page.query_selector('nav, .site-nav, [class*="nav"]')
            navbar_info = {}
            if navbar:
                navbar_height = await navbar.evaluate('el => el.offsetHeight')
                navbar_width = await navbar.evaluate('el => el.offsetWidth')
                navbar_padding = await navbar.evaluate('el => window.getComputedStyle(el).padding')
                navbar_info = {
                    'height': navbar_height,
                    'width': navbar_width,
                    'padding': navbar_padding
                }

            # Check content containers
            containers = await page.query_selector_all('.module-container, .concept-modules-parent, .links4')
            container_info = []
            for container in containers:
                class_name = await container.get_attribute('class')
                max_width = await container.evaluate('el => window.getComputedStyle(el).maxWidth', container)
                margin = await container.evaluate('el => window.getComputedStyle(el).margin', container)
                padding = await container.evaluate('el => window.getComputedStyle(el).padding', container)
                container_info.append({
                    'class': class_name,
                    'maxWidth': max_width,
                    'margin': margin,
                    'padding': padding
                })

            # Detect whitespace issue
            if body_height > viewport_height * 1.1:  # More than 10% extra height suggests whitespace
                test_result['issues'].append(f'Excess whitespace detected (body: {body_height}px, viewport: {viewport_height}px)')

            test_result['metrics'] = {
                'bodyHeight': body_height,
                'viewportHeight': viewport_height,
                'bodyBackground': body_bg,
                'wrappers': wrapper_info,
                'navbar': navbar_info,
                'containers': container_info
            }

        except Exception as e:
            test_result['issues'].append(f'Error: {str(e)}')

        results['tests'].append(test_result)

    await context.close()
    return results


async def test_mobile_layout(browser):
    """Test mobile responsive behavior."""

    # Test various mobile viewports
    viewports = [
        {'width': 375, 'height': 667, 'name': 'iPhone SE'},
        {'width': 390, 'height': 844, 'name': 'iPhone 12'},
        {'width': 768, 'height': 1024, 'name': 'iPad'},
    ]

    all_results = []

    for viewport in viewports:
        context = await browser.new_context(viewport={'width': viewport['width'], 'height': viewport['height']})
        page = await context.new_page()

        results = {
            'viewport': f"{viewport['width']}x{viewport['height']} ({viewport['name']})",
            'tests': []
        }

        # Test basic modules page on mobile
        try:
            await page.goto('http://127.0.0.1:8000/learning/basic_module/', wait_until='networkidle', timeout=10000)

            screenshot_name = f"{viewport['name'].replace(' ', '_').lower()}_basic_modules"
            await page.screenshot(path=f'screenshots/{screenshot_name}.png', full_page=True)

            # Check navbar responsiveness
            navbar = await page.query_selector('.site-nav')
            if navbar:
                navbar_width = await navbar.evaluate('el => el.offsetWidth')
                results['tests'].append({
                    'page': 'Basic Modules (Mobile)',
                    'navbar_width': navbar_width,
                    'viewport_width': viewport['width']
                })
        except Exception as e:
            results['tests'].append({'error': str(e)})

        await context.close()
        all_results.append(results)

    return all_results


async def main():
    """Run all tests."""

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        print("Running desktop layout tests...")
        desktop_results = await test_page_layout(browser)

        print("Running mobile layout tests...")
        mobile_results = await test_mobile_layout(browser)

        await browser.close()

        # Save results
        all_results = {
            'desktop': desktop_results,
            'mobile': mobile_results
        }

        with open('test_results.json', 'w') as f:
            json.dump(all_results, f, indent=2)

        print("\n" + "="*60)
        print("TEST RESULTS SUMMARY")
        print("="*60)

        for test in desktop_results['tests']:
            print(f"\n{test['page']}:")
            print(f"  URL: {test['url']}")
            if test['issues']:
                print("  Issues:")
                for issue in test['issues']:
                    print(f"    - {issue}")
            else:
                print("  ✓ No issues detected")

            if 'metrics' in test and test['metrics']['wrappers']:
                print("  Wrapper info:")
                for wrapper in test['metrics']['wrappers']:
                    print(f"    - {wrapper['class']}: bg={wrapper['background']}, minHeight={wrapper['minHeight']}")

        print("\nResults saved to test_results.json")
        print("Screenshots saved to screenshots/ directory")


if __name__ == '__main__':
    asyncio.run(main())
