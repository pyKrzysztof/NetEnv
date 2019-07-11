printf $1
sshpass -f <(printf '%s\n' "$4") sftp -P "$2" "$3"@"$1":"$5"
mv "$5" "$6"