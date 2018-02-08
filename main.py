from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import urlretrieve
import csv
import os.path
import time
from bs4 import BeautifulSoup
# import pypyodbc
# sql.py import
# import sql

download_directory = os.path.dirname(__file__) + "/temp"
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': download_directory}
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome("C:/chromedriver.exe", chrome_options=chrome_options)
browser.maximize_window()


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def login():
    browser.get("https://www.mql5.com/en/auth_login")
    username = browser.find_element_by_id("Login")
    password = browser.find_element_by_id("Password")
    username.send_keys("hammadfozi")
    password.send_keys("ETP4s95L")
    elements = browser.find_elements_by_xpath("//*[@type='submit']")
    login_attempt = elements[1]
    login_attempt.submit()


def read_links():
    link = []
    file = open('links.txt', 'r')

    for line in file:
        if line[len(line)-1] is '\n':
            line = line[:-1]
        link.append(line)

    file.close()
    return link


# Step 2: Go to a link
def go_to_link(url_id):
    url = "https://www.mql5.com/en/signals/" + str(url_id)
    browser.get(url)


def get_error(link):
    data = []
    body = browser.find_element_by_class_name("body")
    section = body.find_elements_by_class_name("section")
    not_found = body.find_elements_by_class_name("pageNotFound")

    if section:
        item = []
        item.append(link)
        item.append("Disabled and Unavailable")
        data.append(item)

    elif not_found:
        item = []
        item.append(link)
        item.append("Not Exist")
        data.append(item)

    return data


