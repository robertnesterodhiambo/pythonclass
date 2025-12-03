<?php
header("Content-Type: text/plain");

// Get days from URL: ?days=1,2,3
$days = isset($_GET['days']) ? $_GET['days'] : "1";

// Paths
$python = "C:\\Users\\Dragon\\AppData\\Local\\Programs\\Python\\Python311\\python.exe";
$script = "C:\\xampp\\htdocs\\python_scraper\\scrape.py";

// Set up descriptors so we can write to stdin and read stdout
$descriptorspec = array(
    0 => array("pipe", "r"),  // stdin
    1 => array("pipe", "w"),  // stdout
    2 => array("pipe", "w")   // stderr
);

// Start process
$process = proc_open("\"$python\" \"$script\"", $descriptorspec, $pipes);

if (is_resource($process)) {
    // Write days into the script's stdin (simulate user typing)
    fwrite($pipes[0], $days . "\n");
    fclose($pipes[0]);

    // Read output
    $output = stream_get_contents($pipes[1]);
    fclose($pipes[1]);

    // Read errors
    $errors = stream_get_contents($pipes[2]);
    fclose($pipes[2]);

    // Close process
    $return_value = proc_close($process);

    // Output everything
    echo $output;
    if ($errors) {
        echo "\n⚠️ Errors:\n$errors";
    }
} else {
    echo "❌ Failed to start Python process.";
}
?>
