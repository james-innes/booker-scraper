import json

# a Python object (dict):
x = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# convert into JSON:
j = json.dumps(x)

with open('test-pie.json', 'w', encoding='utf-8') as f:
    json.dump(j, f, ensure_ascii=False, indent=4)
