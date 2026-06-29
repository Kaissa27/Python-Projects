import asyncio
import json

HOST = "127.0.0.1"
PORT = 5555

# Global server-side state repository tracking player coordinates
game_state = {}
connected_clients = set()

async def handle_client_connection(reader, writer):
    """Manages an isolated network data socket for an active player connection."""
    client_address = writer.get_extra_info('peername')
    player_id = f"Player_{client_address[1]}"
    print(f"🔌 New client connected: {player_id}")
    
    # Initialize player coordinate space inside the master state matrix
    game_state[player_id] = {"x": 100, "y": 100, "color": player_id[-4:]}
    connected_clients.add(writer)

    try:
        while True:
            # Read incoming byte packets from this specific client network line
            data = await reader.read(1024)
            if not data:
                break
                
            # Deserialize the input command payload
            command = json.loads(data.decode('utf-8'))
            
            # AUTHORITATIVE VALUE UPDATE: Server handles state changes
            if command.get("type") == "move":
                game_state[player_id]["x"] += command["dx"]
                game_state[player_id]["y"] += command["dy"]

            # BROADCAST PHASE: Stream updated world state back to ALL connected players
            serialized_state = json.dumps(game_state).encode('utf-8')
            for client_writer in list(connected_clients):
                try:
                    client_writer.write(serialized_state + b"\n")
                    await client_writer.drain()
                except Exception:
                    connected_clients.remove(client_writer)

    except Exception as e:
        print(f"⚠️ Connection anomaly on {player_id}: {e}")
    finally:
        print(f"🛑 Disconnecting player: {player_id}")
        connected_clients.remove(writer)
        if player_id in game_state:
            del game_state[player_id]
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client_connection, HOST, PORT)
    print(f"🚀 Authoritative Game Server actively listening on {HOST}:{PORT}...")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
