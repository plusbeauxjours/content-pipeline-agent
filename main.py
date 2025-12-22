from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel


class ContentPipelineState(BaseModel):

    content_type: str = ""
    topic: str = ""
    max_length: int = 0


class ContentPipelineFlow(Flow):

    @start()
    def init_content_pipeline(self):
        if self.state.content_type not in ["blog", "tweet"]:
            raise ValueError("Content type must be either blog or tweet")

        if self.topic == "":
            raise ValueError("Topic is required")

        if self.state.content_type == "blog":
            self.state.max_length = 150
        elif self.state.content_type == "tweet":
            self.state.max_length = 280
        elif self.state.content_type == "linkedin":
            self.state.max_length = 3000

    @listen(init_content_pipeline)
    def conduct_research(self) -> bool:
        print("Researching...")
        return True

    @router(conduct_research)
    def router(self) -> str:
        content_type = self.state.content_type

        if content_type == "blog":
            return "make_blog"
        elif content_type == "tweet":
            return "make_tweet"
        elif content_type == "linkedin":
            return "make_linkedin"

    @listen("make_blog")
    def handle_make_blog(self) -> bool:
        print("Making blog...")
        return True

    @listen("make_tweet")
    def handle_make_tweet(self) -> bool:
        print("Making tweet...")
        return True

    @listen("make_linkedin")
    def handle_make_linkedin(self) -> bool:
        print("Making linkedin...")
        return True

    @listen(handle_make_blog)
    def check_seo(self) -> bool:
        print("Checking SEO...")
        return True

    @listen(or_(handle_make_tweet, handle_make_linkedin))
    def check_virality(self) -> bool:
        print("Checking Virality...")
        return True

    @listen(or_(check_seo, check_virality))
    def finalize_content(self) -> bool:
        print("Finalizing content...")
        return True


flow = ContentPipelineFlow()
# flow.kickoff(inputs={"content_type": "blog", "topic": "AI Dog Training"})

flow.plot()
