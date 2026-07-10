from functions.get_files_info import get_files_info

dict = "."
print(f'Result for "{dict}":\n{get_files_info("calculator", dict)}')
dict = "pkg"
print(f'Result for "{dict}":\n{get_files_info("calculator", dict)}')
dict = "/bin"
print(f'Result for "{dict}":\n{get_files_info("calculator", dict)}')
dict = "../"
print(f'Result for "{dict}":\n{get_files_info("calculator", dict)}')
