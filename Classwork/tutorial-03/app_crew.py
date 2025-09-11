from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

# Define LLM object
llm = LLM(
    model= os.getenv("MODEL"), 
    api_key=os.getenv("API_KEY")
)

# Define Agent objects
coder = Agent(
    name="Coder",
    role= "Senior Python Developer",
    goal= "Understand the requirements mentioned in {requirements} and implement using python code.",
    backstory="A expert 15 year experienced software developer who writes code in python.",
    llm=llm)

tester = Agent(
    name="Tester",  
    role= "Software Tester",
    goal= "Test the code implemented by coder agent",
    backstory="A expert 10 year experienced software tester who writes test cases in python.",
    llm=llm)

# Define Task objects
coding_task = Task(
    name="Coding Task",
    description="Write a structured python code to implement the {requirements}. Store the code in a file names as solutions.py",
    agent=coder,
    expected_output="Python code in solutions.py",
    output_file= "solutions.py"
    )

testing_task = Task(
    name="Testing Task",
    description="""Run the code inside solutions.py and test it against 5 test cases.
        Put the inputs, expected outputs, and actual outputs.
        Save the results in a file named test_results.txt.""",
    agent=tester,
    expected_output="Test results in test_results.txt",
    output_file= "test_results.txt",
    context=[coding_task]
    )

# Create Crew object
crew = Crew(
    name="Python Development Crew",
    agents=[coder, tester],
    tasks=[coding_task, testing_task]
)