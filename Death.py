# -*- coding: utf-8 -*-
import json
import pyspigot as ps
from org.bukkit.event.entity import PlayerDeathEvent
from org.bukkit.event import Listener
from java.net import URL
from java.net import HttpURLConnection
from java.io import OutputStreamWriter  # Corrected this import

WEBHOOK_URL = "put_your_webhook_here"

# Define the function that will handle the event
def on_player_death(event):
    if isinstance(event, PlayerDeathEvent):
        player = event.getEntity()  # Get the player who died
        if player is None:
            return  # If somehow the player is None, we do nothing

        # Get the death message and player's name
        death_message = event.getDeathMessage()
        player_name = player.getName()

        # Build the data to send to Discord
        embed = {
            "username": "Minecraft Death Logger",  # Set the bot's name
            "embeds": [{
                "title": "☠ Player Death",  # Embed title
                "description": "**{0}** died.\n```{1}```".format(player_name, death_message),  # Message description
                "color": 16711680  # Red color for death
            }]
        }

        # Send the data to the webhook
        send_to_discord(embed)

# Function to send data to the Discord webhook using Java's HttpURLConnection
def send_to_discord(data):
    """Send the provided data to the Discord webhook using HttpURLConnection."""
    try:
        # Create a URL object
        url = URL(WEBHOOK_URL)
        # Open a connection to the URL
        connection = url.openConnection()
        connection.setRequestMethod("POST")
        connection.setRequestProperty("Content-Type", "application/json")
        connection.setDoOutput(True)

        # Write the JSON data to the output stream
        output_stream = OutputStreamWriter(connection.getOutputStream())
        output_stream.write(json.dumps(data))
        output_stream.flush()
        output_stream.close()

        # Get the response code
        response_code = connection.getResponseCode()
        if response_code == 204:
            ps.logger.info("Death webhook sent successfully.")
        else:
            ps.logger.warning("Failed to send webhook. Status code: {0}".format(response_code))
        
        # Close the connection
        connection.disconnect()

    except Exception as e:
        ps.logger.warning("An error occurred while sending the webhook: {0}".format(str(e)))

# Register the event listener with PySpigot's listener manager
ps.listener.registerListener(on_player_death, PlayerDeathEvent)
