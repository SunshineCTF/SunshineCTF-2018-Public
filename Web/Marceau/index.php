<?php
// sun{45k_4nd_y3_5h411_r3c31v3} (nice work!)

// */* won't work here- you'll have to be more assertive.
if(strpos($_SERVER['HTTP_ACCEPT'], "text/php") === false)
  echo "<marquee><h3>You specifically want my PHP source. Why did you accept anything else?</h3></marquee>";
else
  show_source(__FILE__);
?>

