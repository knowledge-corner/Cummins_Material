from app_crew import crew

if __name__ == "__main__":
    description = "A python function to calculate factorial."
    result = crew.kickoff(inputs={"requirements": description})
    print("==========Final Output:===========")
    print(result.tasks_output)



# Task - Create an Agent which will test the code generated and store the
# result of 5 test cases in a file named as test_results.txt.