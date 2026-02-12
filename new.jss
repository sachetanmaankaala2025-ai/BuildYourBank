import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import OpenAI from "openai";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

app.post("/generate-question", async (req, res) => {
  try {
    const { age } = req.body;

    const response = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [
        {
          role: "system",
          content: `Generate one multiple choice finance question for a ${age} year old child. Include 4 options and clearly mark correct answer.`
        }
      ],
    });

    res.json({ question: response.choices[0].message.content });

  } catch (error) {
    res.status(500).json({ error: "Error generating question" });
  }
});

app.listen(5000, () => {
  console.log("🚀 Server running at http://localhost:5000");
});