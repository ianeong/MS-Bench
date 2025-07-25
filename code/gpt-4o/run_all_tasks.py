import subprocess


# Function to run calligraphy-related scripts
def run_calligraphy_recognition():
    subprocess.run(['python', 'calligraphy_recognition.py'])
    subprocess.run(['python', 'calligraphy_recognition_cot.py'])
    subprocess.run(['python', 'calligraphy_recognition_know.py'])


# Function to run date determination-related scripts
def run_date_determination():
    subprocess.run(['python', 'date_determination.py'])
    subprocess.run(['python', 'date_determination_cot.py'])
    subprocess.run(['python', 'date_determination_know.py'])
    subprocess.run(['python', 'date_determination_binary.py'])


# Function to run image classification script
def run_image_classification():
    subprocess.run(['python', 'image_classification.py'])


def run_manuscript_ocr():
    subprocess.run(['python', 'manuscript_ocr.py'])


# Function to run symbol recognition-related scripts
def run_symbol_recognition():
    subprocess.run(['python', 'symbol_recognition.py'])
    subprocess.run(['python', 'symbol_recognition_cot.py'])
    subprocess.run(['python', 'symbol_recognition_know.py'])
    subprocess.run(['python', 'symbol_recognition_binary.py'])


# Function to run variant-related scripts
def run_variant():
    subprocess.run(['python', 'variant_least.py'])
    subprocess.run(['python', 'variant_medium.py'])
    subprocess.run(['python', 'variant_most.py'])


def run_splice():
    subprocess.run(['python', 'splice_boolean.py'])
    subprocess.run(['python', 'splice_direction.py'])
    subprocess.run(['python', 'splice_score.py'])

def run_image_caption():
    subprocess.run(['python', 'image_caption.py'])

def run_count():
    subprocess.run(['python', 'count_row.py'])
    subprocess.run(['python', 'count_average.py'])

def run_status():
    subprocess.run(['python', 'status.py'])

# Main function to control which program to run
def main():
    run_calligraphy_recognition()
    run_date_determination()
    run_image_classification()
    run_manuscript_ocr()
    run_symbol_recognition()
    run_variant()
    run_splice()
    run_image_caption()
    run_count()
    run_status()

if __name__ == "__main__":
    main()
