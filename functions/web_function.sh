function page_available() {
	WEB_PAGE_URL=$1
	RETRY_COUNT=$2
	WAIT_INTERVAL=$3
	if [ "$RETRY_COUNT" == "" ]; then
		echo "Retry count not provided, setting default value of 5"
		RETRY_COUNT=5
	fi
	if [ "$WAIT_INTERVAL" == "" ]; then
		echo "Wait interval not provided, setting default value of 10s"
		WAIT_INTERVAL=10
	fi
	PAGE_AVAILABLE=1

	for ((iteration_count = 1; iteration_count <= ${RETRY_COUNT}; iteration_count++)); do
		echo "Trying ${iteration_count} time"
		curl -s --head ${WEB_PAGE_URL} | head -n 1 | grep "HTTP/1.[01] [23].."
		if [ "$?" == "0" ]; then
			echo "Page found"
			PAGE_AVAILABLE=0
			break
		fi
		sleep ${WAIT_INTERVAL}
	done
	return ${PAGE_AVAILABLE}
}

function curl_url_available() {
        CURL_URL=$1
        BINARY_DATA_PARAMETER=$2

        echo "Verifying curl url is available or not"
        echo "curl -v -HContent-Type:application/json -X POST --data-binary $BINARY_DATA_PARAMETER ${CURL_URL}"
        curl -v -HContent-Type:application/json -X POST --data-binary ${BINARY_DATA_PARAMETER} ${CURL_URL} > curl.out
        PAGE_AVAILABLE=1
        cat curl.out | grep successful\":true
        if [ "$?" == "0" ]; then
                        echo "CURL Successfull"
                        PAGE_AVAILABLE=0
        fi

        return $PAGE_AVAILABLE
}


function sendEmail() {
        SUBJECT=$1
        EMAIL_ID=$2
        BODY=$3
        echo "Sending mail to User $EMAIL_ID"
        echo $BODY > mail.body
        mail -s "${SUBJECT} "  "${EMAIL_ID}" < mail.body
}


