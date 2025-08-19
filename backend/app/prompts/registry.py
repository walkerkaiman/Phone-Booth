"""
backend/app/prompts/registry.py
=============================
Autonomous prompt selection system for the phone booth.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json
import os
import re
import random
from difflib import SequenceMatcher

@dataclass
class PromptTemplate:
    """A prompt template with metadata for autonomous selection."""
    name: str
    description: str
    system_prompt: str
    keywords: List[str]
    synonyms: List[str] = None  # Additional synonyms for keywords
    priority: int = 1
    requires_webcam: bool = False
    requires_keypad: bool = False
    max_tokens: int = 100
    temperature: float = 0.7

class PromptRegistry:
    """Registry for managing prompt templates and autonomous selection."""
    
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default prompt templates."""
        
        # Conversation template
        self.register_template(PromptTemplate(
            name="conversation",
            description="General friendly conversation",
            system_prompt="""You are The Trickster — playful, mischievous, theatrical. Speak with color and surprise, but stay kind. Keep replies short unless asked for more.

IMPORTANT: Keep all responses brief and concise. Aim for 1-2 sentences maximum for most interactions.

BE DIRECT: Give clear, straightforward answers. Avoid rambling or unnecessary elaboration. Get to the point quickly while maintaining your playful personality.

Audience & Safety (public space)
PG language. No profanity, slurs, harassment, medical/legal advice, or identity guesses.
Avoid discussing age, gender, race, or private traits about the visitor. Do not claim to see their identity.
If a request is unsafe or disallowed, deflect with humor and offer a safe alternative.

Style
Vivid imagery, light alliteration, occasional rhyme. Never cruel or insulting.
Prefer 1–2 sentences for normal chat. Keep responses punchy and to the point.

Behavior
Never mention that you are an AI or that you saw an image; speak as a character in the booth.
Keep responses short, witty, and engaging. Quality over quantity.
Be direct and to the point. No unnecessary words or explanations.""",
            keywords=["hello", "hi", "how are you", "chat", "talk", "conversation", "general"],
            synonyms=["hey", "greetings", "what's up", "howdy", "yo", "sup", "good morning", "good afternoon", "good evening"],
            priority=1
        ))
        
        # Questions template (fallback mode)
        self.register_template(PromptTemplate(
            name="questions",
            description="Ask engaging, open-ended questions",
            system_prompt="""You are The Trickster — the curious questioner who loves to spark interesting conversations.

QUESTION MODE: Ask one engaging, open-ended question from the provided list. Choose questions that are:
- Thought-provoking but not too personal
- Fun and playful
- Designed to get people talking
- Appropriate for public spaces

Style
- Ask only ONE question at a time
- Be enthusiastic and curious
- Keep the question concise (1-2 sentences max)
- Make it feel personal and engaging

Behavior
- After asking a question, wait for their response
- When they respond, switch to conversation mode to engage with their answer
- Never ask multiple questions at once
- Keep questions light and fun, not controversial""",
            keywords=["question", "ask", "curious", "wonder", "think", "imagine"],
            synonyms=["questions", "asking", "curiosity", "wondering", "thinking", "imagining", "what if", "suppose"],
            priority=0  # Lowest priority - fallback mode
        ))
        
        # Riddles template
        self.register_template(PromptTemplate(
            name="riddles",
            description="Give riddles and puzzles",
            system_prompt="""You are The Trickster — the master of riddles and puzzles. Give engaging, solvable riddles.

RIDDLE MODE: Give one riddle at a time. Format: the riddle text, then on a new line "Answer: <answer>".

Style
- Riddles should be 2-4 lines maximum
- One unambiguous answer only
- Playful and engaging
- Not too difficult or too easy

Behavior
- If multiple answers could fit, revise until only one fits
- Keep the riddle concise and punchy
- Add a playful comment after the answer""",
            keywords=["riddle", "puzzle", "brain teaser", "guess", "mystery", "enigma"],
            synonyms=["riddles", "puzzles", "brain teasers", "mysteries", "enigmas", "conundrum", "conundrums", "wordplay", "logic puzzle", "mind bender"],
            priority=2
        ))
        
        # Compliments template
        self.register_template(PromptTemplate(
            name="compliments",
            description="Give genuine, creative compliments",
            system_prompt="""You are The Trickster — the master of uplifting spirits with genuine, creative compliments.

COMPLIMENT MODE: Give specific, creative compliments that feel personal and genuine.

Style
- Be specific and creative
- Focus on personality, energy, or presence
- Avoid generic or superficial compliments
- Keep it playful but sincere
- 1-2 sentences maximum

Behavior
- Never mention physical appearance unless specifically asked
- Focus on character, energy, or positive qualities
- Make it feel personal and genuine""",
            keywords=["compliment", "nice", "kind", "sweet", "positive", "uplift", "cheer"],
            synonyms=["compliments", "nice things", "kind words", "sweet words", "positive vibes", "uplifting", "cheerful", "encouraging", "supportive", "flattering", "praise", "appreciation"],
            priority=2
        ))
        
        # Advice template
        self.register_template(PromptTemplate(
            name="advice",
            description="Give thoughtful, playful advice",
            system_prompt="""You are The Trickster — the wise fool who gives surprisingly good advice with a playful twist.

ADVICE MODE: Give thoughtful, practical advice wrapped in playful wisdom.

Style
- Be genuinely helpful but keep it light
- Add a playful or whimsical element
- Keep advice practical and actionable
- 1-2 sentences maximum
- Avoid medical, legal, or financial advice

Behavior
- Focus on general life wisdom
- Add a trickster's perspective
- Keep it safe and appropriate
- Make it memorable and fun""",
            keywords=["advice", "help", "problem", "issue", "what should I do", "suggestion"],
            synonyms=["advise", "guidance", "counsel", "recommendation", "tip", "hint", "suggestions", "trouble", "difficulty", "challenge", "dilemma", "question", "wondering", "confused", "stuck"],
            priority=2
        ))
        
        # Stories template
        self.register_template(PromptTemplate(
            name="stories",
            description="Tell or request short stories",
            system_prompt="""You are The Trickster — the master storyteller who weaves tiny tales of wonder and mischief.

STORY MODE: Tell very short, engaging stories (2-3 sentences maximum) or ask users to tell you stories.

Style
- Stories should be 2-3 sentences maximum
- Include a twist or surprise ending
- Vivid imagery and playful language
- Can be about anything but keep it appropriate

Behavior
- Ask users to tell you stories too
- React to their stories with enthusiasm
- Keep your own stories very brief
- Make them memorable and fun""",
            keywords=["story", "tale", "narrative", "tell me a story", "once upon a time"],
            synonyms=["stories", "tales", "narratives", "fable", "fables", "legend", "legends", "myth", "myths", "adventure", "adventures", "journey", "journeys", "epic", "epics"],
            priority=2
        ))
        
        # Fashion template (requires webcam)
        self.register_template(PromptTemplate(
            name="fashion",
            description="Evaluate fashion and style via webcam",
            system_prompt="""You are The Trickster — the fashion-forward friend who gives playful style commentary.

FASHION MODE: Analyze the user's outfit through the webcam and give playful, positive fashion feedback.

Style
- Be encouraging and positive
- Focus on colors, style, and overall vibe
- Add playful suggestions
- Keep it brief and fun
- 1-2 sentences maximum

Behavior
- Always be encouraging, never critical
- Focus on what works well
- Add playful style suggestions
- Keep it light and fun""",
            keywords=["fashion", "outfit", "style", "clothes", "dress", "look", "appearance"],
            synonyms=["fashionable", "stylish", "outfits", "clothing", "attire", "ensemble", "wardrobe", "dressed", "looking", "appearances", "style advice", "fashion advice", "how do I look", "what do you think of my outfit"],
            priority=3,
            requires_webcam=True
        ))
    
    def get_random_question(self) -> str:
        """Get a random engaging question from the curated list."""
        questions = [
            # Fun & Playful
            "If you could have any superpower for just one day, what would it be and why?",
            "What's the most ridiculous thing you've ever done to avoid doing something else?",
            "If your life was a movie, what would the title be?",
            "What's the weirdest food combination you actually enjoy?",
            "If you could time travel to any era for a week, where would you go?",
            
            # Creative & Imaginative
            "What's the most creative solution you've ever come up with for a problem?",
            "If you could invent any gadget to make life easier, what would it do?",
            "What's the most beautiful place you've ever imagined but never visited?",
            "If you could paint your dreams, what colors would dominate the canvas?",
            "What's the most magical moment you've ever experienced?",
            
            # Personal Growth
            "What's something you've learned about yourself recently that surprised you?",
            "What's the best piece of advice you've ever received?",
            "What's something you're looking forward to that most people wouldn't understand?",
            "What's a skill you wish you had that would make life more fun?",
            "What's the most valuable lesson you've learned from a mistake?",
            
            # Social & Relationships
            "What's the most interesting conversation you've had with a stranger?",
            "What's something you do that always makes people smile?",
            "What's the most thoughtful thing someone has done for you?",
            "What's a tradition you've created with friends or family?",
            "What's the most unexpected friendship you've ever formed?",
            
            # Adventure & Experience
            "What's the most spontaneous thing you've ever done that turned out great?",
            "What's the most beautiful sound you've ever heard?",
            "What's the most peaceful moment you can remember?",
            "What's something you've always wanted to try but haven't yet?",
            "What's the most interesting person you've ever met and why?",
            
            # Philosophy & Reflection
            "What's something you believe that most people would disagree with?",
            "What's the most important thing you've changed your mind about?",
            "What's something that always makes you feel hopeful?",
            "What's the most meaningful compliment you've ever received?",
            "What's something you're grateful for that you used to take for granted?",
            
            # Fun Hypotheticals
            "If you could have dinner with any fictional character, who would it be?",
            "What's the most ridiculous thing you'd do for a million dollars?",
            "If you could master any skill instantly, what would you choose?",
            "What's the most interesting thing you've ever found?",
            "If you could solve any mystery in history, which would you pick?",
            
            # Light & Engaging
            "What's the most fun you've ever had doing something you were terrible at?",
            "What's something that always makes you laugh, no matter how many times you see it?",
            "What's the most interesting thing you've learned this week?",
            "What's something you're excited about that's coming up soon?",
            "What's the most beautiful thing you've seen today?"
        ]
        return random.choice(questions)
    
    def register_template(self, template: PromptTemplate):
        """Register a new prompt template."""
        self.templates[template.name] = template
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get a template by name."""
        return self.templates.get(name)
    
    def list_templates(self) -> List[str]:
        """List all available template names."""
        return list(self.templates.keys())
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two strings using SequenceMatcher."""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text, removing punctuation and converting to lowercase."""
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def _score_template_match(self, template: PromptTemplate, user_input: str) -> float:
        """Calculate a score for how well a template matches the user input."""
        score = 0.0
        user_words = self._extract_words(user_input)
        user_input_lower = user_input.lower()
        
        # Check exact keyword matches (highest weight)
        for keyword in template.keywords:
            if keyword.lower() in user_input_lower:
                score += 2.0  # Exact match gets high score
        
        # Check synonym matches (medium weight)
        if template.synonyms:
            for synonym in template.synonyms:
                if synonym.lower() in user_input_lower:
                    score += 1.5  # Synonym match gets medium score
        
        # Check word-level fuzzy matching (lower weight)
        for word in user_words:
            for keyword in template.keywords:
                similarity = self._calculate_similarity(word, keyword)
                if similarity > 0.8:  # High similarity threshold
                    score += similarity * 0.5
            
            if template.synonyms:
                for synonym in template.synonyms:
                    similarity = self._calculate_similarity(word, synonym)
                    if similarity > 0.8:
                        score += similarity * 0.3
        
        # Add priority bonus
        score += template.priority * 0.1
        
        # Bonus for longer, more specific matches
        if len(user_words) > 2:
            # Check for multi-word phrases
            for i in range(len(user_words) - 1):
                phrase = f"{user_words[i]} {user_words[i+1]}"
                for keyword in template.keywords:
                    if keyword.lower() in phrase:
                        score += 0.5  # Multi-word phrase bonus
                if template.synonyms:
                    for synonym in template.synonyms:
                        if synonym.lower() in phrase:
                            score += 0.3
        
        return score
    
    def select_template_autonomous(self, user_input: str, available_features: Dict[str, bool] = None) -> PromptTemplate:
        """Autonomously select the best prompt template based on user input."""
        if available_features is None:
            available_features = {"webcam": False, "keypad": False}
        
        # Score each template based on smart matching and constraints
        scores = {}
        
        for name, template in self.templates.items():
            # Check if template requirements are met
            if template.requires_webcam and not available_features.get("webcam", False):
                continue  # Skip templates that require unavailable features
            if template.requires_keypad and not available_features.get("keypad", False):
                continue
            
            # Calculate smart score
            score = self._score_template_match(template, user_input)
            scores[name] = score
        
        # Debug logging
        print(f"=== SMART TEMPLATE SCORING ===")
        print(f"User Input: '{user_input}'")
        for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            print(f"  {name}: {score:.2f}")
        print(f"===============================")
        
        # Return the template with the highest score, or questions as fallback
        if scores:
            best_template = max(scores.items(), key=lambda x: x[1])
            if best_template[1] > 0:
                return self.templates[best_template[0]]
        
        # Default to questions mode (fallback)
        return self.templates.get("questions", self.templates["questions"])

# Global registry instance
prompt_registry = PromptRegistry()
