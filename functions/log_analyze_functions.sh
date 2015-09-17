source /opt/scripts/BashLibrary/library/file_functions.sh
source /opt/scripts/BashLibrary/library/string_functions.sh
source /opt/scripts/BashLibrary/library/mail_functions.sh

EFFECTIVE_FILE="effectiveLogFile.txt"
REG_EXPRESSION="[0-2][0-9][:][0-6][0-9][:][0-6][0-9][,]"
ADMIN_MAIL_ID=sandeep.rawat@mettl.com


###########################################################################################################
#I will get the exception stack trailing after a particular exception till i find the REG_EXPRESSION and 
# will store the stacktrace of exception in EXCEPTION_TO_CHECK file
#
###########################################################################################################

function getExceptionStack() {
	local EXCEPTION_TO_CHECK=$1
	local EXCEPTION_LINE_NO=$2

	echo "Getting stacktrace of exception ${EXCEPTION_TO_CHECK} at line no ${EXCEPTION_LINE_NO}"
	END_LINE_IN_TEMP_FILE=$( numberOfLinesInFile $EFFECTIVE_FILE )
	EXCEPTION_LINE=$( getStringAtLineNo "${EXCEPTION_LINE_NO}" "${EFFECTIVE_FILE}" )
	echo "Now processing line ${EXCEPTION_LINE}" 

	while ( ! matchRegex "${EXCEPTION_LINE}" "${REG_EXPRESSION}" )  ; do
		echo "${EXCEPTION_LINE}" >> ${EXCEPTION_TO_CHECK}.txt
		EXCEPTION_LINE_NO=$((EXCEPTION_LINE_NO+1))
		EXCEPTION_LINE=$( (getStringAtLineNo "${EXCEPTION_LINE_NO}" "$EFFECTIVE_FILE" ) )
		if [ ${EXCEPTION_LINE_NO} -ge ${END_LINE_IN_TEMP_FILE} ] ; then
			break
		fi
#		echo "Now processing line ${EXCEPTION_LINE}" 
	done
	return ${EXCEPTION_LINE_NO}
}

###################################################################################################################
# I'll analyze a log file(LOG_FILE) for the provided exception(EXCEPTION_TO_CHECK) between
# line no(STARTING_LINE_NO, END_LINE_NO) & I'll place all the stacktrace of that exception in a file name by that
# exception only
#
#
###################################################################################################################
function funcLogAnalyzer() {
        local LOG_FILE=$1
        local EXCEPTION_TO_CHECK=$2
        local START_LINE_NO=$3
	local END_LINE_NO=$( ( numberOfLinesInFile ${LOG_FILE} ) )

  	initializFile "${EXCEPTION_TO_CHECK}.txt"
        initializFile "${EFFECTIVE_FILE}"
    
        DIFF=$((END_LINE_NO - START_LINE_NO))
        tail -n "$DIFF" "$LOG_FILE" >> $EFFECTIVE_FILE

        END_LINE_IN_TEMP_FILE=$( ( numberOfLinesInFile ${EFFECTIVE_FILE} ) )
        echo "File is being processed for exception ${EXCEPTION_TO_CHECK} from line no ${START_LINE_NO} to ${END_LINE_NO} please wait ..."
	EXCEPTION_LINE_NOS=$( getLineNoMatchingRegex "$EFFECTIVE_FILE"  $EXCEPTION_TO_CHECK )
	for LINE_NO in ${EXCEPTION_LINE_NOS}
	do
		READ_LINE_STRING=$( (getStringAtLineNo "$LINE_NO" "$EFFECTIVE_FILE" ) )
		echo "$READ_LINE_STRING"  >> $EXCEPTION_TO_CHECK.txt
		LINE_NO= getExceptionStack "$EXCEPTION_TO_CHECK" $LINE_NO
		LINE_NO=$((LINE_NO+1))
               	    if [ $LINE_NO -ge $END_LINE_IN_TEMP_FILE ] ;then
                            break
              	     fi
	done
}


############################################################################################################################################
# I'll parse the log file for exceptions mentioned in exception file having format(exception=recipient mail id)
#
#
#
#
############################################################################################################################################
function parseLogFileForExceptions() {
	local FILE_TO_ANALYSE=$1
	local START_LINE_NO=$2
	local EXCEPTIONS_FILE=$3
	local ENVIRONMENT=$4

	while read EXCEPTION_LINE ; do
		EXCEPTION=$( getWordAtPosition "${EXCEPTION_LINE}" 1 '=' )
		EXCEPTION_RECIPIENT=$( getWordAtPosition "${EXCEPTION_LINE}" 2 '=' )

		funcLogAnalyzer ${FILE_TO_ANALYSE} ${EXCEPTION} ${START_LINE_NO}

		EXCEPTION_FILE_SIZE=$( numberOfLinesInFile  ${EXCEPTION}.txt)
		if [ ${EXCEPTION_FILE_SIZE} -gt 20 ]; then
			sendMailForFile ${EXCEPTION_RECIPIENT} "Exception stack trace for ${EXCEPTION} in file ${FILE_TO_ANALYSE} on environment ${ENVIRONMENT}" ${ADMIN_MAIL_ID} ${EXCEPTION}.txt
		else
			echo "No need to send mail for exception ${EXCEPTION}" 
		fi
	done < ${EXCEPTIONS_FILE}
}

