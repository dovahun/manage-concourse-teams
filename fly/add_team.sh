#!/usr/bin/env bash
TMP_TEAMS=/tmp/teams

fly  -t "$1" login -u "$2" -p "$3" --concourse-url="$4" -n "$5"
if [[ $? -ne 0 ]]
then
  exit 1
fi
for i in $(fly -t $1 teams)
do
  echo "$i" >> $TMP_TEAMS
done

# Добавь сюда проверку что файл переданный в аргументе существует.
# а еще лучше переделай на while read line

for i in $(cat $6)
do
 if grep -Fxq "$i" $TMP_TEAMS
 then
   # оставь
   echo "$i found"
 else
   # тут создавай тиму
   echo "
  roles:
  - name: owner
    local:
      users: ["admin"]
  - name: member
    local:
      users: ["admin"]
    ldap:
      groups:  ['$i']
  - name: viewer
    local:
      users: ["admin"]
    ldap:
      groups: ['concourse-users']" > teams.yml
   fly -t "$1" set-team -n $i -c teams.yml --non-interactive
   echo "$i is'nt found"
 fi
done

rm -f $TMP_TEAMS