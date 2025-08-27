from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables.graph import MermaidDrawMethod
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain.vectorstores import Chroma

load_dotenv()  # Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")

chroma_path = "chroma"

embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=chroma_path, embedding_function=embeddings)
    

#initilize the state graph
class State(TypedDict):
    query: str
    category: str
    response: str

# categorize the query
def query_categorization(state):
    prompt = ChatPromptTemplate.from_template(
        "Categorize the following query into one of the following categories: 'weather', 'jobsite_related', 'general'.Note: The query will be jobsite_related if the word 'jobsite' is mentioned in that. The query will be weather if user is asking about the weather. Just return a single word without any explanation. \n\nQuery: {query}\n\nCategory:"
    )
    chain = prompt | ChatOpenAI(model= "gpt-4o",temperature=0)
    response = chain.invoke({"query": state["query"]}).content.lower()
    print(f"Categorized query: {response}")
    return {"response" : response}
  
#first tool: weather
def weather(state):
    """A tool that takes in a query and returns a weather-related response."""
    return {"response": f"The weather tool is not implemented yet."}

#second tool: jobsite_related
def jobsite_related(state):
    """A tool that takes in a query and returns a jobsite-related response."""
    #Extract the content from the vector db
    docs = vectordb.similarity_search(state["query"], k=3)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Use the following context to answer the query: {query}\n\nContext: {context}"
    )
    chain = prompt | ChatOpenAI(model= "gpt-4o",temperature=0)
    response = chain.invoke({"query": state["query"], "context": context}).content
    return {"response" : response}
   
#third node will be for general queries
def general(state):
    prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant. Answer the following query: {query}"
    )
    chain = prompt | ChatOpenAI(model= "gpt-4o",temperature=0)
    response = chain.invoke({"query": state["query"]}).content
    return {"response" : response}

#conditional function to route the query to the appropriate tool
def route(state):
    if state["response"] == "weather":
        return "weather"
    elif state["response"] == "jobsite_related":
        return "jobsite_related"
    else:
        return "general"

#compile the state graph
workflow = StateGraph(State)


#Add nodes to the graph
workflow.add_node("query_categorization", query_categorization)
workflow.add_node("weather", weather)
workflow.add_node("jobsite_related", jobsite_related)
workflow.add_node("general", general)

#Add edges to the graph
workflow.set_entry_point("query_categorization")
#conditional edges based on the category

workflow.add_conditional_edges("query_categorization", route,
                               {
                                      "weather": "weather",
                                      "jobsite_related": "jobsite_related",
                                      "general": "general"
                               })

#End edges
workflow.add_edge("weather", END)
workflow.add_edge("jobsite_related", END)
workflow.add_edge("general", END)


#Compile the graph
app = workflow.compile()

#Graph visualization mermaid
png = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
with open("LangGraphWithRAG.png", "wb") as f:
    f.write(png)

#test the graph with a sample query
if __name__ == "__main__":
    state = {"query": "Who is the owner of jobsite sentry?"}
    result = app.invoke(state)
    print(result)