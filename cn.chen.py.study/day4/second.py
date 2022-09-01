from playwright.sync_api import sync_playwright


def on_response(response, url):
    if '/api/movie/' in response.url and response.status == 200:
        print("%s得到的响应为：" % url, response.json())


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    url = 'https://spa6.scrape.center/'
    page.on('response', lambda response: on_response(response, url))
    page.goto(url)
    page.wait_for_load_state('networkidle')
    browser.close()
