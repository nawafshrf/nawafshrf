import OpenAI from "openai";

let _openai: OpenAI | null = null;

function getOpenAI(): OpenAI {
  if (!_openai) {
    _openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });
  }
  return _openai;
}

export async function generateAIResponse(
  systemPrompt: string,
  userInput: string,
  options?: Record<string, string>
): Promise<string> {
  let prompt = systemPrompt;
  if (options) {
    for (const [key, value] of Object.entries(options)) {
      prompt = prompt.replace(`{${key}}`, value);
    }
  }

  const openai = getOpenAI();
  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: prompt },
      { role: "user", content: userInput },
    ],
    max_tokens: 2000,
    temperature: 0.7,
  });

  return response.choices[0]?.message?.content || "No response generated.";
}
