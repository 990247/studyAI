import os
import json
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            with open("index.html", "rb") as f:
                page = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(page)
    def do_POST(self):
        if self.path == "/ask":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            question = data.get("question", "")

            token = os.environ.get("HF_TOKEN")

            payload = {
                "model": "openai/gpt-oss-120b:fastest",
                "stream": False,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are StudyAI, a friendly student tutor. Explain answers clearly and simply."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }

            headers = {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json"
            }

            req = urllib.request.Request(
                "https://router.huggingface.co/v1/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )

            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode("utf-8"))

                answer = result["choices"][0]["message"]["content"]

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"answer": answer}).encode("utf-8")
                )

            except Exception as e:
                print("ERROR:", e)
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"answer": "Sorry, StudyAI could not answer right now."}).encode("utf-8")
                )
        if self.path == "/ask":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            question = data.get("question", "")

            token = os.environ.get("HF_TOKEN")

            payload = {
                "model": "openai/gpt-oss-120b:fastest",
                "stream": False,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are StudyAI, a helpful homework assistant. Explain answers clearly and simply for students."
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "StudyAI/1.0"
            }

            req = urllib.request.Request(
                "https://router.huggingface.co/v1/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )

            try:
                with urllib.request.urlopen(req) as response:
                    result = json.loads(response.read().decode("utf-8"))

                answer = result["choices"][0]["message"]["content"]

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"answer": answer}).encode("utf-8")
                )

            except Exception as e:
                print("ERROR:", e)
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"error": str(e)}).encode("utf-8")
                )

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("StudyAI server running on port 8000...")
    server.serve_forever()
