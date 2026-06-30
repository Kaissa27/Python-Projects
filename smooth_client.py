import pygame
import json
import sys

pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lag-Compensated Network Client")
clock = pygame.time.Clock()

class SmoothLocalPlayer:
    """Handles predictive coordinate transformations before server verification."""
    def __init__(self):
        self.x = 100
        self.y = 100
        self.speed = 4

    def predict_movement(self, keys):
        """CLIENT-SIDE PREDICTION: Instantly shift coordinates based on user input."""
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:  dx = -self.speed
        if keys[pygame.K_RIGHT]: dx = self.speed
        if keys[pygame.K_UP]:    dy = -self.speed
        if keys[pygame.K_DOWN]:  dy = self.speed
        
        self.x += dx
        self.y += dy
        return dx, dy

    def reconcile_with_server(self, server_x: float, server_y: float):
        """SERVER RECONCILIATION: Softly snap local position if client drifts too far."""
        # If the client's predicted position drifts wildly from the server's truth,
        # we forcefully override it to prevent cheating or desync.
        distance = ((self.x - server_x)**2 + (self.y - server_y)**2)**0.5
        if distance > 20: # Threshold radius error
            self.x = server_x
            self.y = server_y

class RemotePlayerProxy:
    """Manages external network entities using Linear Interpolation."""
    def __init__(self, start_x, start_y):
        self.current_x = start_x
        self.current_y = start_y
        self.target_x = start_x
        self.target_y = start_y

    def set_new_target(self, tx, ty):
        self.target_x = tx
        self.target_y = ty

    def interpolate_step(self, lerp_factor=0.15):
        """LINEAR INTERPOLATION (LERP): Smoothly glide from current position to target position."""
        # Formula: Position = Position + (Target - Position) * Factor
        self.current_x += (self.target_x - self.current_x) * lerp_factor
        self.current_y += (self.target_y - self.current_y) * lerp_factor


# =====================================================================
# SYSTEM LOOP DECONSTRUCTION
# =====================================================================
def run_engine():
    local_player = SmoothLocalPlayer()
    remote_players = {} # Dictionary mapping player_id strings to RemotePlayerProxy instances
    
    # Mock representation of an incoming network data packet from our server
    # In a real environment, this payload arrives asynchronously via our socket thread
    mock_incoming_network_packet = {
        "Player_99": {"x": 300, "y": 200},
        "Player_Self": {"x": 104, "y": 100} # The server's view of where we are
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((24, 28, 36))

        # 1. PROCESS LOCAL INPUT & PREDICT
        keys = pygame.key.get_pressed()
        dx, dy = local_player.predict_movement(keys)
        
        # 2. SIMULATE INCOMING NETWORK DATA INTERPOLATION
        # Say player 99 suddenly changes position on the server:
        if pygame.time.get_ticks() % 2000 < 20: # Every 2 seconds, simulate network hop
            mock_incoming_network_packet["Player_99"]["x"] = float(pygame.time.get_ticks() % WIDTH)

        # Process external network objects
        for p_id, p_data in mock_incoming_network_packet.items():
            if p_id == "Player_Self":
                # Ensure our predictive track hasn't drifted out of boundary bounds
                local_player.reconcile_with_server(p_data["x"], p_data["y"])
            else:
                # If it's a remote player, track them via a proxy instance
                if p_id not in remote_players:
                    remote_players[p_id] = RemotePlayerProxy(p_data["x"], p_data["y"])
                
                # Update the target destination vector
                remote_players[p_id].set_new_target(p_data["x"], p_data["y"])

        # 3. COMPUTE LERP STEPS FOR ALL EXTERNAL PLAYERS
        for proxy in remote_players.values():
            proxy.interpolate_step(lerp_factor=0.1) # Smoothly glide 10% closer to target each frame

        # 4. RENDER GRAPHICS
        # Draw our predicted local player (Green)
        pygame.draw.rect(screen, (46, 204, 113), (local_player.x, local_player.y, 25, 25))
        
        # Draw interpolated remote players (Purple)
        for proxy in remote_players.values():
            pygame.draw.rect(screen, (155, 89, 182), (int(proxy.current_x), int(proxy.current_y), 25, 25))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_engine()
