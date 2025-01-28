from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.chains.summarize import load_summarize_chain
from .llm_config import initialize_groq
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

groq = initialize_groq()


def summarize(url: str) -> str:
    """
    Takes a url from the api request and uses groq to summarize the transcript of the video.

    Args:
        url: the url of the youtube video to use.

    Returns:
        string: transcript summary.
    """
    # load full transcript.
    loader = YoutubeLoader.from_youtube_url(youtube_url=url, language=["en", "en-US"])

    # fetch transcript
    transcript = loader.load()

    # spit transcript into chunks
    splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=10)
    chunks = splitter.split_documents(transcript)
    sum_chain = load_summarize_chain(llm=groq, chain_type="refine")
    summary = sum_chain.run(chunks)
    print(summary)
    return summary
