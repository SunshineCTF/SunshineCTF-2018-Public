<?php
function get_ip() {

  //Just get the headers if we can or else use the SERVER global.
  if ( function_exists( 'apache_request_headers' ) ) {

    $headers = apache_request_headers();

  } else {

    $headers = $_SERVER;

  }

  //Get the forwarded IP if it exists.
  if ( array_key_exists( 'X-Forwarded-For', $headers ) && filter_var( $headers['X-Forwarded-For'], FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 ) ) {

    $the_ip = $headers['X-Forwarded-For'];

  } elseif ( array_key_exists( 'HTTP_X_FORWARDED_FOR', $headers ) && filter_var( $headers['HTTP_X_FORWARDED_FOR'], FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 ) ) {

    $the_ip = $headers['HTTP_X_FORWARDED_FOR'];

  } else {
      
    $the_ip = filter_var( $_SERVER['REMOTE_ADDR'], FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 );

  }

  return $the_ip;

}

$ip = get_ip();

echo($ip);

if ($ip == "127.0.0.1") {
	echo("Here's your flag: sun{Th3rEs_n0_pl4cE_l1kE_127.0.0.1}");
} else {
	echo("This IP address is not authorized");
}
?>