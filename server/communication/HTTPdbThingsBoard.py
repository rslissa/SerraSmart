from requests import post, get

HOST_NAME = "http://localhost:9090"
token = "8ZwQiDFtXDFZ2VxU39pq"

item = {"humidity": 80}
#r = post(f"{HOST_NAME}/api/v1/8ZwQiDFtXDFZ2VxU39pq/telemetry", json=item)
#print(r.text, r.status_code)

r = get(f"{HOST_NAME}/api/v1/8ZwQiDFtXDFZ2VxU39pq/telemetry")
print(r.text, r.status_code)
