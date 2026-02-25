# =========================================================
# 보고서 작성 + Word/PDF 자동 생성 Agent
# =========================================================
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from docx import Document
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
#from reportlab.pdfbase.cidfonts import UnicodeCIDfont

llm = ChatOllama(model="llama3.1:latest", temperature=0)

PROMPT = """
너는 보고서 작성 Agent이다.
아래 구조로 보고서를 작성하라:
1. 개요
2. 배경
3. 주요 내용
4. 분석 및 시사점
5. 결론
"""
#에이전트 생성
agent = create_react_agent(model=llm, tools=[], prompt=PROMPT)

#보고서 작성
def generate_report(topic: str) -> str:
    result = agent.invoke({
        "messages": [HumanMessage(content=f"주제: {topic}")]
    })
    return result["messages"][-1].content

def save_word(text, filename):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    doc.save(filename)

def save_pdf(text, filename):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename)
    """style = styles["Normal"]"""
    story = [Paragraph(line, styles["Normal"]) for line in text.split("\n") if line.strip()]
    doc.build(story)
#Agent AI 구동
def run():
    topic = input("보고서 주제: ")
    report = generate_report(topic)

    save_word(report, "report.docx")
    save_pdf(report, "report.pdf")

    print("report.docx / report.pdf 생성 완료")

if __name__ == "__main__":
    run()
