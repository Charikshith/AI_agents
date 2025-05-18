# =============================================================================
# agents/google_adk/__main__.py
# =============================================================================
# Purpose:
# This is the main script that starts your TellTimeAgent server.
# It:
# - Declares the agent’s capabilities and skills
# - Sets up the A2A server with a task manager and agent
# - Starts listening on a specified host and port
#
# This script can be run directly from the command line:
#     python -m agents.google_adk
# =============================================================================

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

# Your custom A2A server class
from server.server import A2AServer