def populate_main():
    data = []

    item = []
    item.append(link_id)

    path = browser.find_element_by_class_name("path")

    name = path.find_element_by_class_name("title-min")
    item.append(name.text)

    rating_area = path.find_element_by_class_name("rating")
    rating_area = rating_area.find_elements_by_xpath(".//*")
    info = rating_area[0].get_attribute("class")
    info = info[1:]
    if len(info) is 2:
        info = info[:1] + '.' + info[1:]
    item.append(info)

    rating_area = path.find_element_by_class_name("rating-area")
    rating_area = rating_area.find_elements_by_xpath(".//*")
    info = rating_area[0].get_attribute("title")
    pos = info.find(' ')
    info = info[:pos]
    if info == "No":
        info = "0"
    item.append(info)

    check_archive = browser.find_elements_by_class_name("priceArchive")
    if len(check_archive) is not 0:
        price = -1
    else:
        price = browser.find_element_by_class_name("price")
        price = price.find_elements_by_xpath(".//*")
        price = price[0].get_attribute("content")
    if price:
        item.append(price)
    else:
        item.append("0")

    overall_data = browser.find_elements_by_class_name("list")
    tooltip_data = overall_data[0].find_elements_by_class_name("item")

    growth = tooltip_data[0].find_element_by_class_name("header").find_element_by_tag_name("span").text
    growth = growth[:-1]

    tooltip_further_data = tooltip_data[0].find_element_by_class_name("tooltip").find_element_by_class_name("content").\
        find_elements_by_class_name("line")

    retry = True

    while retry:
        # print("Trying...")
        init_dep = tooltip_further_data[1].find_element_by_class_name("value").text
        deposits = tooltip_further_data[2].find_element_by_class_name("value").text
        withdrawals = tooltip_further_data[3].find_element_by_class_name("value").text
        balance = tooltip_further_data[4].find_element_by_class_name("value").text
        equity = tooltip_further_data[5].find_element_by_class_name("value").text
        tooltip_data[0].click()
        if init_dep and deposits and withdrawals and balance and equity:
            retry = False

    pos = init_dep.rfind(' ')
    currency = init_dep[pos+1:]
    init_dep = init_dep[:pos]
    init_dep = init_dep.replace(" ", "")
    pos = deposits.rfind(' ')
    deposits = deposits[:pos]
    deposits = deposits.replace(" ", "")
    pos = withdrawals.rfind(' ')
    withdrawals = withdrawals[:pos]
    withdrawals = withdrawals.replace(" ", "")
    pos = balance.rfind(' ')
    balance = balance[:pos]
    balance = balance.replace(" ", "")
    pos = equity.rfind(' ')
    equity = equity[:pos]
    equity = equity.replace(" ", "")

    if len(overall_data) is 3:
        tooltip_desc = overall_data[1].find_element_by_class_name("item").text
    else:
        tooltip_desc = ""

    index = 1

    profit = subs = subs_funds = max_dd = max_dd_amt = weeks = latest_trade = trades_per_week = avg_holding_time = \
        profit_tool_tip = ""

    if index <= (len(tooltip_data) - 1):
        name = tooltip_data[index].find_element_by_class_name("header").text
        pos = name.find(":")
        name = name[:pos]
        if name == "Profit" and index <= (len(tooltip_data)-1):
            profit = tooltip_data[index].find_element_by_class_name("header").find_element_by_tag_name("span").text
            pos = profit.rfind(' ')
            profit = profit[:pos]
            profit = profit.replace(" ", "")
            index = index + 1

    info = overall_data[0].find_elements_by_class_name("info")
    if info:
        # print(len(info))
        # new_info = info[0].find_element_by_tag_name("p")
        profit_tool_tip = info[0].text
        # print(profit_tool_tip)

    if index <= (len(tooltip_data) - 1):
        name = tooltip_data[index].find_element_by_class_name("header").text
        pos = name.find(":")
        name = name[:pos]
        if name == "Subscribers":
            subs = tooltip_data[index].find_element_by_class_name("header").find_element_by_tag_name("span").text
            index = index + 1

    if index <= (len(tooltip_data) - 1):
        name = tooltip_data[index].find_element_by_class_name("header").text
        pos = name.find(":")
        name = name[:pos]
        if name == "Subscribers' funds" and index <= (len(tooltip_data)-1):
            subs_funds = tooltip_data[index].find_element_by_class_name("header").find_element_by_tag_name("span").text
            subs_funds = subs_funds[:-4]
            index = index + 1

    if index <= (len(tooltip_data) - 1):
        name = tooltip_data[index].find_element_by_class_name("header").text
        pos = name.find(":")
        name = name[:pos]
        if name == "Maximum drawdown":
            max_dd = tooltip_data[index].find_element_by_class_name("header").find_element_by_tag_name("span").text
            max_dd = max_dd[:-1]

            max_dd_amt = tooltip_data[index].get_attribute("title")
            pos = max_dd_amt.rfind(' ')
            max_dd_amt = max_dd_amt[:pos]
            pos = max_dd_amt.rfind(' ')
            max_dd_amt = max_dd_amt[pos+1:]
            index = index + 1

    if index <= (len(tooltip_data) - 1):
        name = tooltip_data[index].find_element_by_class_name("header").text
        pos = name.find(":")
        name = name[:pos]
        if name == "Weeks":
            weeks = tooltip_data[index].find_element_by_class_name("header").find_element_by_tag_name("span").text
            index = index + 1

    if index <= (len(tooltip_data) - 1):
        name = tooltip_data[index].find_element_by_class_name("header").text
        pos = name.find(":")
        name = name[:pos]
        if name == "Latest trade":
            latest_trade = tooltip_data[index].find_element_by_class_name("header").find_element_by_tag_name("span").text
            pos = latest_trade.find(' ')
            unit = latest_trade[pos+1:]
            latest_trade = latest_trade[:pos]
            latest_trade = int(latest_trade)
            if unit == "days ago" or unit == "day ago":
                latest_trade = latest_trade * 1440
            elif unit == "hour ago" or unit == "hours ago":
                latest_trade = latest_trade * 60
            else:
                print("ERROR IN LATEST TRADE [CHECK]")
                print("UNIT: " + unit)
            index = index + 1

    if index <= (len(tooltip_data) - 1):
        name = tooltip_data[index].find_element_by_class_name("header").text
        pos = name.find(":")
        name = name[:pos]
        if name == "Trades per week" and index <= (len(tooltip_data)-1):
            trades_per_week = tooltip_data[index].find_element_by_class_name("header").find_element_by_tag_name("span").text
            index = index + 1

    if index <= (len(tooltip_data) - 1):
        name = tooltip_data[index].find_element_by_class_name("header").text
        pos = name.find(":")
        name = name[:pos]
        if name == "Avg holding time" and index <= (len(tooltip_data)-1):
            avg_holding_time = tooltip_data[index].find_element_by_class_name("header").find_element_by_tag_name(
                "span").text
            pos = avg_holding_time.find(' ')
            unit = avg_holding_time[pos+1:]
            avg_holding_time = avg_holding_time[:pos]
            avg_holding_time = int(avg_holding_time)
            if unit == "minutes":
                avg_holding_time = avg_holding_time * 60
            elif unit == "hours":
                avg_holding_time = avg_holding_time * 3600
            elif unit == "days" or unit == "day":
                avg_holding_time = avg_holding_time * 86400
            else:
                print("ERROR in Avg Holding time [Check]")
                print("UNIT: " + unit)

    more_data = overall_data[-1].find_elements_by_class_name("item")

    broker_data = more_data[0].find_element_by_class_name("header").find_element_by_tag_name("form")
    broker = broker_data.text
    broker_name = broker_data.find_element_by_tag_name("span").find_element_by_tag_name("a").get_attribute("title")
    pos = broker_name.find("(")
    broker_name = broker_name[pos+1:-1]
    leverage = more_data[1].find_element_by_class_name("header").find_element_by_tag_name("span").text
    pos = leverage.find(":")
    leverage = leverage[pos+1:]
    trading_mode = more_data[2].find_element_by_class_name("header").find_element_by_tag_name("span").text
    author_data = more_data[3].find_element_by_class_name("header").find_element_by_tag_name("span")
    author = author_data.text
    author_code = author_data.find_element_by_tag_name("a").get_attribute("title")

    item.append(growth)
    item.append(tooltip_desc)
    item.append(currency)
    item.append(init_dep)
    item.append(deposits)
    item.append(withdrawals)
    item.append(balance)
    item.append(equity)
    item.append(profit)
    item.append(profit_tool_tip)
    item.append(subs)
    item.append(subs_funds)
    item.append(max_dd)
    item.append(max_dd_amt)
    item.append(weeks)
    item.append(latest_trade)
    item.append(trades_per_week)
    item.append(avg_holding_time)
    item.append(broker)
    item.append(broker_name)
    item.append(leverage)
    item.append(trading_mode)
    item.append(author)
    item.append(author_code)

    html = str(browser.page_source)
    x_axis_data = html[html.find('Signals.ReturnChartIndex = ') + 27: html.find('Signals.BalanceChartData =')]
    x_axis_data = x_axis_data.strip()
    x_axis_data = x_axis_data[:len(x_axis_data) - 1]

    equity_start_date = x_axis_data[find_nth(x_axis_data, "},'", 2) + 3: find_nth(x_axis_data, "':{", 3)]
    if len(equity_start_date) is 6 or len(equity_start_date) is 7:
        pos = equity_start_date.find('.')
        month = equity_start_date[pos+1:]
        if month == "1" or month == "3" or month == "5" or month == "7" or month == "8" or month == "10" or month == "12":
            day = "31"
        elif month == "2":
            day = "28"
        else:
            day = "30"
        equity_start_date = equity_start_date[:] + "." + day
    item.append(equity_start_date)

    # Collecting Stats
    browser.find_element_by_id("tab_stats").click()
    info = browser.find_element_by_id("tab_content_stats")
    columns = info.find_elements_by_class_name("value")

    for i in range(len(columns)):
        data_to_append = columns[i].text
        if i is 0:
            data_to_append = data_to_append.replace(" ", "")
        if i is 1 or i is 2 or i is 13 or i is 14:
            pos = data_to_append.find('(')
            data_to_append_2 = data_to_append[pos+1:-2]
            data_to_append = data_to_append[:pos-1]
            data_to_append = data_to_append.replace(" ", "")
            item.append(data_to_append)
            data_to_append = data_to_append_2
        elif i is 3 or i is 4 or i is 16 or i is 17 or i is 18:
            pos = data_to_append.rfind(' ')
            data_to_append = data_to_append[:pos]
            data_to_append = data_to_append.replace(" ", "")
        elif i is 5 or i is 6:
            pos = data_to_append.find('(')
            data_to_append_2 = data_to_append[pos+1:-6]
            data_to_append = data_to_append[:pos-1]
            pos = data_to_append.rfind(' ')
            data_to_append = data_to_append[:pos]
            data_to_append = data_to_append.replace(" ", "")
            data_to_append_2 = data_to_append_2.replace(" ", "")
            item.append(data_to_append)
            data_to_append = data_to_append_2
        elif i is 7 or i is 19:
            pos = data_to_append.find('(')
            pos2 = data_to_append.rfind(' ')
            data_to_append_2 = data_to_append[pos+1:pos2]
            data_to_append = data_to_append[:pos-1]
            data_to_append = data_to_append.replace(" ", "")
            data_to_append_2 = data_to_append_2.replace(" ", "")
            item.append(data_to_append)
            data_to_append = data_to_append_2
        elif i is 8 or i is 20:
            pos = data_to_append.find('(')
            data_to_append_2 = data_to_append[pos+1:-1]
            data_to_append = data_to_append[:pos-1]
            pos = data_to_append.rfind(' ')
            data_to_append = data_to_append[:pos]
            data_to_append = data_to_append.replace(" ", "")
            data_to_append_2 = data_to_append_2.replace(" ", "")
            item.append(data_to_append)
            data_to_append = data_to_append_2
        elif i is 10 or i is 11 or i is 21 or i is 22 or i is 23:
            data_to_append = data_to_append[:-1]
        item.append(data_to_append)

    # Collecting Risks
    browser.find_element_by_id("tab_risks").click()
    info = browser.find_elements_by_class_name("signals-data-columns")
    cols = info[1].find_elements_by_class_name("column")
    for col in cols:
        all_val = col.find_elements_by_class_name("hoverable")
        for i in range(len(all_val)):
            val = all_val[i].find_element_by_class_name("value").text
            if i is 0 or i is 3:
                pos = val.rfind(' ')
                val = val[:pos]
                val = val.replace(" ", "")
                # val = val[:-3]
            elif i is 1 or i is 4:
                pos = val.find(' ')
                pos2 = val.rfind(' ')
                val_2 = val[pos+2:pos2]
                val_2 = val_2.replace(" ", "")
                val = val[:pos]
                item.append(val)
                val = val_2
            elif i is 2 or i is 5:
                pos = val.rfind(' ')
                val_2 = val[pos+2:-1]
                val = val[:pos]
                pos = val.rfind(' ')
                val = val[:pos]
                val = val.replace(" ", "")
                # val = val[:-3]
                item.append(val)
                val = val_2
            item.append(val)

    cols = info[2].find_elements_by_class_name("column")
    all_val = cols[0].find_elements_by_class_name("item")
    dd_bal_abs = all_val[1].find_element_by_class_name("value").text
    pos = dd_bal_abs.rfind(' ')
    dd_bal_abs = dd_bal_abs[:pos]
    item.append(dd_bal_abs)

    dd_bal_max = all_val[2].find_element_by_class_name("value").text
    pos = dd_bal_max.rfind(' ')
    dd_bal_max_pct = dd_bal_max[pos + 2:-2]
    dd_bal_max_amt = dd_bal_max[:pos]
    pos = dd_bal_max_amt.rfind(' ')
    dd_bal_max_amt = dd_bal_max_amt[:pos]
    dd_bal_max_amt = dd_bal_max_amt.replace(" ", "")
    item.append(dd_bal_max_amt)
    item.append(dd_bal_max_pct)

    all_val = cols[1].find_elements_by_class_name("item")
    rdd_bal = all_val[1].find_element_by_class_name("value").text
    pos = rdd_bal.find(' ')
    pos2 = rdd_bal.rfind(' ')
    rdd_bal_amt = rdd_bal[pos+2:pos2]
    rdd_bal_amt = rdd_bal_amt.replace(" ", "")
    rdd_bal_pct = rdd_bal[:pos-1]
    item.append(rdd_bal_amt)
    item.append(rdd_bal_pct)

    all_val = cols[1].find_elements_by_class_name("item")
    rdd_equity = all_val[2].find_element_by_class_name("value").text
    pos = rdd_equity.find(' ')
    pos2 = rdd_equity.rfind(' ')
    rdd_equity_amt = rdd_equity[pos+2:pos2]
    rdd_equity_amt = rdd_equity_amt.replace(" ", "")
    rdd_equity_pct = rdd_equity[:pos-1]
    item.append(rdd_equity_amt)
    item.append(rdd_equity_pct)

    table = browser.find_element_by_class_name("signals-chart-dist").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    symbols_count = len(table) - 1
    item.append(symbols_count)

    data.append(item)

    return data


