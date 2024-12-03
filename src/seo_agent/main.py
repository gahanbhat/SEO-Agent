
import sys
import warnings
from datetime import datetime

from crew import SeoAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    inputs = {
        'client': 'Google',
        'topic': 'LLMs',
        'type of post': 'blog post',
        'language': 'English',
        'keywords': 'LLMs, AI',
        'competitors': 'OpenAI, Anthropic',
    }
    SeoAgent().crew().kickoff(inputs=inputs)

run()