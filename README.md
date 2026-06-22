1# divik box – FOH (Full On Haunting) 👻
2
3A savage, streaming anti-leak proxy built for devs who want to blockade secrets and sensitive data at the network edge—no chill and no leaks slip through.
4
5## Features
6
7- **Full On Haunting**: Blocks forbidden patterns in real time, even across packet/chunk boundaries.
8- **Streaming-safe**: No secrets get out, not before, during, or after a chunk boundary.
9- **Zero Leaks, No Mercy**: Hit a forbidden phrase? The stream stops. Client gets a violation message.
10- **Async & Modern**: FastAPI-based, async-native. Ready for prod stress and chaos.
11
12## Quickstart (Demo)
13
14```python
15from divikbox_demo import divik_box_demo
16
17divik_box_demo("This is safe LLM output.")              # All streams
18divik_box_demo("Hey, my SECRETKEY is right here!")      # BLOCKED, instantly
API Usage
Start server:
uvicorn divikbox_app:app --reload 2. POST /proxy with JSON: { "prompt": "put any data here" } 3. If the text contains forbidden stuff, you’ll get [BLOCKED — SENSITIVE DATA LEAK FLAGGED]
No apologies, no leaks. FOH.
 

