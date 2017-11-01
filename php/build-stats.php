<?php

if ($argc < 2) {
  echo "Usage: {$argv[0]} <in.json>" . PHP_EOL;
  exit(1);
}

$in_filename = $argv[1];
$in = fopen($in_filename, "r");

if ($in === false) {
  echo "Could not open input filename" . PHP_EOL;
  exit(1);
}

$line_num = 0;
$days_stats = [];

$morning_starts_at = 6;
$day_starts_at = 12;
$evening_starts_at = 21;
$night_starts_at = 23;

$time_shift = $morning_starts_at;

$morning_starts_at -= $time_shift;
$day_starts_at     -= $time_shift;
$evening_starts_at -= $time_shift;
$night_starts_at   -= $time_shift;

if ($morning_starts_at <= 0) $morning_starts_at += 24;
if ($day_starts_at <= 0) $day_starts_at += 24;
if ($evening_starts_at <= 0) $mevening_starts_at += 24;
if ($night_starts_at <= 0) $night_starts_at += 24;

$skip_authors = [ 'Бот-менеджер' ];

$empty_stats = [
  "morning" => 0,
  "day" => 0,
  "evening" => 0,
  "night" => 0
];

while (($raw_data = fgets($in)) !== false) {
  $line_num += 1;

  $data = json_decode($raw_data);
  if ($data === null) {
    echo "Failed to decode line #{$line_num}: '" . print_r($raw_data) . "'" . PHP_EOL;
    exit(1);
  }

  list($id, $datetime, $author_id, $author, $text) = $data;
  $datetime = strtotime($datetime);

  $shifted_datetime = strtotime("-{$time_shift} hour", $datetime);
  $date_parts = getdate($shifted_datetime);
  $daytime = "morning";
  if ($date_parts["hours"] >= $night_starts_at) {
    $daytime = "night";
  } elseif ($date_parts["hours"] >= $evening_starts_at) {
    $daytime = "evening";
  } elseif ($date_parts["hours"] >= $day_starts_at) {
    $daytime = "day";
  }
  $shifted_date = strtotime(date("Y-m-d", $shifted_datetime) . " 00:00:00");
  if (!array_key_exists($shifted_date, $days_stats)) {
    end($days_stats);
    $last_day = count($days_stats) > 0 ? key($days_stats) : strtotime("-1 day", $shifted_date);
    $day = strtotime("+1 day", $last_day);
    while ($day <= $shifted_date) {
      $days_stats[$day] = $empty_stats;
      $day = strtotime("+1 day", $day);
    }
  }

  if (!in_array($author, $skip_authors) && !is_null($text)) {
    $days_stats[$shifted_date][$daytime] += 1;
  }
}

if (!feof($in)) {
  echo "Failed to read line #{$line_num}" . PHP_EOL;
  exit(1);
}

fclose($in);

$prev_day = 0;
echo "Date,Morning,Day,Evening,Night" . PHP_EOL;
foreach ($days_stats as $day => $day_stats) {
  // $day_str = date("l, F j", $day);
  $day_str = date("Y-m-d", $day);
  // echo sprintf("%30s %4d %4d %4d %4d\n",
  echo sprintf("%s,%d,%d,%d,%d\n",
    $day_str,
    $day_stats["morning"],
    $day_stats["day"],
    $day_stats["evening"],
    $day_stats["night"]
  );
  if (date("w", $day) === "0") {
    // echo "--" . PHP_EOL;
  }
  $prev_day = $day;
}
