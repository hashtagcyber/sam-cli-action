#!/bin/bash

set -u

function parseInputs(){
	# Required inputs
	if [ "${INPUT_SAM_COMMAND}" == "" ]; then
		echo "Input sam_subcommand cannot be empty"
		exit 1
	fi
}

function runSam(){
	echo "Run sam ${INPUT_SAM_COMMAND}"
	output=$(sam ${INPUT_SAM_COMMAND} 2>&1)
	exitCode=${?}
	echo "${output}"

	commentStatus="Failed"
	if [ "${exitCode}" == "0" ]; then
		commentStatus="Success"
	fi

	if [ "$GITHUB_EVENT_NAME" == "pull_request" ] && [ "${INPUT_ACTIONS_COMMENT}" == "true" ]; then
		commentWrapper="#### \`sam ${INPUT_SAM_COMMAND}\` ${commentStatus}
<details><summary>Show Output</summary>

\`\`\`
${output}
\`\`\`

</details>

*Workflow: \`${GITHUB_WORKFLOW}\`, Action: \`${GITHUB_ACTION}\`*"

		payload=$(echo "${commentWrapper}" | jq -R --slurp '{body: .}')
		commentsURL=$(cat ${GITHUB_EVENT_PATH} | jq -r .pull_request.comments_url)

		echo "${payload}" | curl -s -S -H "Authorization: token ${GITHUB_TOKEN}" --header "Content-Type: application/json" --data @- "${commentsURL}" > /dev/null
	fi

	if [ "${exitCode}" == "1" ]; then
		exit 1
	fi
}

function gotoDirectory(){
	#if [ -z "${INPUT_DIRECTORY}" ]; then
	#	return 1
	#fi
#
#	if [ ! -d "${INPUT_DIRECTORY}" ]; then
#		echo "Directory ${INPUT_DIRECTORY} does not exists."
#		exit 127
#	fi
#
#	echo "cd ${INPUT_DIRECTORY}"
#	cd $INPUT_DIRECTORY
    # cat $GITHUB_EVENT_PATH
    cd $(python3 /find-package.py)
}

function main(){
	parseInputs
	gotoDirectory
	runSam
}

main
