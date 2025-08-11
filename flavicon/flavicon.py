from PIL import Image 
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Convert your logo or image to a flavicon for your website")
    parser.add_argument("input", type=str, help="Path to the image to convert")
    parser.add_argument("-o", "--output", default="./flavicon.ico", type=str, help="Path to the output file")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    _input, _output = args.input, args.output
    if not _input:
        _input = input("Enter the path to the image to convert: ").strip()
    if not _output:
        try:
            _output = input("Enter the path to the output file: ").strip()
        except EOFError:
            _output = "flavicon.ico"
    if not _output.endswith(".ico"):
        _output = _output.split(".")[0] + ".ico"
    img = Image.open(_input) 
    img.save(_output, format="ICO", sizes=[(256,256), (128,128), (64,64), (48,48), (32,32), (16,16)])
    print(f"Flavicon saved to {_output}")

if __name__ == "__main__":
    main()
