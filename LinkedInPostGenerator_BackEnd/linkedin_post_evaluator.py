import pydantic
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

class LinkinPostEvaluationScore(pydantic.BaseModel):
    clarity_score: int = pydantic.Field(..., ge=1, le=10, description="How clear and easy to understand is the message in this post?")
    engagement_potential_score: int = pydantic.Field(..., ge=1, le=10, description="How likely is this post to engage the LinkedIn audience?")
    overall_impact_score: int = pydantic.Field(..., ge=1, le=10, description="How impactful is this post in terms of its value to the audience?")

class LinkedInPostEvaluator:
    def __init__(self):
        linkedin_evaluation_prompt = """
        Please evaluate the following LinkedIn post based on the following criteria:

            - Clarity Score: How clear and easy to understand is the message in this post? Is the information presented logically and concisely? Consider how well the post conveys its message without any ambiguity or unnecessary complexity. Rate Clarity on a scale of 1 to 10, where 1 is extremely unclear and 10 is very clear and easy to understand.
            - Engagement Potential Score: How likely is this post to engage the LinkedIn audience? Consider if the post encourages interaction (likes, comments, shares), if it poses a question, shares insightful information, or prompts action. Does it have elements that could spark conversation or debate? Rate Engagement Potential on a scale of 1 to 10, where 1 is not engaging at all and 10 is highly likely to spark significant engagement.
            - Overall Impact Score: How impactful is this post in terms of its value to the audience? Does it leave a lasting impression, inspire action, or provide valuable insight? Does it add value to the professional community or the target audience? Consider whether the post helps inform, educate, or inspire the reader. Rate Overall Impact on a scale of 1 to 10, where 1 has no impact and 10 has a highly significant impact on the audience.

        Please provide your scores for each criterion along with brief explanations for your ratings.

        LinkedIn Post:
        {linkedin_post}
        """

        self.evaluation_prompt =  PromptTemplate.from_template(linkedin_evaluation_prompt)
        self.evaluator_llm = ChatOllama(
            model = "llama3.1",
            temperature = 0,
            num_predict = 256,
            format="json"
        )

        self.evaluator_llm = self.evaluator_llm.with_structured_output(LinkinPostEvaluationScore)

    def evaluate(self, linked_in_posts):
        evaluation_results = []
        for post in linked_in_posts:
            prompt = self.evaluation_prompt.invoke({"linkedin_post": post})
            evaluation = self.evaluator_llm.invoke(prompt)
            evaluation_results.append(evaluation)

        return evaluation_results    