def populate_positions():
    data = []
    table = browser.find_elements_by_class_name("signal-info-table")

    if table:
        err = table[0].find_element_by_tag_name("tbody").find_element_by_tag_name("tr").find_element_by_tag_name("td").text
        if "Paid" not in err and "positions" not in err:
            all_rows = table[0].find_elements_by_tag_name("tr")

            for i in range(len(all_rows)):
                if i is not 0:
                    cells = all_rows[i].find_elements_by_xpath("./*")
                    row_data = []
                    row_data.append(link_id)

                    for item in cells:
                        item_data = ""

                        if len(item.text) is not 0:
                            item_data = item.text

                        row_data.append(item_data)

                    data.append(row_data)

    # Remove last row
    # data = data[:-1]
    return data


def populate_history(link, no_of_rows_to_read):
    data = []

    browser.find_element_by_id("tab_trading").click()

    # table = browser.find_elements_by_class_name("signal-info-table")[1]
    # all_rows = table.find_elements_by_tag_name("tr")
    # row_counter = -1
    #
    # for row in all_rows:
    #     row_counter = row_counter + 1
    #     if row_counter is not 0:
    #         cells = row.find_elements_by_xpath("./*")
    #         col = -1
    #         row_data = []
    #         row_data.append(link_id)
    #
    #         for item in cells:
    #             col = col + 1
    #             item_data = ""
    #
    #             if len(item.text) is not 0:
    #                 item_data = item.text
    #
    #             row_data.append(item_data)
    #
    #         data.append(row_data)

    csv_download_url = browser.current_url + "/export/history"
    # print(csv_download_url)
    browser.get(csv_download_url)

    filename = os.path.dirname(__file__) + "/temp/" + link + ".history.csv"

    while not os.path.exists(filename):
        time.sleep(1)

    with open(filename, newline='') as File:
        reader = csv.reader(File, delimiter=';')
        counter = 0
        for row in reader:
            row.insert(0, link_id)
            if counter is not 0 and counter < no_of_rows_to_read:
                data.append(row)
            counter = counter + 1

    return data


