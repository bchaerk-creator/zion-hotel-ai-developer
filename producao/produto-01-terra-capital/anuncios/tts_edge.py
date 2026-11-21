import asyncio, os, ssl, sys, aiohttp, edge_tts
async def go(text, out, voice="pt-BR-AntonioNeural", rate="+0%"):
    ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
    conn = aiohttp.TCPConnector(ssl=ctx)
    c = edge_tts.Communicate(text, voice, rate=rate, proxy=os.environ.get("HTTPS_PROXY"), connector=conn)
    await c.save(out)
asyncio.run(go(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv)>3 else "pt-BR-AntonioNeural"))
