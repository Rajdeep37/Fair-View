import re
from typing import List, Dict
from nltk.tokenize import sent_tokenize

class QuestionAnswerExtractor:
    def __init__(self):
        """Initialize the Q&A extractor with question detection patterns."""
        self.question_starters = [
            "what", "how", "why", "where", "when", "who", "which", "whose",
            "can you", "could you", "would you", "do you", "did you", "are you", "tell me"
        ]

    def is_question(self, text: str) -> bool:
        """Detect if a sentence is a question."""
        text = text.strip().lower()
        if not text:
            return False
        if text.endswith('?'):
            return True
        return any(text.startswith(start) for start in self.question_starters)

    def clean_text(self, text: str) -> str:
        """Clean text by removing extra spaces."""
        return re.sub(r'\s+', ' ', text).strip()

    def extract_qa_pairs(self, text: str) -> List[Dict[str, str]]:
        """Extract Q&A pairs from the text."""
        sentences = re.split(r'(?<=[.?!])\s+', text)
        qa_pairs = []
        current_question = None
        current_answer = []

        for sentence in sentences:
            if self.is_question(sentence):
                if current_question:
                    qa_pairs.append({
                        "question": self.clean_text(current_question),
                        "answer": self.clean_text(" ".join(current_answer))
                    })
                current_question = sentence
                current_answer = []
            else:
                if current_question:
                    current_answer.append(sentence)

        if current_question and current_answer:
            qa_pairs.append({
                "question": self.clean_text(current_question),
                "answer": self.clean_text(" ".join(current_answer))
            })

        return qa_pairs


if __name__ == "__main__":
    sample_text = """Thanks for coming in today. Uh, why don’t we start with a quick intro — can you tell me a bit about your background? 
Yeah, sure… um, so I’ve been working as a backend engineer for a little over three years now. Mostly Python and Django, but in my first job I also had some exposure to Go, working on small microservices. 
Before that, I did my computer science degree. I guess what I really enjoy is solving scaling problems, like making things run faster when there’s a ton of data. Okay, that’s good. So let’s warm up. What’s the difference between a process and a thread? 
Right… so a process has its own memory space, it’s like a totally separate program running. A thread is lighter, it lives inside a process and shares memory with other threads. Processes are more isolated but heavier, and threads are faster to spin up, but then you have to deal with synchronization issues. Mm-hmm. 
Now imagine, uh, you’re running a web service and suddenly people are complaining it’s super slow. What do you check first? First thing, I’d look at the basics: CPU, memory usage, disk I/O. If those look fine, I’d move on to the database, maybe queries are slow or missing an index. 
Then I’d check traffic, maybe there’s a sudden spike. Oh, and sometimes it’s network latency between services. Logging and metrics, like in Datadog or New Relic, help me narrow it down. 
Okay. How would you, let’s say, detect a cycle in a linked list? Uh, I’d probably go with Floyd’s cycle detection algorithm — you know, the slow and fast pointer approach. One pointer moves step by step, the other skips ahead. If they ever meet, then yeah, that means there’s a cycle. Got it. 
Now tell me… how does a hash map work internally? So, keys get passed into a hash function, which gives you an index in an array. If two keys map to the same index, that’s a collision. Usually you fix that with chaining, like a linked list at that slot, or open addressing. 
Okay. Let me shift gears. Have you worked with cloud services? Yeah, mostly AWS. EC2 for compute, S3 for storage, RDS for relational databases, and Lambda for serverless stuff. Sometimes I used CloudWatch for monitoring. 
Can you describe a production issue you had to fix? Yeah, sure… so one time a dependency update broke our background worker. Suddenly tasks stopped processing. I, uh, rolled back the change quickly, then added alerts so we’d know if that happened again. Later I patched the code to handle the new dependency properly. That was stressful."""

    extractor = QuestionAnswerExtractor()
    qa_pairs = extractor.extract_qa_pairs(sample_text)
    print(f"Extracted {len(qa_pairs)} Q&A pairs:")
    for i, pair in enumerate(qa_pairs, 1):
        print(f"\nQ{i}: {pair['question']}")
        print(f"A{i}: {pair['answer']}")
