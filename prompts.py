from langchain.prompts import ChatPromptTemplate


class prompt:
    def __init__(self) -> None:
        pass

    def KeyPointsPrompt(self):
        temp = ChatPromptTemplate.from_template(
            template="""<s>[INST] For the given objective, come up with at least ten key-points user should do to achive the objective. \nThese key-points should involve all the important points to do to achive the task, if the key-points are executed correctly, that will complete the objective.\nConsider FEEDBACK if provided to genrate better response than before. [/INST]</s>"""
            + """[INST] OBJECTIVE:\n{objective}\n\nFEEDBACK:\n{feedback}\n[/INST]\n"""
        )
        return temp

    def ExcecutorPrompt(self):
        temp = ChatPromptTemplate.from_template(
            template="""<s>[INST] Complete the given TASK like a market analyst, and return findings as detailed bullet points, a descriptive and detailed summary, and some year on year data on diffenrent fields if possible, dont respond fake data .Bullet points should sounds professional, include names and should be in correct order. Summary should be crisp. And year on year data should be justified, fields of data should be well descriptive. These key-points, summary and data will be important hence respond correctly. [/INST]</s>\n"""
            + """[INST] TASK:\n{sub_task}\n[/INST]\n"""
        )
        return temp
