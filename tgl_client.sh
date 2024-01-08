inputs="Which team won the NBA Championship the year when Lebron James was born?"
max_new_tokens=200

curl 127.0.0.1:8080/generate \
-X POST \
-H 'Content-Type: application/json' \
-d "{\"inputs\":\"$inputs\",\"parameters\":{\"max_new_tokens\":$max_new_tokens}}"