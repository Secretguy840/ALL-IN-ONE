function chatbot(input) {
    input = input.toLowerCase();
    
    if (input.includes('hello') || input.includes('hi')) {
        return "Hello! How can I help you today?";
    } else if (input.includes('how are you')) {
        return "I'm just a bot, but I'm functioning well!";
    } else if (input.includes('bye')) {
        return "Goodbye! Have a great day!";
    } else {
        return "I'm not sure how to respond to that. Can you ask me something else?";
    }
}

// Test
console.log(chatbot("Hello there!"));
console.log(chatbot("How are you doing?"));
console.log(chatbot("What's the weather like?"));