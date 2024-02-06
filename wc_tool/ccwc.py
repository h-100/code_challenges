import argparse
import select
import sys
from pathlib import Path


def number_of_words(data):
    return len(data.split())

def num_characters(data):
  return len(data)

def num_bytes(data):
  return len(bytes(data, 'utf-8'))

def num_lines(data):
  return len(data.splitlines())

def is_file_present(target_file):
  if not Path(target_file).is_file():
    print("the target file doesn't exist, please create a file")
    raise SystemExit(1)
  else:
    return True

def is_stdin():
  if select.select([sys.stdin], [], [], 0.0)[0]:
    return True
  else:
    return False 
  
def read_stdin_data():
  return sys.stdin.read() 

def get_file_data(target_file):
  if is_file_present(target_file):
    with open(Path(target_file), 'r') as f:
      return f.read()
  
def get_results_from_data(args, input_data, target_file=''):
  stat_list = []
  result_string = ""
  
  if args.lines:
    lines = num_lines(input_data)
    result_string += f'    {lines}'
    stat_list.append(lines)

  if args.words:
    words = number_of_words(input_data)
    result_string += f'    {words}'
    stat_list.append(words)

  if args.count:
    bytes = num_bytes(input_data)
    result_string += f'    {bytes}'
    stat_list.append(bytes)

  if args.multi:
    multi_bytes = num_characters(input_data)
    result_string += f'    {multi_bytes}'
    stat_list.append(multi_bytes)

  (result_string := result_string + f' {target_file}' )

  return [result_string, stat_list]
    
def get_results_per_file(args, target_file):
  input_data = get_file_data(target_file)
  return get_results_from_data(args, input_data, target_file)

def get_results_all_files(args):
  final_result_string = ""
  stat_list_total = []

  for f in args.file_names:
    result_string, stat_list = get_results_per_file(args, f)
    final_result_string += result_string + '\n'
    stat_list_total.append(stat_list)


  final_results = [sum(x) for x in zip(*stat_list_total)]
  for item in final_results:
    final_result_string += f'    {item}'

  (final_result_string := final_result_string + f' total' )

  return final_result_string

def get_results_from_stdin(args):
  input_data = read_stdin_data()
  return get_results_from_data(args, input_data)

def main():
  parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
  description="""
  NAME:                             
       wc tool: unix-like tool for word count
                                   
  DESCRIPTION:                                  
      The wc tool displays the number of lines, words and bytes contained in each input file or 
      via standard input. You can append multiple filenames at the end or use any unix command 
      to pipe input data into the utlity.

      Use one of -w, -l, -c, -m flags to display number of words, lines, bytes and characters.

      The result displayed would always be in "lines, words, character count" order

  USAGE:
      python3 ccwc.py -w -l -c -m file_name1 file_name2
  """)
  parser.add_argument("-c", "--count", action="store_true", help="count number of bytes")
  parser.add_argument("-w", "--words", action="store_true", help="count number of words")
  parser.add_argument("-l", "--lines", action="store_true", help="count number of lines")
  parser.add_argument("-m", "--multi", action="store_true", help="count number of characters")
  parser.add_argument("file_names", nargs='*', help="one or more file names as input")
  
  args = parser.parse_args()

  if is_stdin():
    if len(args.file_names) == 0:
      result_string = get_results_from_stdin(args)[0]
      print(result_string)
    else:
      print("ERROR: cannot use both piping and filenames, please use one input method")
      raise SystemExit(1)

  else:
    if len(args.file_names) == 0:
      print("ERROR: Please add a file name at the end")
      raise SystemExit(1)
    else:
      if len(args.file_names) > 1:
        final_result_string = get_results_all_files(args)
        print(final_result_string)

      elif len(args.file_names) == 1:
        result_string, stat_list = get_results_per_file(args, args.file_names[0])
        print(result_string)

if __name__ == "__main__":
  main()