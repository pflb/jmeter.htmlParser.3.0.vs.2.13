SET testfile="jmeter.testfile.jmx"

SET jmeter="D:\tools\jmeter.2.13\bin\jmeter" --testfile %testfile% ^
	--nongui ^
	--jmeterproperty URL=%1 ^
	--jmeterproperty loopCount=%2 ^
	--jmeterproperty siteKey=%3 ^
	-Jsample_variables=siteKey,htmlParser,jmeterVersion,i ^
	-Dfile.encoding=UTF-8

CALL %jmeter% --jmeterproperty htmlParser.className=org.apache.jmeter.protocol.http.parser.LagartoBasedHtmlParser  --jmeterlogfile jmeterLogs\jmeter.2.13.LagartoBasedHtmlParser.%3.log
CALL %jmeter% --jmeterproperty htmlParser.className=org.apache.jmeter.protocol.http.parser.HtmlParserHTMLParser    --jmeterlogfile jmeterLogs\jmeter.2.13.HtmlParserHTMLParser.%3.log
CALL %jmeter% --jmeterproperty htmlParser.className=org.apache.jmeter.protocol.http.parser.JTidyHTMLParser         --jmeterlogfile jmeterLogs\jmeter.2.13.JTidyHTMLParser.%3.log
CALL %jmeter% --jmeterproperty htmlParser.className=org.apache.jmeter.protocol.http.parser.RegexpHTMLParser        --jmeterlogfile jmeterLogs\jmeter.2.13.RegexpHTMLParser.%3.log
CALL %jmeter% --jmeterproperty htmlParser.className=org.apache.jmeter.protocol.http.parser.JsoupBasedHtmlParser    --jmeterlogfile jmeterLogs\jmeter.2.13.JsoupBasedHtmlParser.%3.log