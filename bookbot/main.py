from stats import count_words, count_characters, sort
import sys

def get_book_text(filepath):
	try:
		with open(filepath) as f:
			file_contents = f.read()
		return file_contents
	except FileNotFoundError:
		print(f"Sorry, the file {filepath} does not exist.")
		return None

def create_report(filepath, num_words, num_chars):
	alpha_chars = ""
	for char in num_chars:
		if char["char"].isalpha():
			alpha_chars += f"{char['char']}: {char['num']}\n"
	report = (
		f"\n"
		f"============ BOOKBOT ============\n"
		f"Analyzing book found at {filepath}...\n"
		f"----------- Word Count ----------\n"
		f"Found {num_words} total words\n"
		f"--------- Character Count -------\n"
		f"{alpha_chars}\n"
		f"============= END ==============="
		f"\n"
	)
	return report

def main():
	if len(sys.argv) < 2:
		print("Usage: python3 main.py <path_to_book>")
		sys.exit(1)
	filepath = sys.argv[1]
	book_content = get_book_text(filepath)
	num_words = count_words(book_content)
	num_chars = count_characters(book_content)
	num_chars = sort(num_chars)
	report = create_report(filepath, num_words, num_chars)
	print(report)

main()

