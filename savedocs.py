import csv
import os
import requests

# Function to download documents
def download_documents(document_ids, document_filenames, output_folder, bearer_token):
    base_url = 'https://example.com/api/download'  # Replace with your API endpoint
    failed_downloads = []
    for doc_id, filename in zip(document_ids, document_filenames):
        params = {'id': doc_id}
        headers = {'Authorization': f'Bearer {bearer_token}'}
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            # Create the output folder if it does not exist
            os.makedirs(output_folder, exist_ok=True)
            # Save the document to the output folder with document filename
            try:
                with open(os.path.join(output_folder, filename), 'wb') as f:
                    f.write(response.content)
                print(f'Document {filename} downloaded successfully.')
            except Exception as e:
                print(f'Failed to save document {filename}: {e}')
                failed_downloads.append({'document.id': doc_id, 'document.filename': filename, 'status': 'Failed'})
        else:
            print(f'Failed to download document {filename}.')
            failed_downloads.append({'document.id': doc_id, 'document.filename': filename, 'status': 'Failed'})

    # Write failed downloads to CSV
    if failed_downloads:
        failed_csv_file = f'{csv_file}_fails.csv'
        with open(failed_csv_file, 'w', newline='') as csvfile:
            fieldnames = ['document.id', 'document.filename', 'status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(failed_downloads)
        print(f'Failed downloads logged to {failed_csv_file}')

# Function to read document IDs and filenames from CSV
def read_documents(csv_file):
    document_ids = []
    document_filenames = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            document_ids.append(row['document.id'])
            document_filenames.append(row['document.filename'])
    return document_ids, document_filenames

# Main function
def main():
    csv_file = 'documents.csv'  # Replace with your CSV file name
    output_folder = 'downloaded_documents'  # Replace with your output folder path

    # Input bearer token
    bearer_token = input("Enter Bearer Token: ")

    document_ids, document_filenames = read_documents(csv_file)
    download_documents(document_ids, document_filenames, output_folder, bearer_token)

if __name__ == "__main__":
    main()
