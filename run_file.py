import subprocess
import os


def main():
	# Get the current directory
	current_dir = os.path.dirname(os.path.abspath(__file__))

	# Execute the first script
	subprocess.run(['python', 'python_scipts/autofill.py'], check=True)

	# Execute the second script
	subprocess.run(['python', os.path.join(current_dir, 'python_scripts', 'app.py')], check=True)

	# Execute the third script
	subprocess.run(['python', 'app.py'], check=True)


if __name__ == '__main__':
	main()
