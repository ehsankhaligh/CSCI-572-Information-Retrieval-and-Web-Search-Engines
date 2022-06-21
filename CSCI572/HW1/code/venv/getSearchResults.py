from bs4 import BeautifulSoup #https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import time
import json
import csv
import requests
from random import randint
from html.parser import HTMLParser #https://docs.python.org/3/library/html.parser.html

#spider or crawler -> a program that systematically browses the World Wide Web in order to create an index of data

USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

class SearchEngine:
    @staticmethod
    def search(query, sleep=True):
        if sleep:  # Prevents loading too many pages too soon
            rand_sleep = randint(2, 5)
            print("1. sleep start ...")
            print("sleep rand time:", rand_sleep)
            time.sleep(rand_sleep)
            print("2. sleep end")
            print("passed func query:", query)

        temp_url = '+'.join(query.split())  # for adding + between words for the query -> hi+my+name+is...
        url = 'http://www.ask.com/web?q=' + temp_url + "&page=1"

        print("3. search key:", temp_url)
        print("search ask URL:", url)

        soup = BeautifulSoup(requests.get(url, headers=USER_AGENT).text, "html.parser")
        print("4. retrieved HTML ...")
#        print(soup.prettify())

        new_results = SearchEngine.scrape_search_result(soup)

        return new_results

    @staticmethod
    def scrape_search_result(soup):
        raw_results = soup.find_all("div", attrs = {"class" : "PartialSearchResults-item-title"})  # ["div", attrs = {"class" : "PartialSearchResults-item-title"}]
        results = []
        count = 0

        print("4. raw raw_results ...")

        # implement a check to get only 10 results and also check that URLs must not be duplicated
        for result in raw_results:
            link = result.find('a').get('href')
            print("count:", count)
#            print("for loop result:", result)
            print("link:", link)

            if count < 10:
                if link not in results:
                    results.append(link)
                    count = count + 1
                    print("Query appended to results list and count incremented ...")
#            print("results:", results)
        return results

if __name__ == "__main__":

    queries = []
    with open("100QueriesSet3.txt", "r") as f:
        for ask_query in f:
            queries.append(ask_query.strip("? \n"))
#    print("queries:", queries)
#    print("len(queries):", len(queries))

    ask_search_results = {}
    for count, query in enumerate(queries):
        print("count:", count)
        print("query:", query)
        ask_search_results[query] = SearchEngine.search(query, True)
        print("len(ask_search_results[query])", len(ask_search_results[query]))
        print("ask_search_results[query]:", ask_search_results[query])
        print("--------------------------")
#        time.sleep(1000000)

    print(ask_search_results)

    with open("hw1.json", "w") as f:
        json.dump(ask_search_results, f, indent=4)