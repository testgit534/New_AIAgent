from playwright.sync_api import sync_playwright


def crawl_pages(url: str) -> list:

    crawled_pages = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        print(f"[Crawler] Opening: {url}")

        page.goto(
            url,
            wait_until="networkidle",
            timeout=30000
        )

        visited_urls = set()

        links = page.locator("a").evaluate_all(
            """
            elements => elements
                .map(el => el.href)
                .filter(href => href)
            """
        )

        links = [url] + links[:4]

        for link in links:

            if link in visited_urls:
                continue

            visited_urls.add(link)

            try:

                page.goto(
                    link,
                    wait_until="networkidle",
                    timeout=30000
                )

                title = page.title()

                html = page.content()

                crawled_pages.append({
                    "page_url": link,
                    "page_title": title,
                    "html": html
                })

                print(f"[Crawler] Crawled: {title}")

            except Exception as e:

                print(f"[Crawler] Failed: {link}")

        browser.close()

    return crawled_pages