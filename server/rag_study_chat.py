import os
import json
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.agents import Tool, initialize_agent, AgentType

from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

tracer_provider = register()
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)

# Load environment variables (for OpenAI API key)
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Load JSON data
json_file_path = "data/clinical_trials_results.json"
with open(json_file_path, "r") as file:
    data = json.load(file)

# Preprocess the JSON data into LangChain documents
def preprocess_clinical_studies(data):
    """Convert clinical studies JSON data into a list of LangChain documents."""
    documents = []
    for study in data:
        protocol = study.get("protocolSection", {})
        identification = protocol.get("identificationModule", {})
        description = protocol.get("descriptionModule", {})
        eligibility = protocol.get("eligibilityModule", {})
        conditions = protocol.get("conditionsModule", {})

        # Extract relevant information
        study_id = identification.get("nctId", "Unknown ID")
        brief_title = identification.get("briefTitle", "No Title Provided")
        detailed_description = description.get("detailedDescription", "No Description Provided")
        inclusion_criteria = eligibility.get("eligibilityCriteria", "No Eligibility Criteria Provided")
        conditions_list = ", ".join(conditions.get("conditions", []))

        # Create document text
        doc_text = (
            f"Study ID: {study_id}\n"
            f"Title: {brief_title}\n"
            f"Description: {detailed_description}\n"
            f"Inclusion Criteria: {inclusion_criteria}\n"
            f"Conditions: {conditions_list}"
        )
        documents.append(Document(page_content=doc_text))
    return documents

# Preprocess JSON data
documents = preprocess_clinical_studies(data)

# Split the documents for better embedding and retrieval
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
splits = text_splitter.split_documents(documents)

# Create a FAISS vectorstore
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(splits, embeddings)
retriever = db.as_retriever()

# Create a retriever tool
tool = Tool(
    name="search_studies",
    func=retriever.get_relevant_documents,
    description="Searches and retrieves information from clinical studies."
)
tools = [tool]

# Load OpenAI LLM
llm = ChatOpenAI(temperature=0, verbose=True)

# Initialize agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Example query
query = "What is the study titled 'Cardiometabolic Screening Program' about?"
result = agent.run(query)
print(f"Query: {query}\nResult: {result}")