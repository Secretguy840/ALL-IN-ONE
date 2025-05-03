const OpenAI = require('openai');

const openai = new OpenAI({
    apiKey: 'your-api-key-here' // Replace with your actual API key
});

async function chatWithGPT(prompt) {
    try {
        const response = await openai.chat.completions.create({
            model: "gpt-3.5-turbo",
            messages: [{ role: "user", content: prompt }],
            temperature: 0.7,
        });
        return response.choices[0].message.content;
    } catch (error) {
        console.error("Error:", error);
        return "Sorry, I encountered an error.";
    }
}

// Example usage
chatWithGPT("Tell me a joke").then(response => console.log(response));