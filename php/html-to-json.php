<?php

if ($argc < 3) {
  echo "Usage: {$argv[0]} <in.html> <out.json>" . PHP_EOL;
  exit(1);
}

$in_filename = $argv[1];
$out_filename = $argv[2];

$dom = new DOMDocument('1.0', 'UTF8');
libxml_use_internal_errors(true);
$rc = $dom->loadHTMLFile($in_filename);
libxml_clear_errors();
if (!$rc) {
  echo "Failed to load input file" . PHP_EOL;
  exit(1);
}

$out = fopen($out_filename, "w");
if (!$out) {
  echo "Failed to open output file" . PHP_EOL;
  exit(1);
}

$finder = new DomXPath($dom);
$classname = "im_history_messages_peer";
$nodes = $finder->query(".//*[contains(@class, '$classname')]");
$history = $nodes[0];

$skip_types = [ 'DOMText', 'DOMComment' ];

$node_num = 0;
$prev_date = '';
$date = '';

$days = [];

foreach ($history->childNodes as $message_node) {
  $node_num += 1;

  if (in_array(get_class($message_node), $skip_types)) {
    continue;
  }

  // $im_service_message_nodes = $finder->query(".//*[contains(@class, 'im_service_message_wrap')]", $message_node);
  // if ($im_service_message_nodes->length > 0) {
  //   continue;
  // }

  $text = null;
  $message_text_nodes = $finder->query(".//*[contains(@class, 'im_message_text')]", $message_node);
  if ($message_text_nodes->length > 0) {
    $message_text_node = $message_text_nodes[0];
    $text = clean($message_text_node->nodeValue);
  } else {
    echo "WARNING: No text detected in node #{$node_num}: " . clean($message_node->nodeValue) . PHP_EOL;
  }

  $author = null;
  $q = ".//*[contains(@class, 'im_message_author') and not(contains(@class, 'im_message_author_wrap'))]";
  $author_nodes = $finder->query($q, $message_node);
  if ($author_nodes->length > 0) {
    $author_node = $author_nodes[0];
    $author = clean($author_node->nodeValue);
    // var_dump($author);die();
  } else {
    echo "WARNING: No author detected in node #{$node_num}: " . clean($message_node->nodeValue) . PHP_EOL;
  }

  // $text = trim(preg_replace("~\n| {2,}~", ' ', trim($message_node->nodeValue)));
  $time = null;
  $time_text_nodes = $finder->query(".//*[contains(@ng-bind, 'historyMessage.date')]", $message_node);
  if ($time_text_nodes->length > 0) {
    $time_text_node = $time_text_nodes[0];
    $time = clean($time_text_node->nodeValue);
  } else {
    echo "WARNING: No time detected in node #{$node_num}: " . clean($message_node->nodeValue) . PHP_EOL;
  }

  $date_split = "";
  $date_nodes = $finder->query(".//*[contains(@class, 'im_message_date_split_text')]", $message_node);
  if ($date_nodes->length > 0) {
    $date_node = $date_nodes[0];
    $date_split = clean($date_node->nodeValue);
    if ($date_split !== $date) {
      $prev_date = $date;
      $date = $date_split;
    }
  }

  $datetime_int = strtotime($date . ' ' . $time);

  if (!is_null($text)) {
    if (strlen($date_split) > 0) {
      echo '-- ' . $date_split . ' --' . PHP_EOL;
    }

    echo date("c", $datetime_int) . " " . $author . ": " . $text . PHP_EOL;
  }

  $json = json_encode([ $datetime_int, $author, $text ], JSON_UNESCAPED_UNICODE);
  fwrite($out, "{$json}\n");
}

$dom->saveHTMLFile($in_filename . ".debug");

function clean($str) {
  return trim(preg_replace('~ {2,}~', ' ', str_replace("\n", '', $str)));
}


/*

12 -- 19 -- 23 --- 6 -- 12 -- 19 -- 23 -- 6
--------------<-0->----------------------

*/
