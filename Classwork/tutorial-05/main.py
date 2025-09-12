from crew import crew

# ------------------------
# Run workflow
# ------------------------
if __name__ == "__main__":
    result = crew.kickoff()
    print("=== Shipment Status ===")
    print(result)