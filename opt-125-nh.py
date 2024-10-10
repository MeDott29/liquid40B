from openai import OpenAI

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:2242/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

completion = client.completions.create(
    model="ccore/opt-125-nh",
    prompt="Once upon a time",
    temperature=1.1,
    extra_body={"min_p": 0.1}
)

print("Completion result:", completion)