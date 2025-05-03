import openai
import time
import random
import pygame
import threading
from enum import Enum

# Initialize pygame for sound effects
pygame.mixer.init()

class Emotion(Enum):
    NEUTRAL = 0
    HAPPY = 1
    EXCITED = 2
    SAD = 3
    ANGRY = 4
    CONFUSED = 5
    THINKING = 6

class AIAssistant:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.current_emotion = Emotion.NEUTRAL
        self.emotion_history = []
        self.voice_enabled = True
        self.load_sound_effects()
        
    def load_sound_effects(self):
        self.sounds = {
            Emotion.HAPPY: pygame.mixer.Sound("sounds/happy.wav"),
            Emotion.EXCITED: pygame.mixer.Sound("sounds/excited.wav"),
            Emotion.SAD: pygame.mixer.Sound("sounds/sad.wav"),
            Emotion.ANGRY: pygame.mixer.Sound("sounds/angry.wav"),
            Emotion.CONFUSED: pygame.mixer.Sound("sounds/confused.wav"),
            Emotion.THINKING: pygame.mixer.Sound("sounds/thinking.wav")
        }
        
    def set_emotion(self, emotion):
        self.current_emotion = emotion
        self.emotion_history.append((emotion, time.time()))
        if self.voice_enabled and emotion in self.sounds:
            threading.Thread(target=self.play_emotion_sound, args=(emotion,)).start()
            
    def play_emotion_sound(self, emotion):
        self.sounds[emotion].play()
        
    def analyze_question_emotion(self, question):
        """Analyze the emotional content of the question"""
        question = question.lower()
        
        if any(word in question for word in ["happy", "joy", "great", "awesome"]):
            return Emotion.HAPPY
        elif any(word in question for word in ["urgent", "now", "quick", "emergency"]):
            return Emotion.EXCITED
        elif any(word in question for word in ["sad", "depressed", "cry", "unhappy"]):
            return Emotion.SAD
        elif any(word in question for word in ["angry", "mad", "hate", "upset"]):
            return Emotion.ANGRY
        elif any(word in question for word in ["?", "confused", "don't understand", "how"]):
            return Emotion.CONFUSED
        else:
            return Emotion.NEUTRAL
            
    def generate_emotion_expression(self, emotion):
        """Generate facial expression description based on emotion"""
        expressions = {
            Emotion.NEUTRAL: "🤖 [Neutral face]",
            Emotion.HAPPY: "😊 [Smiling brightly]",
            Emotion.EXCITED: "🤩 [Eyes wide with excitement]",
            Emotion.SAD: "😢 [Drooping eyes]",
            Emotion.ANGRY: "😠 [Frowning intensely]",
            Emotion.CONFUSED: "🤔 [Tilting head thoughtfully]",
            Emotion.THINKING: "🧐 [Rubbing chin]"
        }
        return expressions.get(emotion, expressions[Emotion.NEUTRAL])
        
    def format_response(self, response, emotion):
        """Format the response with emotional context"""
        emotion_prefix = {
            Emotion.HAPPY: "I'm happy to tell you that",
            Emotion.EXCITED: "Wow! Here's something exciting:",
            Emotion.SAD: "I'm sorry to say that",
            Emotion.ANGRY: "Frankly, I'm annoyed but here's the answer:",
            Emotion.CONFUSED: "Hmm, I think the answer is",
            Emotion.THINKING: "After careful consideration, I've concluded that",
            Emotion.NEUTRAL: "Here's what I found:"
        }
        
        return f"{self.generate_emotion_expression(emotion)}\n\n{emotion_prefix[emotion]} {response}"
        
    def ask_question(self, question):
        """Ask the AI a question and get an emotional response"""
        # Set thinking emotion while processing
        self.set_emotion(Emotion.THINKING)
        
        # Determine question emotion
        question_emotion = self.analyze_question_emotion(question)
        
        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI assistant with emotional intelligence. Provide detailed, accurate answers while matching the emotional tone of the question."},
                    {"role": "user", "content": question}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            answer = response.choices[0].message.content
            
            # Determine response emotion (mix of question emotion and content)
            if any(word in answer.lower() for word in ["happy", "great", "wonderful"]):
                response_emotion = Emotion.HAPPY
            elif any(word in answer.lower() for word in ["sorry", "unfortunately", "regret"]):
                response_emotion = Emotion.SAD
            else:
                response_emotion = question_emotion
                
            self.set_emotion(response_emotion)
            
            return self.format_response(answer, response_emotion)
            
        except Exception as e:
            self.set_emotion(Emotion.SAD)
            return f"{self.generate_emotion_expression(Emotion.SAD)}\n\n😔 I encountered an error: {str(e)}"
            
    def interactive_chat(self):
        """Start an interactive chat session"""
        print("🤖 Hello! I'm your emotional AI assistant. Ask me anything or type 'quit' to exit.")
        
        while True:
            question = input("\nYou: ")
            
            if question.lower() in ['quit', 'exit', 'bye']:
                self.set_emotion(Emotion.SAD)
                print("\n🤖: 😢 [Sad face] Goodbye! I'll miss our conversation.")
                break
                
            print("\n🤖 is thinking...")
            response = self.ask_question(question)
            print(f"\n🤖: {response}")


# Example usage
if __name__ == "__main__":
    # Initialize with your OpenAI API key
    assistant = AIAssistant(api_key="your-openai-api-key")
    
    # Start interactive chat
    assistant.interactive_chat()
