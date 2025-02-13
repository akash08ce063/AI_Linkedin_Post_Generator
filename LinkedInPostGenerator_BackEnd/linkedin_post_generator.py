from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
import asyncio
from linkedin_post_evaluator import LinkedInPostEvaluator
import datetime

class LinkedInPostGenerator:
    def __init__(self):
        self.linked_in_post_evaluator = LinkedInPostEvaluator()
        self.post_generation_model = ChatOllama(
            model = "llama3.1",
            temperature = 0,
            num_predict = 256,
        )
        self.linkedin_web_prompt_1 = """
            You are a LinkedIn content creator. Given the following webpage content, please generate a professional and engaging LinkedIn post that summarizes the key points and encourages engagement.

                - The post should be concise, attention-grabbing, and formatted to appeal to a LinkedIn audience.
                - Highlight the main takeaway or insights from the content.
                - Make the post sound insightful, yet approachable, suitable for professionals in the relevant industry.
                - End the post with a call-to-action (CTA) that encourages comments or engagement.

            Webpage content:

            {web_content}
                
            """
        self.linkedin_web_prompt_2 = """
            Transform the following webpage content into a concise, thought-provoking LinkedIn post. Focus on key insights or data points that are relevant to professionals, and present them in a way that sparks discussion and adds value to your network. The post should be clear, engaging, and actionable. Highlight the most compelling parts of the webpage, and tie them to real-world applications or challenges.

            Key elements to emphasize:

                - Relevant trends, statistics, or findings.
                - Industry impact or potential outcomes.
                - Practical takeaways or lessons for professionals.
                - A clear and motivating call-to-action (CTA) to encourage engagement or further reading.
                - The tone should be professional and insightful, with a focus on generating conversation or sharing valuable knowledge within the community

            Webpage content:

            {web_content}
            """ 

    async def generate(self, type, value):
        response = []
        linked_in_posts = await self.generate_post_given_weblinks(value)
        linked_in_posts_evaluation_results = self.linked_in_post_evaluator.evaluate(linked_in_posts)
        for post, evaluation in zip(linked_in_posts, linked_in_posts_evaluation_results):
            response.append({"content": post, "scores": evaluation, "timestamp": datetime.now()})
        return response
    

    async def generate_post_given_weblinks(self, web_links):
        loader = WebBaseLoader(web_links)
        documents=loader.load()

        linkedin_web_prompt = """
        You are a LinkedIn content creator. Given the following webpage content, please generate a professional and engaging LinkedIn post that summarizes the key points and encourages engagement.

            - The post should be concise, attention-grabbing, and formatted to appeal to a LinkedIn audience.
            - Highlight the main takeaway or insights from the content.
            - Make the post sound insightful, yet approachable, suitable for professionals in the relevant industry.
            - End the post with a call-to-action (CTA) that encourages comments or engagement.

        Webpage content:

        {web_content}
            
        """

        linkedin_web_prompt_2 = """
        Transform the following webpage content into a concise, thought-provoking LinkedIn post. Focus on key insights or data points that are relevant to professionals, and present them in a way that sparks discussion and adds value to your network. The post should be clear, engaging, and actionable. Highlight the most compelling parts of the webpage, and tie them to real-world applications or challenges.

        Key elements to emphasize:

            - Relevant trends, statistics, or findings.
            - Industry impact or potential outcomes.
            - Practical takeaways or lessons for professionals.
            - A clear and motivating call-to-action (CTA) to encourage engagement or further reading.
            - The tone should be professional and insightful, with a focus on generating conversation or sharing valuable knowledge within the community

        Webpage content:

        {web_content}
        """

        
        linkedin_prompt_1 = PromptTemplate.from_template(linkedin_web_prompt)
        prompt_1 = linkedin_prompt_1.invoke({"web_content": documents[0].page_content})

        linkedin_prompt_2 = PromptTemplate.from_template(linkedin_web_prompt_2)
        prompt_2 = linkedin_prompt_2.invoke({"web_content": documents[0].page_content})

        linkedin_prompts = [prompt_1, prompt_2]


        posts = await self.get_responses_parallel(linkedin_prompts)
        post_contents = [post.content for post in posts]
        return post_contents
    

    async def get_model_response(self, prompt: str):
        # Get the response asynchronously
        response = await self.post_generation_model.ainvoke(prompt)
        return response

    async def get_responses_parallel(self, prompts):
        # Run all the model calls in parallel using asyncio.gather
        tasks = [self.get_model_response(prompt) for prompt in prompts]
        responses = await asyncio.gather(*tasks)
        return responses