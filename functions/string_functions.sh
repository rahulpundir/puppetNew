function firstWordOfLine() {
	line="$1"
	echo "$line" | awk '{print $1}'
}

function initializFile(){
    FILE_NAME=$1
    :>$FILE_NAME
}

function getStringAtLineNo(){
    local LINE_NO=$1
    local FILE=$2
    LINE_STRING=$( ( sed -n "${LINE_NO}"p "${FILE}" ) )
    echo "$LINE_STRING"
}

function getLineNosForString() {
        local FILE=$1
        local STRING_TO_CHECK=$2
        local STARTING_LINE_NO=$3
        local END_LINE_NO=$4
	grep -n -i "$STRING_TO_CHECK" $FILE | cut -f1 -d: 
}

function containsString() {
	local STRING=$1
	local CHAR_SEQUENCE=$2

	if [[ ${STRING} =~ .*${CHAR_SEQUENCE}.* ]]
	then
		return 1
	else
		return 0
	fi
}

function matchRegex() {
	local STRING=$1
	local REGEX=$2

	if [[ ${STRING} =~ ${REGEX} ]]
	then
#		echo "Matched for ${STRING}"
		return 0
	else
#		echo "Didn't matched ${REGEX} for ${STRING}"
		return 1
	fi
}
