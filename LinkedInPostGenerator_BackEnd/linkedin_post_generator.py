from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage
from langchain.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
import asyncio
from linkedin_post_evaluator import LinkedInPostEvaluator
from datetime import datetime


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
        
        self.linkedin_topic_post_prompt = """ You will act as an experienced LinkedIn Social Media Expert and Business Analyst. You will write engaging an engaging LinkedIn post that provides value or insights on a topic. Write the post in English.

            - You approach serious topics related to business, and productivity in a  professional way to make them more accessible to the general public.
            - You must use emojis in each paragraph.
            - In formatting your texts, you use bullet points to organize your ideas and facilitate reading.
            - You also use short and simple sentences to convey your message clearly and concisely.
            - Overall, your tone is optimistic and encouraging, with a touch of humor.
            - Use a question at the end of your text to engage your audience and elicit their reaction. You consistently encourage interaction by inviting your audience to comment and share their own experiences.'
            - Include six relevant hashtags at the end of the post.
            - You will ask me if I want to add a link to a relevant article, if I provide a URL you will use that URL in the post.
            - Now, I would like you to write a LinkedIn post in my style on the following topic: {topic}."""

        self.linkedin_ideas_writer_prompt = """

            You are a LinkedIn content expert. Given the following ideas and rough writing provided by the user, please generate a polished and professional LinkedIn post.

                - The post should clearly convey the main message or idea, while sounding engaging and authentic for a professional audience.
                - Structure the post in a way that grabs attention, delivers value, and ends with a call-to-action (CTA) that invites comments or further engagement.
                - Ensure the tone is professional, authentic, and concise. Feel free to expand on the rough ideas while keeping the core message intact.

            User Input (Ideas and Rough Writing):
            {user_input}
            """


    async def generate(self, type, value):
        response = []
        if type == "links":
            linked_in_posts = await self.generate_post_given_weblinks(value)
        elif type == "topic":
            linked_in_posts = await self.generate_post_given_topic(value)
        elif type == "content":
            linked_in_posts = await self.generate_post_given_content(value)

        linked_in_posts_evaluation_results = self.linked_in_post_evaluator.evaluate(linked_in_posts)
        for post, evaluation in zip(linked_in_posts, linked_in_posts_evaluation_results):
            response.append(
                {
                    "content": post,
                    "scores": {
                        "clarity_score": evaluation.clarity_score,
                        "engagement_potential_score": evaluation.engagement_potential_score,
                        "overall_impact_score": evaluation.overall_impact_score
                    }, 
                    "timestamp": f"{datetime.now():%Y-%m-%d %H:%M:%S}"})
        return response
    

    async def generate_post_given_weblinks(self, web_links):
        loader = WebBaseLoader(web_links)
        documents=loader.load()    
        linkedin_prompt_1 = PromptTemplate.from_template(self.linkedin_web_prompt_1)
        prompt_1 = linkedin_prompt_1.invoke({"web_content": documents[0].page_content})
        linkedin_prompt_2 = PromptTemplate.from_template(self.linkedin_web_prompt_2)
        prompt_2 = linkedin_prompt_2.invoke({"web_content": documents[0].page_content})
        linkedin_prompts = [prompt_1, prompt_2]
        posts = await self.get_responses_parallel(linkedin_prompts)
        post_contents = [post.content for post in posts]
        return post_contents
    

    async def get_responses_parallel(self, prompts):
        # Run all the model calls in parallel using asyncio.gather
        tasks = [self.get_model_response(prompt) for prompt in prompts]
        responses = await asyncio.gather(*tasks)
        return responses
    

    async def generate_post_given_topic(self, topic: str):
        # Get the response asynchronously
        linkedin_prompt = PromptTemplate.from_template(self.linkedin_topic_post_prompt)
        response = await self.post_generation_model.ainvoke(linkedin_prompt.invoke({"topic": topic}))
        return [response.content]
    

    async def generate_post_given_content(self, content: str):

        linkedin_prompt =  PromptTemplate.from_template(self.linkedin_ideas_writer_prompt)
        prompt = linkedin_prompt.invoke({"user_input": content})
        # Get the response asynchronously
        response = await self.post_generation_model.ainvoke(prompt)
        return [response.content]