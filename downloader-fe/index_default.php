<?php
function isIPv6($ip)
{
	if (!filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6) === false) {
		return true;
	}
	return false;
}
function isMyCloudNAS()
{
	if (isset($_SERVER['HTTP_HOST']) && strlen($_SERVER['HTTP_HOST']) > 0)
		$_http_host = $_SERVER['HTTP_HOST'];
	else
		return false;
	$mycloudnas_domains = Array(
        'mycloudnas.com',
        'myqnapnas.com',
        'qcloudnas.com',
        'myqnapcloud.com'
	);
	foreach ($mycloudnas_domains as $d)
	{
		if (strncasecmp(stristr($_http_host,$d),$d,strlen($d))==0)
		{
			return true;
		}
	}
	return false;
}
	if(isMyCloudNAS() == true){
		$extPort = exec('/sbin/getcfg System ExtPort -d 0');
		if(intval($extPort)>0)
			$webAccessPort = $extPort;
		else
			$webAccessPort = exec('/sbin/getcfg System "Web Access Port" -d 8080');
	}
	else
		$webAccessPort = exec('/sbin/getcfg System "Web Access Port" -d 8080');
	$webAccessIP = $_SERVER['SERVER_NAME'];
	if($_SERVER['HTTPS'] && exec('/sbin/getcfg Stunnel Enable -d 1') == '1'){
		$protocol='https';
		$webAccessPort = exec('/sbin/getcfg Stunnel Port -d 443');
	}
	else
		$protocol='http';
	if(isIPv6($webAccessIP))
		$webAccessUrl = $protocol.'://['.$webAccessIP .']:'.$webAccessPort.'/';
	else
		$webAccessUrl = $protocol.'://'.$webAccessIP .':'.$webAccessPort.'/';
?> 
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
<meta http-equiv="expires" content="0">
<script type='text/javascript'>
	location.href = '<?=$webAccessUrl?>';
</script>
	</head>
</html>
