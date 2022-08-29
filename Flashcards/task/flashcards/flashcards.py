import csv
import random
from io import StringIO
import argparse


class Flashcard:
    parser = argparse.ArgumentParser()
    parser.add_argument("--import_from")
    parser.add_argument("--export_to")
    args = parser.parse_args()

    def __init__(self):
        self.list_saved_cards = []
        self.log_file = StringIO()

        if Flashcard.args.import_from:
            self.import_cards()

    def add(self):

        # Takes card name and check if it exists
        print('The card:')
        print('The card:', file=self.log_file)
        while True:
            new_card_term = input()
            self.log_file.write(new_card_term + '\n')

            # Create a list of cards to check if new exists already
            card_list = [list(card.values())[0] for card in self.list_saved_cards]

            if new_card_term in card_list:
                print(f'The card "{new_card_term}" already exists. Try again:', file=self.log_file)
                print(f'The card "{new_card_term}" already exists. Try again:')
                continue
            else:
                break

        # Takes definition and check if it exists
        print('The definition of the card:')
        print('The definition of the card:', file=self.log_file)
        while True:
            new_card_definition = input()
            self.log_file.write(new_card_definition + '\n')

            # Create a list of terms to check if new exists already
            term_list = [list(term.values())[1] for term in self.list_saved_cards]

            if new_card_definition in term_list:
                print(f'The definition "{new_card_definition}" already exists. Try again:', file=self.log_file)
                print(f'The definition "{new_card_definition}" already exists. Try again:')
                continue
            else:
                break

        # Set default dictionary for error count
        definition_error = {}
        definition_error.setdefault('Errors', 0)

        # Adds the card to the dictionary
        self.list_saved_cards.append({'Card': new_card_term, 'Definition': new_card_definition, 'Errors': 0})

        print(f'The pair ("{new_card_term}":"{new_card_definition}") has been added.', file=self.log_file)
        print(f'The pair ("{new_card_term}":"{new_card_definition}") has been added.')

    def remove(self):
        flag = False
        remove_card = input('Which card?\n')

        print('Which card?\n', file=self.log_file)
        self.log_file.write(remove_card + '\n')

        for card in range(len(self.list_saved_cards)):
            if self.list_saved_cards[card]['Card'] == remove_card:
                del self.list_saved_cards[card]
                flag = True
                break

        if flag:
            print('The card has been removed.', file=self.log_file)
            print('The card has been removed.')
        else:
            print(f'Can\'t remove "{remove_card}": there is no such card.', file=self.log_file)
            print(f'Can\'t remove "{remove_card}": there is no such card.')

    def import_cards(self):
        # Type filename to be imported (default name is 'exported_cards')
        filename = Flashcard.args.import_from or input('File name:\n') or 'exported_cards'
        count = 0

        print('File name:\n', file=self.log_file)
        self.log_file.write(filename + '\n')

        try:
            with open(f'{filename}', 'r', encoding='utf-8') as import_file:
                file_reader = csv.DictReader(import_file, delimiter=',')
                for card in file_reader:
                    self.list_saved_cards.append({'Card': card['term'], 'Definition': card['definition'], 'Errors': card['errors']})
                    count += 1
        except FileNotFoundError:
            print('File not found.', file=self.log_file)
            print('File not found.')

        print(f'{count} cards have been loaded.', file=self.log_file)
        print(f'{count} cards have been loaded.')

    def export_cards(self):
        # Type filename to be exported (default name is 'exported_cards')
        filename = Flashcard.args.export_to or input('File name:\n') or 'exported_cards'

        print('File name:\n', file=self.log_file)
        self.log_file.write(filename)

        with open(f'{filename}', 'w', encoding='utf-8') as export_file:
            headers = ['term', 'definition', 'errors']
            file_write = csv.DictWriter(export_file, delimiter=',', lineterminator='\n', fieldnames=headers)
            file_write.writeheader()

            for card in self.list_saved_cards:
                term, definition, errors = card.values()
                file_write.writerow({'term': term, 'definition': definition, 'errors': errors})

        # Print how many cards have been saved
        print(f'{len(self.list_saved_cards)} cards have been saved.', file=self.log_file)
        print(f'{len(self.list_saved_cards)} cards have been saved.')

    def ask(self):
        times_to_ask = int(input('How many times to ask?\n'))

        print('How many times to ask?\n', file=self.log_file)
        self.log_file.write(str(times_to_ask) + '\n')

        # Iterate through a dictionary in pairs: (key:value)
        while times_to_ask > 0:
            error = False

            # Randomly selects card
            card, definition, errors = random.choice(self.list_saved_cards).values()
            # Utilize card
            times_to_ask -= 1

            input_definition = input(f'Print the definition of "{card}":\n')
            print(f'Print the definition of "{card}":\n', file=self.log_file)
            self.log_file.write(input_definition)

            if input_definition == definition:
                print('Correct!')
                print('Correct!', file=self.log_file)

            elif input_definition in [list(defin.values())[1] for defin in self.list_saved_cards]:
                right_key = [r_k['Card'] for r_k in self.list_saved_cards if r_k['Definition'] == input_definition][0]
                print(f'Wrong. The right answer is "{definition}", but your definition is correct for "{right_key}".')
                print(f'Wrong. The right answer is "{definition}", but your definition is correct for "{right_key}".', file=self.log_file)
                error = True

            else:
                print(f'Wrong. The right answer is "{definition}".', file=self.log_file)
                print(f'Wrong. The right answer is "{definition}".')
                error = True

            if error:
                # Increase number of errors for the chosen card
                for item in self.list_saved_cards:
                    if item['Card'] == card:
                        numb_of_err = int(item.get('Errors')) + 1
                        item.update({'Errors': numb_of_err})

    def exit_(self):
        print('Bye bye!')
        print('Bye bye!', file=self.log_file)

        if Flashcard.args.export_to:
            self.export_cards()

        self.log_file.close()
        return exit()

    def log(self):
        print('File name:')
        print('File name:', file=self.log_file)

        filename = input()
        self.log_file.write(filename + '\n')

        log_file = open(f'{filename}', 'w', encoding='utf-8')

        print('The log has been saved.')
        print('The log has been saved.', file=self.log_file)

        self.log_file.seek(0)
        log_file.write(self.log_file.getvalue())
        log_file.close()

    def hardest_card(self):
        cards_sorted_list = sorted(self.list_saved_cards, key=lambda d: int(d['Errors']), reverse=True)

        if cards_sorted_list:
            error = cards_sorted_list[0].get('Errors')

            cards_sorted_list = [item for item in cards_sorted_list if (item['Errors'] == error)]

        if len(cards_sorted_list) == 1:
            print(f'The hardest card is "{cards_sorted_list[0].get("Card")}". You have {cards_sorted_list[0].get("Errors")} errors answering it.')
            print(f'The hardest card is "{cards_sorted_list[0].get("Card")}". You have {cards_sorted_list[0].get("Errors")} errors answering it.', file=self.log_file)
        elif len(cards_sorted_list) > 1 and cards_sorted_list[0].get('Errors') != 0:
            result = []
            for item in range(len(cards_sorted_list)):
                result.append(f'"{cards_sorted_list[item]["Card"]}"')

            print(f'The hardest cards are {", ".join(result)}. You have {cards_sorted_list[0].get("Errors")} errors answering them.')
            print(f'The hardest cards are {", ".join(result)}. You have {cards_sorted_list[0].get("Errors")} errors answering them.', file=self.log_file)

        else:
            print('There are no cards with errors.')
            print('There are no cards with errors.', file=self.log_file)

    def reset_stats(self):
        for card in self.list_saved_cards:
            card.update({'Errors': 0})

        print('Card statistics have been reset.')
        print('Card statistics have been reset.', file=self.log_file)


if __name__ == '__main__':
    flashcard = Flashcard()

    action_dict = {'add': flashcard.add,
                   'remove': flashcard.remove,
                   'import': flashcard.import_cards,
                   'export': flashcard.export_cards,
                   'ask': flashcard.ask,
                   'exit': flashcard.exit_,
                   'log': flashcard.log,
                   'hardest card': flashcard.hardest_card,
                   'reset stats': flashcard.reset_stats}

    while True:
        action = input('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):\n')
        print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):', file=flashcard.log_file)
        flashcard.log_file.write(action + '\n')
        if action in action_dict.keys():
            # Calls the function inside a dictionary
            action_dict.get(action)()
