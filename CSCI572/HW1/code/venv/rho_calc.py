import csv
import json

#http://www.sparknotes.com/film/schindlerslist/symbolS/ -> sparknotes.com/film/schindlerslist/symbols
def urltrim(link):
    return link.lower().rstrip(" /").replace("www.", "").replace("https://", "").replace("http://", "")

total_overlap, total_overlap_percent, total_rho = 0, 0, 0
queries = []
query_stats = []

with open("100QueriesSet3.txt", "r") as f:
    for ask_query in f:
        queries.append(ask_query.strip("? \n"))

with open("Google_Result3.json", "r") as file:
    google_search_results = json.load(file)

with open("hw1.json", "r") as file:
    ask_search_results = json.load(file)

#print("queries:", queries)
#print("len(queries):", len(queries))
#print("google_search_results:", google_search_results)
#print("ask_search_results:", ask_search_results)

for index, query in enumerate(queries):
    ask_query_links = ask_search_results[query]
    google_query_links = google_search_results[query]

    print("index:", index)
    print("query:", query)
    print("ask_query_links:", ask_query_links)
    print("google_query_links:", google_query_links)
    print("len ask_query_links:", len(ask_query_links))
    print("len google_query_links:", len(google_query_links))

    ask_query_links_map = {}
    for rank, val in enumerate(ask_query_links):
        val = urltrim(val)
        ask_query_links_map[val] = rank

    print("modified ask_query_links_map:", ask_query_links_map, "\n")

    overlaps, sum = 0, 0
    overlap_same_rank = False
    for google_rank, google_val in enumerate(google_query_links):
        google_val = urltrim(google_val)

        if google_val in ask_query_links_map:
            overlaps += 1
            sum += ((google_rank - ask_query_links_map[google_val]) ** 2) ## ** --> pwr 2, get ask rank: ask_query_links_map[google_val]
            print("matched:", True)
            print("Google trimed URL:", google_val)
            print("google_rank:", google_rank)
            print("ask_rank:", ask_query_links_map[google_val])
            print("ask_query_links_map:", ask_query_links_map)
            if google_rank == ask_query_links_map[google_val]:
                overlap_same_rank = True
                print("Rank match ...")
            else:
                overlap_same_rank = False

    print("\nnum overlaps:", overlaps)
    print("sum:", sum)

    rho = 0
    if overlaps == 0:
        rho = 0
    elif overlaps == 1:
        if overlap_same_rank == True:
            rho = 1
        else:
            rho = 0
    else:
        print("rho calc ...")
        rho = 1 - ((6 * sum) / (overlaps * (overlaps ** 2 - 1)))

    print("rho:", rho)

    query_stats.append(["Query " + str(index + 1), " " + str(overlaps), " " + str((overlaps / len(google_query_links))*100), " " + str(rho)])
    total_overlap += overlaps
    total_overlap_percent += (overlaps / len(google_query_links))*100
    total_rho += rho

    print("------------------------------")

with open("hw1.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Queries", " Number of Overlapping Results", " Percent Overlap", " Spearman Coefficient"])
    writer.writerows(query_stats)
    writer.writerow(["Averages", " " + str(total_overlap / len(queries)), " " + str(total_overlap_percent / len(queries)), " " + str(round(total_rho / len(queries), 2))])

#main_results -> ask_query_links
#main_links -> given query links
#ref_results -> google