#Omar Shahwan___1/4/2024
#Desc: This project is a chatbot designed to become more intelligent and experienced with its responses as the user asks it questions and teaches it how to respond (offline)

import json #json file can be accessed
from difflib import get_close_matches #Match best response to input given to chatbot, with accuracy level & number of top matched up to the programmer

#Function to load knowledge base from json file:
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file: #'r' is read mode
        data: dict = json.load(file)
    return data

#Function to save replies from knowledge base, to be loaded during later use
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file: #'w' is write mode
        json.dump(data, file, indent=2)
        
#Find best match is used to look through the knowledge base for the question asked, returning either the string answering it or finding none that apply
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6) #uses the get_close_matches func to search the json file knowledge base and give the top 60% or more similar match or return with none if none exist
    return matches[0] if matches else None #return the matches at the index of 0 to display the one match if any are found

def get_answer_for_question(question:str,knowledge_base:dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

#Write the script details:
def chat_bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    while True:
        user_input: str = input('You: ') #Prompt for user input
        if user_input.lower() == 'quit': #How to quit program
            break
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match: #Produce best match if one is found
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else: #Ask for the answer if none are registered
            print("Bot: I don't know, can you teach me?")
            new_answer: str = input("Type the answer to answer or type 'skip' to skip:\n") #Prompt user to teach bot or skip if no answer is available
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer}) #Adds new question and answer to knowledgfe base json file
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')

if __name__ == "__main__":
    chat_bot()