def populate_symbols():
    data = []

    browser.find_element_by_id("tab_stats").click()
    table = browser.find_element_by_id("tab_content_stats").find_elements_by_tag_name("table")[0]
    # print(table.text)

    rows = table.find_elements_by_tag_name("tr")

    for row in range(len(rows) - 1):
        if row > 0:
            cells = rows[row].find_elements_by_xpath("./*")

            row_data = []
            row_data.append(link_id)

            row_data.append(cells[0].text)

            trades = cells[1].text

            sell = cells[3].get_attribute("title")
            sell = sell[sell.index(':') + 2:]

            buy = cells[4].get_attribute("title")
            buy = buy[buy.index(':') + 2:]

            row_data.append(trades)
            row_data.append(sell)
            row_data.append(buy)

            data.append(row_data)

    return data


def populate_slippage():
    data = []
    browser.find_element_by_id("tab_slippage").click()
    table = browser.find_elements_by_id("slippagePlaceholder")

    if table:
        all_rows = table[0].find_elements_by_tag_name("tr")

        for i in range(len(all_rows)):

            if i % 2 is 0:
                row_data = []
                row_data.append(link_id)

                title = all_rows[i].find_element_by_tag_name("span")
                row_data.append(title.text)

                val1 = all_rows[i].find_element_by_class_name("bar")
                val_text = val1.text
                amount = val_text[:4]
                amount2 = val_text[7:]
                row_data.append(amount)
                row_data.append(amount2)

                data.append(row_data)

    return data


