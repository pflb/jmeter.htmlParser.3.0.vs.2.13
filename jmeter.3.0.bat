SET testfile="jmeter.testfile.jmx"

SET jmeter="D:\tools\jmeter.3.0\bin\jmeter" --testfile %testfile% ^
	--nongui ^
	--jmeterproperty URL=%1 ^
	--jmeterproperty loopCount=%2 ^
	--jmeterproperty siteKey=%3 ^
	-Jsample_variables=siteKey,htmlParser,jmeter.version,i ^
	-Dfile.encoding=UTF-8

CALL %jmeter% --jmeterproperty htmlParser.className=org.apache.jmeter.protocol.http.parser.LagartoBasedHtmlParser 	--jmeterlogfile jmeterLogs\jmeter.3.0.LagartoBasedHtmlParser.%3.log
CALL %jmeter% --jmeterproperty htmlParser.className=org.apache.jmeter.protocol.http.parser.JTidyHTMLParser          --jmeterlogfile jmeterLogs\jmeter.3.0.JTidyHTMLParser.%3.log
CALL %jmeter% --jmeterproperty htmlParser.className=org.apache.jmeter.protocol.http.parser.RegexpHTMLParser         --jmeterlogfile jmeterLogs\jmeter.3.0.RegexpHTMLParser.%3.log
CALL %jmeter% --jmeterproperty htmlParser.className=org.apache.jmeter.protocol.http.parser.JsoupBasedHtmlParser     --jmeterlogfile jmeterLogs\jmeter.3.0.JsoupBasedHtmlParser.%3.log