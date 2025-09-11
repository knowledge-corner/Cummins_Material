from app_crew import crew

# if __name__ == "__main__":
#     description = "A python function to calculate factorial."
#     result = crew.kickoff(inputs={"requirements": description})
#     print("==========Final Output:===========")
#     print(result.tasks_output[0])  # Output of coding task


import gradio as gr

def run_crew(description):
    result = crew.kickoff(inputs={"requirements": description})
    return result.tasks_output[0]  # Output of coding task

gr.Interface(
    fn=run_crew,
    inputs=gr.Textbox(lines=4, label="Enter the requirements"),
    outputs=gr.Textbox(lines=500, label="Code Output"),
    title="Python Code Generator and Tester",
).launch(share=True)