from app_crew import crew

if __name__ == "__main__":
    description = "A python function to calculate factorial."
    result = crew.kickoff(inputs={"requirements": description})
    print("==========Final Output:===========")
    print(result)