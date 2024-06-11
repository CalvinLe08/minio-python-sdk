import argparse
import os
from minio import Minio
from minio.error import S3Error

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Upload or download a file to/from MinIO server.")
    parser.add_argument('operation', choices=['upload', 'download'], help="Operation to perform: 'upload' or 'download'.")
    parser.add_argument('file_path', type=str, help="Path to the source file to be uploaded or the object name to be downloaded from MinIO.")
    parser.add_argument('--destination', type=str, help="Destination directory for the downloaded file. If not provided, the file will be saved in the current directory with its original name.")
    
    args = parser.parse_args()
    
    # Create a MinIO client
    client = Minio("localhost:9000",
                   access_key="minio",
                   secret_key="minio123",
                   secure=False)
    
    # Determine the operation
    if args.operation == 'upload':
        # Upload operation
        source_file = args.file_path
        destination_name = os.path.basename(source_file)
        folder_name = determine_folder(destination_name)
        bucket_name = "warehouse-script"
        destination_path = f"{folder_name}/{destination_name}"
        upload(client, bucket_name, source_file, destination_path)
    elif args.operation == 'download':
        # Download operation
        object_name = args.file_path
        destination_dir = args.destination
        
        if destination_dir:
            # Ensure the destination is a directory
            if not os.path.isdir(destination_dir):
                print(f"Error: {destination_dir} is not a valid directory.")
                return
            # Download the file into the specified directory with the original name
            destination_path = os.path.join(destination_dir, os.path.basename(object_name))
        else:
            # If no destination is provided, download to the current directory
            destination_path = os.path.basename(object_name)
        
        download(client, "warehouse-script", object_name, destination_path)

def determine_folder(filename):
    # Mapping of file extensions to folder names
    extension_to_folder = {
        '.csv': 'structured',
        '.tsv': 'structured',
        '.xls': 'structured',
        '.xlsx': 'structured',
        '.xlsm': 'structured',
        '.xlt': 'structured',
        '.xltx': 'structured',
        '.xltm': 'structured',
        '.ods': 'structured',
        '.json': 'semi-structured',
        '.xml': 'semi-structured',
        '.yaml': 'semi-structured',
        '.yml': 'semi-structured',
        '.jpg': 'unstructured',
        '.jpeg': 'unstructured',
        '.png': 'unstructured',
        '.gif': 'unstructured',
        '.bmp': 'unstructured',
        '.tiff': 'unstructured',
        '.pdf': 'unstructured',
        '.doc': 'unstructured',
        '.docx': 'unstructured',
        '.ppt': 'unstructured',
        '.pptx': 'unstructured',
        '.txt': 'unstructured',
        '.rtf': 'unstructured',
    }
    # Extract the file extension
    ext = os.path.splitext(filename)[1].lower()
    
    # Return the corresponding folder name or a default
    return extension_to_folder.get(ext, 'others')

def upload(client, bucket_name, source_file_path, destination_name):
    # Make the bucket if it doesn't exist.
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    # Upload the file to the specified folder (destination_name includes the folder path)
    client.fput_object(
        bucket_name, destination_name, source_file_path
    )
    print(
        source_file_path, "successfully uploaded as object",
        destination_name, "to bucket", bucket_name,
    )

def download(client, bucket_name, object_name, destination_path):
    try:
        client.fget_object(bucket_name, object_name, destination_path)
        print(
            "Object", object_name, "successfully downloaded to",
            destination_path,
        )
    except S3Error as exc:
        print("Error occurred: ", exc)

if __name__ == "__main__":
    main()
