<?php
// make sure browsers see this page as utf-8 encoded HTML
header('Content-Type: text/html; charset=utf-8');

$limit = 10;
$query = isset($_REQUEST['q']) ? $_REQUEST['q'] : false;
$results = false;

if ($query) {
	// The Apache Solr Client library should be on the include path
	// which is usually most easily accomplished by placing in the
	// same directory as this script ( . or current directory is a default
	// php include path entry in the php.ini)
	require_once('Apache/Solr/Service.php');

	// create a new solr service instance - host, port, and webapp
	// path (all defaults in this example)
	$solr = new Apache_Solr_Service('localhost', 8983, '/solr/myexample');

	// if magic quotes is enabled then stripslashes will be needed
	if (get_magic_quotes_gpc() == 1) {
		$query = stripslashes($query);
	}

	// in production code you'll always want to use a try /catch for any
	// possible exceptions emitted  by searchingexternal_pageRankFile (i.e. connection
	// problems or a query parsing error)
	try {

		if ($_GET['alorithm'] == "lucene") {

			$results = $solr->search($query, 0, $limit);

		} else {
			//assignment allows to use either ascending or descending
			$additionalParameters = array('sort' => 'pageRankFile desc');
			$results = $solr->search($query, 0, $limit, $additionalParameters);

		}

	} catch (Exception $e) {
		// in production you'd probably log or email this error to an admin
		// and then show a special message to the user but for this example
		// we're going to show the full exception
		die("<html><head><title>SEARCH EXCEPTION</title><body><pre>{$e->__toString()}</pre></body></html>");
	}
}

?>
<html>
<head>
	<title>USC: CSCI 572 HW 4&5</title>
</head>

<body>
	<form accept-charset="utf-8" method="get">
		<center>
			<h1><label for="q">CSCI572 SEARCH ENG (HW4&5)</label>
		</center>
		</h1>
		<center><input id="q" name="q" type="text" size="50" value="<?php echo htmlspecialchars($query, ENT_QUOTES, 'utf-8'); ?>" /></center>
		<br/>
		<center>Search Algorithms:</center>
		<br/>
		<center><input type="radio" name="alorithm" value="lucene" checked="checked"<?php if (isset($_REQUEST['alorithm']) && $_REQUEST['alorithm'] == 'lucene') {
														echo 'checked="checked"';
														} ?>> Lucene

						<input type="radio" name="alorithm" value="pagerank" <?php if (isset($_REQUEST['alorithm']) && $_REQUEST['alorithm'] == 'pagerank') {
													echo 'checked="checked"';
												} ?>> Page Rank

		</center>
		<br/>
		<center><input type="submit" value="Search"/></center>
	</form>
	<?php

	// display results
	if ($results) {
		$total = (int) $results->response->numFound;
		$start = min(1, $total);
		$end = min($limit, $total);
	?>
		<div>Display Results: <?php echo $start; ?> - <?php echo $end; ?> | Total Results Found: <?php echo $total; ?>:</div>
		<ol>
		<?php

		// iterate result documents
		//$URLtoHTMLcsvFile = array_map('str_getcsv', file('/Users/Ehsan/Desktop/solr-7.7.2/FOXNEWS/URLtoHTML_fox_news.csv'));
		$URLtoHTMLcsvFile = file('/Users/Ehsan/Desktop/solr-7.7.2/FOXNEWS/URLtoHTML_fox_news.csv');

		foreach ($results->response->docs as $doc) {
			//Fields to show
			$pageTitle = $doc->title;
			$url = $doc->og_url;
			$documentID = $doc->id;
			$descending = $doc->og_description;

			//condition check
			if ($pageTitle == null || $pageTitle == "") {
				 $pageTitle = "null";
			}

			if ($descending == null || $descending == "") {
				 $descending = "null";
			}

			if ($url == "" || $url == null) {

						$htmlDocID = explode("/", $documentID);
						$lastParthtmlDocID = $htmlDocID[count($htmlDocID) - 1]; //access the last item *.html
						$find_row = preg_grep("/^$lastParthtmlDocID/i", $URLtoHTMLcsvFile);

						//error_reporting(0); //debug
						//echo "lastParthtmlDocID: $lastParthtmlDocID</br>"; //debug
						//echo "URLtoHTMLcsvFile: $URLtoHTMLcsvFile[2905]</br>"; //debug

						foreach($find_row as $row_item){
                 //echo "item: ". $row_item . "</br>"; //debug
								 $item_url = explode(",", $row_item);
								 $url = $item_url[1]; //extract URL
            }
			 }
			 //display results
			 echo "<strong>Title:</strong> <a style='background-color:yellow;' href = '$url'>$pageTitle</a></br>";
			 echo "<strong>URL: </strong><a href='$url'>$url</a></br>";
			 echo "<strong>ID:</strong> $documentID</br>";
			 echo "<strong>Description:</strong> $descending </br></br>";
		}
	}
	?>
</body>
</html>
