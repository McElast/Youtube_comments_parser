from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

EN = ('K', 'M', 'Chanel: ', 'Subscribers: ', 'Video title: ', 'URL: ', 'Date: ',
      'Views: ', 'Likes: ', 'Dislikes: ', 'Description: ', '----- Comments -------', 'Show more replies')
RU = ('ТЫС.', 'МЛН', 'Канал: ', 'Подписчиков: ', 'Ролик: ', 'Ссылка на видео: ', 'Дата публикации: ',
      'Просмотров: ', 'Лайков: ', 'Дизлайков: ', 'Описание: ', '----- Комментарии -------', 'Другие ответы')


def num_to_str(w, lang=RU):
    if lang[0] in w.upper():
        num = int(float(w.split()[0].replace(',', '.')) * 1000)
    elif lang[1] in w.upper():
        num = int(float(w.split()[0].replace(',', '.')) * 1_000_000)
    else:
        num = int(w.split()[0])
    return num


def subscr(w, lang=RU):
    if lang[0] in w[1] or lang[0].lower() in w[1]:
        num = int(float(w[0].replace(',', '.')) * 1000)
    elif lang[1] in w[1] or lang[1].lower() in w[1]:
        num = int(float(w[0].replace(',', '.')) * 1_000_000)
    else:
        num = int(w[0])
    return num


def parse(url, lang=RU):
    opt = Options()
    opt.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/80.0.3987.116 Safari/537.36')
    opt.add_argument("--disable-notifications")
    pref = {"profile.managed_default_content_settings.images": 2}
    opt.add_experimental_option('prefs', pref)
    browser = Chrome(executable_path='chromedriver.exe', options=opt)
    browser.maximize_window()

    def bad(driver):
        bd = driver.find_elements_by_css_selector('div.ytd-mealbar-promo-renderer')
        if len(bd) > 0 and bd[0].is_displayed():
            bd[0].find_element_by_tag_name('a').send_keys(Keys.ESCAPE)

    browser.get(url)
    browser.implicitly_wait(10)
    browser.find_element_by_css_selector('paper-toggle-button#toggle').click()
    print('...Autoplay off...')
    output = browser.title.split()[0] + '.txt'

    with open(output, 'w', encoding='utf8') as f:
        title = browser.find_element_by_css_selector('h1.title').text.strip()
        views = browser.find_element_by_css_selector('span.yt-view-count-renderer').text.strip()
        views = int(''.join([i for i in views if i != ' ' and not i.isalpha()]))
        date_p = browser.find_element_by_css_selector('div#date').text.strip()
        date_p = date_p.replace('•', '')
        tmp = browser.find_element_by_css_selector('div#top-level-buttons').text.strip().split('\n')
        likes = num_to_str(tmp[0], lang=RU)
        dis = num_to_str(tmp[1], lang=RU)
        chanel = browser.find_element_by_css_selector('div#text-container').text.strip()
        subscribers = browser.find_element_by_css_selector('yt-formatted-string#owner-sub-count').text.strip().split()
        try:
            subscribers = subscr(subscribers, lang=RU)
        except Exception:
            subscribers = '-'
        desc_presence = browser.find_elements_by_css_selector('yt-formatted-string.more-button')
        if len(desc_presence) > 0:
            desc_presence[0].click()
        desc = browser.find_element_by_css_selector('yt-formatted-string.content').text.strip().replace('\n', '')
        print(lang[2], chanel, file=f)
        print(lang[3], subscribers, file=f)
        print(lang[4], title, file=f)
        print(lang[5], url, file=f)
        print(lang[6], date_p, file=f)
        print(lang[7], views, file=f)
        print(lang[8], likes, file=f)
        print(lang[9], dis, file=f)
        print(lang[10], desc, file=f)
        print(lang[11], file=f)
    divs1, divs2 = 0, []
    browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    cnt = 0
    for i in range(1, 777777777777777777):
        browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        sleep(1)
        if i == 10:
            bad(driver=browser)
            browser.find_element_by_tag_name('body').send_keys(Keys.SPACE)
            print('....Video paused....')
        divs2 = browser.find_elements_by_css_selector('ytd-comment-thread-renderer.style-scope')
        if len(divs2) == divs1:
            cnt += 1
            if cnt == 5:
                break
        else:
            cnt = 0
        divs1 = len(divs2)
    bad(driver=browser)
    for k in divs2:
        print('....... Comment ', divs2.index(k) + 1, '/', len(divs2), '..........')
        author = k.find_element_by_css_selector('a#author-text').text.strip()
        if len(author) == 0:
            author = k.find_element_by_css_selector('yt-formatted-string#text').text.strip()
        when = k.find_element_by_css_selector('yt-formatted-string.published-time-text').text.strip()
        text = k.find_element_by_css_selector('yt-formatted-string#content-text').text.strip().replace('\n', '')
        with open(output, 'a', encoding='utf8') as f:
            print(author, ' (', when, ')', file=f, sep='')
            print('  ', text, file=f, sep='')
            repl_p = k.find_elements_by_css_selector('div#replies')
            if repl_p[0].get_attribute('hidden') != 'true':
                q = repl_p[0].find_elements_by_css_selector('a.yt-simple-endpoint')[0]
                bad(driver=browser)
                q.send_keys(Keys.ARROW_UP)
                sleep(1.5)
                if q.is_displayed():
                    q.click()
                    sleep(1)
                while True:
                    nex = k.find_elements_by_css_selector('yt-formatted-string.yt-next-continuation')
                    nex = [i for i in nex if i.text.strip() == lang[12]]
                    txt = [i.text.strip() for i in nex]
                    if lang[12] not in txt:
                        break
                    for _ in nex:
                        t = 0
                        while t < 5:
                            try:
                                if _.is_displayed():
                                    browser.execute_script("arguments[0].scrollIntoView(false);", _)
                                    _.click()
                                    sleep(1)
                                    t = 0
                            except Exception:
                                t += 1
                replies = k.find_element_by_css_selector('div#loaded-replies')
                replies = replies.find_elements_by_css_selector('ytd-comment-renderer')
                for s in replies:
                    print('\tAnswer ', replies.index(s) + 1, ' / ', len(replies))
                    rep_auth = s.find_element_by_css_selector('a#author-text').text.strip()
                    if len(rep_auth) == 0:
                        rep_auth = s.find_element_by_css_selector('yt-formatted-string#text').text.strip()
                    rep_data = s.find_element_by_css_selector('yt-formatted-string.published-time-text').text.strip()
                    rep_text = s.find_element_by_css_selector('yt-formatted-string#content-text'). \
                        text.strip().replace('\n', '')
                    print('\t', rep_auth, ' (', rep_data, ')', file=f, sep='')
                    print('\t\t', rep_text, file=f)
    browser.close()


parse('https://www.youtube.com/watch?v=1E4RKg6z3r0', lang=RU)
