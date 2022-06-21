PHP version:
$ php -version
WARNING: PHP is not recommended
PHP is included in macOS for compatibility with legacy software.
Future versions of macOS will not include PHP.
PHP 7.3.24-(to be removed in future macOS) (cli) (built: Jun 17 2021 21:41:15) ( NTS )
Copyright (c) 1997-2018 The PHP Group
Zend Engine v3.3.24, Copyright (c) 1998-2018 Zend Technologies

Instructions to run:

Modify these lines on index.php
a) $solr = new Apache_Solr_Service('localhost', 8983, '/solr/myexample');
b) $URLtoHTMLcsvFile = file('/Users/Ehsan/Desktop/solr-7.7.2/FOXNEWS/URLtoHTML_fox_news.csv');


The index.php is the main file where UI is generated to get and display search results, and it should be placed inside /solr-php-client.

The core name used is 'myexample' and sold version used is solr-7.7.2.

I was assigned to FoxNews crawled data.

1) $ cd /solr-php-client 
2) $ php -S localhost:9000
3) open http://localhost:9000/ or http://localhost:9000/?q=

If there is any additional question please let me know.

Note: 

Based on one of the TAs response on https://piazza.com/class/ksgrko63l4c34a?cid=321, I am only submitting php code.  




