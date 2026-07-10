from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")


print(f"\nResult for 'main.py':\n{get_file_content("calculator", "main.py")}")
print(f"\nResult for 'pkg/calculator.py':\n{get_file_content("calculator", "pkg/calculator.py")}")
print(f"\nResult for '/bin/cat':\n{get_file_content("calculator", "/bin/cat")}")
print(f"\nResult for 'pkg/does_not_exist.py':\n{get_file_content("calculator", "pkg/does_not_exist.py")}")
