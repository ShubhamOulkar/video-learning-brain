import asyncio
import json
import pathlib

import cognee
from cognee import SearchType
from cognee.infrastructure.llm.LLMGateway import LLMGateway
from pydantic import BaseModel, Field

QUERY_FILE = pathlib.Path(__file__).parent / "queries.json"
OUTPUT_FILE = pathlib.Path(__file__).parent / "evaluation_results.json"

DATASET_NAME = "multimedia_processing"


class RetrievalEvaluation(BaseModel):
    score: int = Field(
        ge=0,
        le=10,
        description="Overall correctness score from 0 to 10.",
    )
    passed: bool = Field(
        description="True if the retrieved answer sufficiently answers the question."
    )
    reasoning: str = Field(description="Brief explanation of why the score was assigned.")


JUDGE_PROMPT = """
    You are evaluating the quality of a retrieval system.

    You will receive:

        1. A user query.
        2. A reference answer (ground truth).
        3. A retrieved answer.

    Evaluate ONLY whether the retrieved answer correctly answers the question.

    Guidelines:

        - Ignore wording differences.
        - Reward semantically equivalent answers.
        - Penalize factual errors.
        - Penalize hallucinated information.
        - Penalize important missing information.
        - Do not use outside knowledge.
        - Evaluate only against the provided reference answer.

    Scoring:

        10 = Completely correct and complete.
        8-9 = Correct with minor omissions.
        6-7 = Mostly correct but missing important details.
        3-5 = Partially correct.
        1-2 = Mostly incorrect.
        0 = Completely incorrect or unrelated.

    Return only the structured response.
    """


async def evaluate_query(test_case: dict) -> dict:
    """
    Run a single retrieval query and evaluate it with an LLM judge.
    """

    results = await cognee.recall(
        query_text=test_case["query"],
        datasets=[DATASET_NAME],
        query_type=SearchType.RAG_COMPLETION,
    )

    if results:
        retrieved_answer = "\n".join(
            result.text
            for result in results
            if getattr(result, "text", None)  # type: ignore
        )
    else:
        retrieved_answer = ""

    judge_input = f"""
        User Query:
        {test_case["query"]}

        Reference Answer:
        {test_case["reference_answer"]}

        Retrieved Answer:
        {retrieved_answer}
        """
    # using cognee interface for LLM provider
    evaluation: RetrievalEvaluation = await LLMGateway.acreate_structured_output(
        text_input=judge_input,
        system_prompt=JUDGE_PROMPT,
        response_model=RetrievalEvaluation,
    )

    return {
        "id": test_case["id"],
        "category": test_case["category"],
        "query": test_case["query"],
        "reference_answer": test_case["reference_answer"],
        "retrieved_answer": retrieved_answer,
        "score": evaluation.score,
        "passed": evaluation.passed,
        "reasoning": evaluation.reasoning,
    }


async def main():
    with open(QUERY_FILE, encoding="utf-8") as f:
        test_cases = json.load(f)

    results = []

    for test_case in test_cases:
        print(f"Running {test_case['id']}:{test_case['query']}...")

        result = await evaluate_query(test_case)

        results.append(result)

        print(f"Score: {result['score']}/10 | {'PASS' if result['passed'] else 'FAIL'}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    total = len(results)
    passed = sum(r["passed"] for r in results)
    average = sum(r["score"] for r in results) / total

    print()
    print("=" * 60)
    print(f"Total Queries : {total}")
    print(f"Passed        : {passed}")
    print(f"Failed        : {total - passed}")
    print(f"Average Score : {average:.2f}/10")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
