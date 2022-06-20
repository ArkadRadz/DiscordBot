import random
from discord.ext import commands

class wordle(commands.Cog):
    guess_status = '⬜⬜⬜⬜⬜'
    correct_word_guess = '🟩'
    invalid_placement_guess = '🟨'
    missing_word_guess = '🟥'
    current_attempt = 0
    words = ''
    has_won = ''
    tried_words = []
    current_word = ''
    guess_history = []

    current_games = {}

    @commands.command(name="wordle")
    async def start_wordle(self, ctx):
        if ctx.author.name not in self.current_games or self.current_games[ctx.author.name] == '':
            target_word = random.choice(self.words)
            self.current_games[ctx.author.name] = target_word
            await ctx.send(f'Generated new word, start guessing with !guess [word]')
            print(target_word)
            return
        else:
            await ctx.send(f"You already have a generated word. Start guessing with !guess [word]")

    @commands.command(name="guess")
    async def guess(self, ctx, guess: str):
        if ctx.author.name not in self.current_games or self.current_games[ctx.author.name] == '':
            await ctx.send('Invalid command order, run !wordle first to generate new word')
            return

        user_guess = guess

        await self.validate_guess_input(ctx, user_guess)

        self.current_attempt += 1
        current_attempt_message = f'**{ctx.author.name}** Current attempt {self.current_attempt}/6'
            
        await ctx.send('{} \n'.format(current_attempt_message))

        target_word = self.current_games[ctx.author.name]

        if target_word == user_guess:
            self.guess_history.append(f'{user_guess}        -        {self.correct_word_guess * 5}')
            await ctx.send('You won')
            self.has_won = True
            self.current_games[ctx.author.name] = ''
            self.current_attempt = 0

            final_msg = '**{}** guesses:\n{}'.format(ctx.author.name, '\n'.join(self.guess_history))
            await ctx.send(final_msg)

            self.guess_history = []
            return 

        result = self.check_guess(user_guess, self.current_games[ctx.author.name])

        # await ctx.send(f'{result}')
        await ctx.send('\n'.join(self.guess_history))


    def __init__(self, bot) -> None:
        self.words = self.populate_word_list()
        self.bot = bot

    def main_loop(self, target_word, current_attempt = 0):
        if current_attempt == 6:
            self.has_won = False
            return

        print(f'Current attempt {current_attempt}/6', end='\n')

        if len(self.tried_words) > 0:
            tried_words_string = ', '.join(self.tried_words)
            print(f'Currently tried words [{tried_words_string}]', end='\n')

        user_guess = self.get_user_guess()

        if target_word == user_guess:
            self.has_won = True
            return 

        result = self.check_guess(user_guess, target_word)

        print(result)
        current_attempt += 1

        if current_attempt < 6:
            self.main_loop(target_word=target_word, current_attempt=current_attempt)


    def check_guess(self, guess, target):
        result = ['', '', '', '', '']
        for index, guess_letter in enumerate(guess):
            search_result = target.find(guess_letter)
            
            result[index] = self.invalid_placement_guess

            if search_result == -1:
                result[index] = self.missing_word_guess

            if target[index] == guess[index]:
                result[index] = self.correct_word_guess

            if target.count(guess_letter) > 2:
                result[index] = self.invalid_placement_guess

        guess_result = ''.join(result)
        guess_message = f'{guess}        -        {guess_result}'
        self.guess_history.append(guess_message)
        return guess_message


    def get_user_guess(self):
        proper_input_entered = False

        while proper_input_entered is not True:
            guess = input('Enter your guess \n')
            proper_input_entered = self.validate_guess_input(guess)

        return guess

    async def validate_guess_input(self, ctx, guess):
        if ctx.author.name not in self.current_games:
            await ctx.send('Invalid command order.')
            return

        if len(guess) != 5 or guess not in self.words:
            await ctx.send('Invalid guess')
            return

    def populate_word_list(self):
        with open('word_list.txt', 'r') as word_file:
            return word_file.read().splitlines()
        
    def start(self):
        target_word = random.choice(self.words)
        self.main_loop(target_word=target_word)

        if self.has_won:
            print(self.correct_word_guess * 5, end='\n')
            print('You won')
        else:
            print(f'You lost, target word was: {target_word}')