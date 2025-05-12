from setuptools import setup, find_packages

setup(
    name = "medikbot",
    version = "0.0.1",
    author = "Moby Mikes",
    author_email = "moby.mikes@gmail.com",
    packages = find_packages(),
    license = "MIT",
    install_requires = [
        "sentence-transformers==2.2.2",
        "langchain",
        "flask",
        "pypdf",
        "python-dotenv",
        "pinecone[grpc]",
        "langchain-pinecone",
        "langchain_community",
        "langchain_openai",
        "langchain_experimental"
    ]
)