def populate_description():
    data = []
    desc_tab = browser.find_elements_by_id("tab_description")

    if desc_tab:
        desc_tab[0].click()

        browser.find_element_by_id("tab_content_description").find_element_by_tag_name("a").click()
        time.sleep(1)

        row_data = []
        row_data.append(link_id)

        all_data = browser.find_element_by_id("description").text

        row_data.append(all_data)
        data.append(row_data)

    return data


def populate_review():
    data = []
    # row_data = []

    browser.find_element_by_id("tab_reviews").click()
    reviews = browser.find_element_by_id("reviews")

    # avg_rating = reviews.find_element_by_class_name("rating")
    # avg_rating = avg_rating.find_elements_by_xpath(".//*")
    #
    # rating = avg_rating[0].get_attribute("class")
    # rating = rating[1:-1]

    # row_data.append(rating)
    # data.append(row_data)

    customer_reviews = reviews.find_elements_by_class_name("customer-reviews")
    if customer_reviews:
        customer_reviews = customer_reviews[0].find_elements_by_class_name("comment")

        for customer_review in customer_reviews:
            placeholder = customer_review.find_element_by_class_name("text").find_element_by_class_name("commands")\
                .find_elements_by_tag_name("span")
            if placeholder:
                placeholder[-1].click()

        reviews = browser.find_element_by_id("reviews")
        customer_reviews = reviews.find_elements_by_class_name("customer-reviews")
        customer_reviews = customer_reviews[0].find_elements_by_class_name("comment")

        for customer_review in customer_reviews:
            placeholder = customer_review.find_element_by_class_name("text")
            row_data = []
            row_data.append(link_id)

            author = placeholder.find_elements_by_class_name("author")
            if author:
                row_data.append(author[0].text)
            else:
                row_data.append(" ")

            time = placeholder.find_elements_by_tag_name("meta")
            row_data.append(time[1].get_attribute("content"))

            rating = placeholder.find_elements_by_class_name("rating")

            if rating:
                rating = rating[0].find_elements_by_xpath(".//*")
                info = rating[0].get_attribute("class")
                row_data.append(info[1:-1])
            else:
                row_data.append("0")  # no rating is treated as a 0

            text = placeholder.find_element_by_class_name("content")
            row_data.append(text.text)

            data.append(row_data)

    return data


def populate_news():
    data = []
    news_tab = browser.find_elements_by_id("tab_news")

    if news_tab:
        news_tab[0].click()

        updates = browser.find_elements_by_class_name("signal_update")
        for update in updates:
            row_data = []
            timestamp = update.find_element_by_class_name("timestamp")
            row_data.append(timestamp.text)
            options = timestamp.find_elements_by_class_name("options")
            if options:
                options[0].find_element_by_class_name("command").click()
                row_data.append(update.find_element_by_class_name("content").text)
            else:
                row_data.append(update.find_element_by_class_name("text").text)
            data.append(row_data)

    return data


def write_csv(name, data):
    name = name + ".csv"

    dir2 = os.path.dirname(__file__) + "/" + name
    if os.path.isfile(dir2):
        if name == "description" or name == "review":
            outfile = open(name, "a", newline='')
        else:
            outfile = open(name, "a", newline='', encoding="UTF-8")
        del data[0]
    else:
        if name == "description" or name == "review":
            outfile = open(name, "w", newline='')
        else:
            outfile = open(name, "w", newline='', encoding="UTF-8")

    writer = csv.writer(outfile)
    writer.writerows(data)
    outfile.close()


def write_data(main, positions, history, symbols, slippage, description, review, news):
    data = ["URL", "Time", "Type", "Volume", "Symbol", "Price", "S/L", "T/P", "Price", "Commission", "Swap", "Profit"]
    positions.insert(0, data)
    write_csv("positions", positions)

    data = ["URL", "Time", "Type", "Volume", "Symbol", "Price", "S/L", "T/P", "Time", "Price", "Commission", "Swap",
            "Profit", "Comment"]
    history.insert(0, data)
    write_csv("history", history)

    data = ["URL", "Currency", "Deals", "Sell", "Buy"]
    symbols.insert(0, data)
    write_csv("symbols", symbols)

    data = ["URL", "Title", "Amount", "Amount2"]
    slippage.insert(0, data)
    write_csv("slippage", slippage)

    data = ["URL", "Description"]
    description.insert(0, data)
    write_csv("description", description)

    data = ["URL", "Name", "DateTime", "Rating", "Comment"]
    review.insert(0, data)
    write_csv("review", review)

    data = ["Timestamp", "Message"]
    news.insert(0, data)
    write_csv("whatsNew", news)

    # Stats start from Trades, Risks start from BestTrade
    data = ["URL", "SignalName", "Rating", "ReviewCount", "Cost", "Growth", "TooltipDesc", "AccCurrency",
            "InitialDeposit", "Deposits", "Withdrawals", "Balance", "Equity", "Profit", "ProfitToolTip", "Subscribers",
            "SubscribersFunds", "MaxDDPct", "MaxDDAmt", "Weeks", "LatestTrade", "TradesPerWeek", "AvgHoldingTime", "Broker", "BrokerName", "Leverage",
            "TradingMode", "Author", "AuthorCode", "EquityStDate", "Trades", "ProfitTradeNo", "ProfitTradePct",
            "LossTradesNo", "LossTradesPct", "BestTrade", "WorstTrade", "GrossProfitAmt", "GrossProfitPips",
            "GrossLossAmt", "GrossLossPips", "MaxConsecWinsNo", "MaxConsecWinsAmt",  "MaxConsecProfitAmt",
            "MaxConsecProfitNo", "SharpeRatio", "TradingActivity", "MaxDepositLoad", "RecoveryFactor", "LongTradesNo",
            "LongTradesPct", "ShortTradesNo", "ShortTradesPct", "ProfitFactor", "ExpectedPayoff", "AvgProfit",
            "AvgLoss", "MaxConsecLossesNo", "MaxConsecLossesAmt", "MaxConsecLossAmt", "MaxConsecLossNo",
            "Monthly Growth", "Annual Forecast", "Algo Trading", "BestTrade", "MaxConsWinsNo",
            "MaxConsWinsAmt", "MaxConsProfitAmt", "MaxConsProfitNo", "WorstTrade", "MaxConsLossesNo", "MaxConsLossesAmt",
            "MaxConsLossAmt", "MaxConsLossNo", "DDBalAbsolute", "DDBalMaxAmt", "DDBalMaxPct", "RDDBalAmt", "RDDBalPct",
            "RDDEquityAmt", "RDDEquityPct", "SymbolsCount"]
    main.insert(0, data)
    write_csv("mainData", main)

    # NOTE: CREATE "TEST" DB BEFORE RUNNING THIS
    # db = sql.init_db()

    # for dataInfo in positions:
    #    sql.execute_insertion(db, "positions", dataInfo)

    # db.close()


if __name__ == "__main__":

    # print("Reading Links...")
    links = read_links()

    # print("Logging in...")
    login()

    counter = 0

    for link_id in links:
        # print("Going to Link...")
        go_to_link(link_id)

        err_data = get_error(link_id)

        if err_data:
            data = ["URL", "Message"]
            err_data.insert(0, data)
            write_csv("warnings", err_data)

        else:
            # print("Gathering Position...")
            position_data = populate_positions()

            main_data = populate_main()

            # print("Gathering History...")
            history_data = populate_history(link_id, no_of_rows_to_read=1000)

            # print("Gathering Symbols...")
            symbols_data = populate_symbols()

            # print("Gathering Slippage...")
            slippage_data = populate_slippage()

            # print("Gathering Description...")
            description_data = populate_description()

            # print("Gathering Reviews...")
            review_data = populate_review()

            news_data = populate_news()

            # print("Writing all data...")
            write_data(main_data, position_data, history_data, symbols_data, slippage_data, description_data,
                       review_data, news_data)

        counter = counter + 1
        print(str(counter) + " DONE. %Complete: " + str(counter/len(links) * 100) + "%")
